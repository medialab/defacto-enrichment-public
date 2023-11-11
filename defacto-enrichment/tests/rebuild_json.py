import json
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
        self.app.flatten_export()

    def test_url_deduplication(self) -> None:
        self.app.rebuild_export()
        original_export = self.app.database_export_copy
        with open(self.app.new_export_json) as f:
            new_export = json.load(f)

        assert original_export == new_export

    # def tearDown(self) -> None:
    #     [file.unlink() for file in DATA_DIR.iterdir() if file.is_file()]
    #     DATA_DIR.rmdir()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        TestEnrich.DATABASE_EXPORT = Path(sys.argv.pop())
    unittest.main()
