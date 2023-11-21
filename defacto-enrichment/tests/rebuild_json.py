import json
import unittest
from pathlib import Path

from defacto_enrichment.main import App


class TestRebuild(unittest.TestCase):
    def setUp(self):
        self.TEST_DATA_DIR = Path(__file__).parent.joinpath("data")
        self.TEST_DATA_DIR.mkdir(exist_ok=True)
        self.TEST_MINALL_OUTPUT = Path(__file__).parent.joinpath("minall_output")
        self.TEST_MINALL_OUTPUT.mkdir(exist_ok=True)

    def test_identical_json_object(self) -> None:
        self.app = App(data_dir=self.TEST_DATA_DIR, json_object=TEST_DATA_ENRICHED)
        self.app.flatten_export()
        self.app.rebuild_export()
        original_export = self.app.json_data_original_copy
        with open(self.app.new_export_json) as f:
            new_export = json.load(f)
        assert original_export == new_export

    def test_different_json_objects(self) -> None:
        self.app = App(data_dir=self.TEST_DATA_DIR, json_object=TEST_DATA_NOT_ENRICHED)
        self.app.flatten_export()
        self.app.enrichment(
            config={},
            minall_output=self.TEST_MINALL_OUTPUT,
        )
        self.app.rebuild_export()
        original_export = self.app.json_data_original_copy
        with open(self.app.new_export_json) as f:
            new_export = json.load(f)
        assert original_export != new_export

    def tearDown(self) -> None:
        [file.unlink() for file in self.TEST_DATA_DIR.iterdir() if file.is_file()]
        self.TEST_DATA_DIR.rmdir()
        [file.unlink() for file in self.TEST_MINALL_OUTPUT.iterdir() if file.is_file()]
        self.TEST_MINALL_OUTPUT.rmdir()


TEST_DATA_NOT_ENRICHED = {
    "data": [
        {
            "id": "Medias/Factuel/Fact-checks/Attention-aux-mauvaises-interpretations-d-une-nouvelle-loi-locale-americaine-sur-la-protection-des-mineurs",
            "claim-review": {
                "itemReviewed": {
                    "appearance": {
                        "url": " https://www.facebook.com/pretreSn/posts/pfbid05UJCY3wvHnmVKRcyx3FJHNSAwM5DH2kx5NZUAqsY32ryQPQhUQPHcCDp3XjcT6mTl",
                        "headline": "",
                    }
                }
            },
        }
    ]
}


TEST_DATA_ENRICHED = {
    "data": [
        {
            "claim-review": {
                "itemReviewed": {
                    "appearance": {
                        "@type": None,
                        "creator": {},
                        "headline": "",
                        "interactionStatistic": [],
                        "isPartOf": {"@type": "WebSite", "name": "facebook.com"},
                        "url": " "
                        "https://www.facebook.com/pretreSn/posts/pfbid05UJCY3wvHnmVKRcyx3FJHNSAwM5DH2kx5NZUAqsY32ryQPQhUQPHcCDp3XjcT6mTl",
                    }
                }
            },
            "id": "Medias/Factuel/Fact-checks/Attention-aux-mauvaises-interpretations-d-une-nouvelle-loi-locale-americaine-sur-la-protection-des-mineurs",
        }
    ]
}


if __name__ == "__main__":
    unittest.main()
