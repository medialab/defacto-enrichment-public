import json
import unittest
from pathlib import Path
from typing import List

from defacto_enrichment.main import App


class TestRebuild(unittest.TestCase):
    def setUp(self):
        self.TEST_DATA_DIR = Path(__file__).parent.joinpath("data")
        self.TEST_DATA_DIR.mkdir(exist_ok=True)
        self.TEST_MINALL_OUTPUT = Path(__file__).parent.joinpath("minall_output")
        self.TEST_MINALL_OUTPUT.mkdir(exist_ok=True)

    def test_identical_json_object(self) -> None:
        input = {"data": TEST_DATA_IDENTICAL["input"]}
        self.app = App(data_dir=self.TEST_DATA_DIR, json_object=input)
        self.app.flatten_export()
        self.app.rebuild_export()
        with open(self.app.new_export_json) as f:
            new_export = json.load(f)
        expected_output = {"data": TEST_DATA_IDENTICAL["output"]}
        self.assertEquals(new_export, expected_output)

    def test_different_json_objects(self) -> None:
        self.app = App(data_dir=self.TEST_DATA_DIR, json_object=TEST_DATA_ENRICHED)
        self.app.flatten_export()
        self.app.enrichment(
            config={},
            minall_output=self.TEST_MINALL_OUTPUT,
        )
        self.app.rebuild_export()
        original_export = self.app.json_data_original_copy
        with open(self.app.new_export_json) as f:
            new_export = json.load(f)
        self.assertNotEquals(original_export, new_export)

    def test_different_input_formats(self) -> None:
        self.app = App(data_dir=self.TEST_DATA_DIR, json_object=TEST_DATA_DIFF_FORMATS)
        self.app.flatten_export()
        self.app.rebuild_export()
        with open(self.app.new_export_json) as f:
            new_export = json.load(f)
        for fact_check in new_export["data"]:
            self.assertIsInstance(fact_check["claim-review"], List)

            # Check dict format
            new_appearance_url = new_export["data"][0]["claim-review"][0][
                "itemReviewed"
            ]["appearance"]["url"]
            old_appearance_url = (
                "https://twitter.com/CH_Gallois/status/1731268150669255163"
            )
            self.assertEquals(new_appearance_url, old_appearance_url)

            # Check string format
            new_appearance_url = new_export["data"][1]["claim-review"]
            self.assertEquals(new_appearance_url, [])

            # Check list format
            new_appearance_url = new_export["data"][2]["claim-review"][0][
                "itemReviewed"
            ]["appearance"]["url"]
            old_appearance_url = "https://www.facebook.com/marylene.ditmylene/posts/pfbid02QWK5A39qmvnknJW1G9HEa13EFrsTuQnPVmaW2SKvR323bcn5sTCi87T16KukqTdsl"
            self.assertEquals(new_appearance_url, old_appearance_url)

    def tearDown(self) -> None:
        [file.unlink() for file in self.TEST_DATA_DIR.iterdir() if file.is_file()]
        self.TEST_DATA_DIR.rmdir()
        [file.unlink() for file in self.TEST_MINALL_OUTPUT.iterdir() if file.is_file()]
        self.TEST_MINALL_OUTPUT.rmdir()


TEST_DATA_IDENTICAL = {
    "input": [
        {
            "id": "Medias/Factuel/Fact-checks/Attention-aux-mauvaises-interpretations-d-une-nouvelle-loi-locale-americaine-sur-la-protection-des-mineurs",
            "claim-review": [
                {
                    "itemReviewed": {
                        "appearance": [
                            {
                                "url": "https://www.facebook.com/pretreSn/posts/pfbid05UJCY3wvHnmVKRcyx3FJHNSAwM5DH2kx5NZUAqsY32ryQPQhUQPHcCDp3XjcT6mTl",
                            },
                        ]
                    }
                },
            ],
        },
    ],
    "output": [
        {
            "id": "Medias/Factuel/Fact-checks/Attention-aux-mauvaises-interpretations-d-une-nouvelle-loi-locale-americaine-sur-la-protection-des-mineurs",
            "claim-review": [
                {
                    "itemReviewed": {
                        "appearance": [
                            {
                                "url": "https://www.facebook.com/pretreSn/posts/pfbid05UJCY3wvHnmVKRcyx3FJHNSAwM5DH2kx5NZUAqsY32ryQPQhUQPHcCDp3XjcT6mTl",
                                "@type": None,
                                "isPartOf": {"@type": "WebSite", "name": None},
                                "creator": {},
                                "interactionStatistic": [],
                            }
                        ]
                    }
                }
            ],
        }
    ],
}


TEST_DATA_ENRICHED = {
    "data": [
        {
            "id": "Medias/Factuel/Fact-checks/Attention-aux-mauvaises-interpretations-d-une-nouvelle-loi-locale-americaine-sur-la-protection-des-mineurs",
            "claim-review": [
                {
                    "itemReviewed": {
                        "appearance": {
                            "@type": None,
                            "creator": {},
                            "headline": "",
                            "interactionStatistic": [],
                            "isPartOf": {"@type": "WebSite", "name": "facebook.com"},
                            "url": "https://www.facebook.com/pretreSn/posts/pfbid05UJCY3wvHnmVKRcyx3FJHNSAwM5DH2kx5NZUAqsY32ryQPQhUQPHcCDp3XjcT6mTl",
                        }
                    },
                }
            ],
        }
    ]
}

TEST_DATA_DIFF_FORMATS = {
    "data": [
        {
            "id": "Medias/Factuel/Fact-checks/Attention-aux-mauvaises-interpretations-d-une-nouvelle-loi-locale-americaine-sur-la-protection-des-mineurs",
            "claim-review": {
                "itemReviewed": {
                    "appearance": {
                        "url": "https://twitter.com/CH_Gallois/status/1731268150669255163"
                    },
                }
            },
        },
        {
            "id": "Medias/20-Minutes/Fact-checks/Mais-pourquoi-autant-de-theories-du-complot-au-sujet-de-Taylor-Swift",
            "claim-review": "",
        },
        {
            "id": "Medias/Factuel/Fact-checks/Non-le-Gardasil-un-vaccin-contre-les-papillomavirus-ne-contient-pas-de-mort-au-rat",
            "claim-review": [
                {
                    "itemReviewed": {
                        "appearance": "https://www.facebook.com/marylene.ditmylene/posts/pfbid02QWK5A39qmvnknJW1G9HEa13EFrsTuQnPVmaW2SKvR323bcn5sTCi87T16KukqTdsl",
                    },
                },
                {
                    "itemReviewed": {
                        "appearance": "https://www.facebook.com/groups/958321254610945/posts/1750528682056861/",
                    },
                },
            ],
        },
    ]
}


if __name__ == "__main__":
    unittest.main()
