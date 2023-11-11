import csv
import sys
import unittest
from pathlib import Path

import casanova
import flatten
from defacto_enrichment.main import App

DATA_DIR = Path(flatten.__file__).parent.joinpath("data")
DATA_DIR.mkdir(exist_ok=True)
MINALL_OUTPUT = Path(flatten.__file__).parent.joinpath("minall_output")
MINALL_OUTPUT.mkdir(exist_ok=True)


class TestEnrich(unittest.TestCase):
    DATABASE_EXPORT: Path | None = None

    def setUp(self) -> None:
        if self.DATABASE_EXPORT:
            self.app = App(data_dir=DATA_DIR, database_export_file=self.DATABASE_EXPORT)
        else:
            self.app = App(data_dir=DATA_DIR)
        with open(self.app.appearance_csv, "w") as f:
            writer = csv.writer(f)
            writer.writerows(
                [
                    ["fact_check_id", "url"],
                    ["id1", "url1"],
                    ["id2", "url1"],
                ]
            )
        with open(self.app.fact_check_csv, "w") as f:
            writer = csv.writer(f)
            writer.writerows(
                [
                    ["url"],
                ]
            )

    def test_url_deduplication(self) -> None:
        infile_count = casanova.count(self.app.appearance_csv)
        self.app.enrichment(minall_output=MINALL_OUTPUT, with_shared_content_file=False)
        result_count = casanova.count(self.app.appearance_csv)

        assert infile_count == 2
        assert result_count == 1

    def tearDown(self) -> None:
        [file.unlink() for file in MINALL_OUTPUT.iterdir() if file.is_file()]
        [file.unlink() for file in DATA_DIR.iterdir() if file.is_file()]
        MINALL_OUTPUT.rmdir()
        DATA_DIR.rmdir()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        TestEnrich.DATABASE_EXPORT = Path(sys.argv.pop())
    unittest.main()
