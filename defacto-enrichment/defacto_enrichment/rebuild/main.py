import csv
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from sqlite3 import Connection, Cursor
from typing import Dict, Generator, Type

from defacto_enrichment.flatten.main import DataStream
from defacto_enrichment.types import Appearance, FactCheck, SharedContent
from minall.tables.base import BaseTable


@dataclass
class SharedContentTable:
    name = "shared_content"
    pk = ["post_url", "content_url"]


@dataclass
class AppearanceTable:
    name = "appearance"
    pk = ["exact_url"]


@dataclass
class FactCheckTable:
    name = "fact_check"
    pk = ["exact_url"]


class Selector:
    def __init__(
        self,
        table: Type[SharedContentTable | AppearanceTable | FactCheckTable],
        conn: Connection,
        infile: Path,
        outfile=Path(),
    ) -> None:
        self.conn = conn
        with open(infile) as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames
        if not columns:
            raise KeyError
        dtypes = {c: "TEXT" for c in columns}
        self.pk = getattr(table, "pk")
        self.table = BaseTable(
            name=getattr(table, "name"),
            pk=self.pk,
            conn=conn,
            dtypes=dtypes,
            outfile=outfile,
        )
        self.table.update_from_csv(datafile=infile)
        self.conn.row_factory = self.dict_factory

    def __call__(self, url: str) -> Generator[Dict, None, None]:
        sql = "SELECT * FROM %s WHERE %s = ?" % (self.table.name, self.pk[0])
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, (url,))
        except Exception as e:
            raise e
        rows = cursor.fetchall()
        yield from rows

    def dict_factory(self, cursor: Cursor, row) -> Dict:
        """Convert cursor result to dictionary with column names.

        Solution taken from: https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


def rebuild(
    database_export: Dict,
    appearances_csv: Path,
    shared_content_csv: Path,
    fact_check_csv: Path,
) -> Dict:
    # Set up streamer for JSON data
    stream = DataStream(data=database_export["data"])

    with sqlite3.connect(":memory:") as conn:
        fact_check_selector = Selector(
            table=FactCheckTable, conn=conn, infile=fact_check_csv
        )
        appearances_selector = Selector(
            table=AppearanceTable, conn=conn, infile=appearances_csv
        )
        media_selector = Selector(
            table=SharedContentTable, conn=conn, infile=shared_content_csv
        )

        # Enrich the fact-check articles
        for _, fact_check in stream.fact_checks():
            record = FactCheck.from_json(fact_check)
            if record.exact_url:
                match = list(fact_check_selector(record.exact_url))[0]
                fact_check.update(
                    {
                        "interactionStatistic": FactCheck.from_csv_dict_row(
                            match
                        ).to_json()
                    }
                )

            # Enrich the fact-check article's appearances
            for _, appearance, _ in stream.claim_reviews(fact_check):
                record = Appearance.from_json(appearance)
                if record.exact_url and record.clean_url:
                    match = list(appearances_selector(record.exact_url))[0]
                    appearance.update(Appearance.from_csv_dict_row(match).to_json())

                    shared_content = []
                    for match in media_selector(record.exact_url):
                        shared_content.append(
                            SharedContent.from_csv_dict_row(match).to_json()
                        )
                    if len(shared_content) > 0:
                        appearance.update({"sharedContent": shared_content})

    # Return modified JSON object
    return database_export


if __name__ == "__main__":
    import json
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--export")
    parser.add_argument("--appearances")
    parser.add_argument("--shared-content")
    parser.add_argument("--fact-checks")
    parser.add_argument("--outfile")
    args = parser.parse_args()

    with open(args.export, "r") as f:
        exported_data = json.load(f)

    data = rebuild(
        database_export=exported_data,
        appearances_csv=args.appearances,
        shared_content_csv=args.shared_content,
        fact_check_csv=args.fact_checks,
    )

    with open(args.outfile, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
