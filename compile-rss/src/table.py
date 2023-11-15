import csv
from pathlib import Path
from sqlite3 import Connection
from typing import Dict, List


class Table:
    def __init__(
        self, connection: Connection, name: str, fieldnames: List, primary_key: List
    ) -> None:
        self.connection = connection
        self.name = name
        self.columns = fieldnames
        self.primary_key = primary_key
        self.create()
        self.count = 0

    def create(self):
        cursor = self.connection.cursor()
        columns = ", ".join([f"{f} TEXT" for f in self.columns])
        primary_key = ",".join(self.primary_key)
        query = "CREATE TABLE %s (%s, PRIMARY KEY (%s))" % (
            self.name,
            columns,
            primary_key,
        )
        cursor.execute(query)
        self.connection.commit()

    def columns_to_update(self) -> str:
        columns = []
        for column in self.columns:
            if column not in self.primary_key:
                columns.append(f"{column} = COALESCE(excluded.{column}, {column})")
        return ", ".join(columns)

    def parse_row(self, d: Dict) -> List:
        o = []
        for v in d.values():
            if v == "":
                o.append(None)
            else:
                o.append(v)
        return o

    def coalesce(self, infile: Path):
        cursor = self.connection.cursor()

        res = cursor.execute(f"select count(*) from {self.name}")
        count = res.fetchone()[0]
        assert count >= self.count
        self.count = count
        print(self.name, count)

        columns_to_update = self.columns_to_update()
        primary_key = ",".join(self.primary_key)
        with open(infile, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                values = self.parse_row(row)
                n_values = ", ".join(["?" for _ in range(len(values))])
                query = f"""
                INSERT INTO {self.name} ({", ".join(self.columns)})
                VALUES ({n_values})
                ON CONFLICT ({primary_key})
                DO UPDATE SET {columns_to_update}
                """
                cursor.execute(query, tuple(values))
                self.connection.commit()
