import json
import os
import unittest
from pathlib import Path

from defacto_enrichment.main import App
from minall.main import Minall


class TestFactCheck(unittest.TestCase):
    TEST_DATA = {}
    CONFIG = {}

    def setUp(self):
        self.TEST_DATA_DIR = Path(__file__).parent.joinpath("data")
        self.TEST_DATA_DIR.mkdir(exist_ok=True)
        self.TEST_MINALL_OUTPUT = Path(__file__).parent.joinpath("minall_output")
        self.TEST_MINALL_OUTPUT.mkdir(exist_ok=True)
        self.fact_check_csv = self.TEST_DATA_DIR.joinpath("fact_checks.csv")

    def test_enrichment(self):
        self.app = App(data_dir=self.TEST_DATA_DIR, json_object=self.TEST_DATA)
        self.app.flatten_export()
        minall = Minall(
            database=None,
            config=self.CONFIG,
            output_dir=str(self.TEST_MINALL_OUTPUT),
            links_file=str(self.fact_check_csv),
            url_col="clean_url",
            shared_content_file=None,
            buzzsumo_only=True,
        )
        minall.collect_and_coalesce()
        fact_check_file, _ = minall.export()
        fact_check_file.rename(self.fact_check_csv)

    def tearDown(self) -> None:
        [file.unlink() for file in self.TEST_DATA_DIR.iterdir() if file.is_file()]
        self.TEST_DATA_DIR.rmdir()
        [file.unlink() for file in self.TEST_MINALL_OUTPUT.iterdir() if file.is_file()]
        self.TEST_MINALL_OUTPUT.rmdir()


if __name__ == "__main__":
    config_file = os.environ["CONFIG"]
    with open(config_file, "r") as f:
        TestFactCheck.CONFIG = json.load(f)
    data_file = os.environ["DATA"]
    with open(data_file, "r") as f:
        TestFactCheck.TEST_DATA = json.load(f)
    unittest.main()
