import csv
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
    def setUp(self) -> None:
        # Initialize the defacto-enrichment app
        self.app = App(json_object={"data": []}, data_dir=DATA_DIR)

        # Generate flattened mock appearances CSV file
        with open(self.app.appearance_csv, "w") as f:
            writer = csv.writer(f)
            writer.writerows(
                [
                    ["fact_check_rating", "clean_url"],
                    ["1", "url1"],
                    ["1", "url1"],
                ]
            )
        # Generate flattened mock fact-check CSV file
        with open(self.app.fact_check_csv, "w") as f:
            writer = csv.writer(f)
            writer.writerows(
                [
                    ["fact_check_rating", "clean_url"],
                    ["5", "url1"],
                ]
            )

    def test_url_deduplication(self) -> None:
        """Test that Minall's enrichment transforms a CSV with 2 identical URLs
        into a CSV file with 1 URL / 1 row.
        """
        self.app.enrichment(minall_output=MINALL_OUTPUT, with_shared_content_file=False)
        result_count = casanova.count(self.app.appearance_csv)
        assert result_count == 1

    def tearDown(self) -> None:
        [file.unlink() for file in MINALL_OUTPUT.iterdir() if file.is_file()]
        [file.unlink() for file in DATA_DIR.iterdir() if file.is_file()]
        MINALL_OUTPUT.rmdir()
        DATA_DIR.rmdir()


if __name__ == "__main__":
    unittest.main()
