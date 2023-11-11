import sys
import unittest
from pathlib import Path

import flatten
from defacto_enrichment.main import App

DATA_DIR = Path(flatten.__file__).parent.joinpath("data")
DATA_DIR.mkdir(exist_ok=True)


class TestFlatten(unittest.TestCase):
    DATABASE_EXPORT: Path | None = None

    def setUp(self) -> None:
        if self.DATABASE_EXPORT:
            self.app = App(data_dir=DATA_DIR, database_export_file=self.DATABASE_EXPORT)
        else:
            self.app = App(data_dir=DATA_DIR)

    def test(self) -> None:
        self.app.flatten_export()

    def tearDown(self) -> None:
        [file.unlink() for file in DATA_DIR.iterdir()]
        DATA_DIR.rmdir()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        TestFlatten.DATABASE_EXPORT = Path(sys.argv.pop())
    unittest.main()
