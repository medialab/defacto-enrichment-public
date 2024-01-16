import json
import unittest
from pathlib import Path

from defacto_enrichment.main import App


class TestFlatten(unittest.TestCase):
    def setUp(self):
        self.TEST_DATA_DIR = Path(__file__).parent.joinpath("data")
        self.TEST_DATA_DIR.mkdir(exist_ok=True)
        self.TEST_MINALL_OUTPUT = Path(__file__).parent.joinpath("minall_output")
        self.TEST_MINALL_OUTPUT.mkdir(exist_ok=True)

    def test(self):
        self.app = App(data_dir=self.TEST_DATA_DIR, json_object=TEST_DATA)
        self.app.flatten_export()

    def tearDown(self) -> None:
        [file.unlink() for file in self.TEST_DATA_DIR.iterdir() if file.is_file()]
        self.TEST_DATA_DIR.rmdir()
        [file.unlink() for file in self.TEST_MINALL_OUTPUT.iterdir() if file.is_file()]
        self.TEST_MINALL_OUTPUT.rmdir()


TEST_DATA = {
    "data": [
        {
            "id": "Medias/Factuel/Fact-checks/Attention-a-ces-fausses-allegations-sur-l-UE-et-l-utilisation-du-mot-Noel-ou-des-prenoms-chretiens",
            "url": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Attention-a-ces-fausses-allegations-sur-l-UE-et-l-utilisation-du-mot-Noel-ou-des-prenoms-chretiens/",
            "channel": {
                "id": "Medias/Factuel",
                "name": "Factuel - AFP",
                "url": "https://factuel.afp.com/",
            },
            "datePublished": "2023-12-29T12:16:20+0000",
            "authors": "Marion DAUTRY / Chloé RABS / AFP Belgrade",
            "themes": ["Politique", "Société"],
            "tags": [],
            "medias": [
                {
                    "url": "https://defacto-observatoire.fr/download/Medias/Factuel/Fact-checks/Attention-a-ces-fausses-allegations-sur-l-UE-et-l-utilisation-du-mot-Noel-ou-des-prenoms-chretiens/WebHome/9c3b1920184cadfec65296b2217d0a8d5c2c440e-ipad.jpg?rev=1.1"
                }
            ],
            "claimReviews": [
                {
                    "itemReviewed": {
                        "author": {
                            "name": "Sources multiples",
                            "url": None,
                            "sameAs": None,
                            "logo": None,
                            "@type": "Person",
                        },
                        "datePublished": "2023-12-03",
                        "appearance": {
                            "url": "https://twitter.com/CH_Gallois/status/1731268150669255163"
                        },
                        "@type": "Claim",
                    },
                    "author": {
                        "name": "AFP",
                        "url": "https://factcheck.afp.com/",
                        "sameAs": "https://twitter.com/AFPFactCheck",
                        "logo": {
                            "url": "https://www.afp.com/sites/all/themes/custom/afpcom/logo.png",
                            "@type": "ImageObject",
                        },
                        "@type": "Organization",
                    },
                    "reviewRating": {
                        "ratingValue": "1",
                        "bestRating": "5",
                        "worstRating": "1",
                        "alternateName": "Faux",
                        "@type": "Rating",
                    },
                    "datePublished": "2023-12-22 03:04",
                    "url": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Attention-a-ces-fausses-allegations-sur-l-UE-et-l-utilisation-du-mot-Noel-ou-des-prenoms-chretiens/",
                    "claimReviewed": 'L\'UE veut interdire le mot "Noël" et les "prénoms chrétiens"',
                    "@context": "https://schema.org",
                    "@type": "ClaimReview",
                }
            ],
            "isBasedOnUrl": "https://factuel.afp.com/doc.afp.com.348Q2WV",
        },
        {
            "id": "Medias/20-Minutes/Fact-checks/Mais-pourquoi-autant-de-theories-du-complot-au-sujet-de-Taylor-Swift",
            "url": "https://defacto-observatoire.fr/Medias/20-Minutes/Fact-checks/Mais-pourquoi-autant-de-theories-du-complot-au-sujet-de-Taylor-Swift/",
            "channel": {
                "id": "Medias/20-Minutes",
                "name": "Fake off - 20 Minutes",
                "url": "https://www.20minutes.fr/societe/desintox/",
            },
            "datePublished": "2023-12-29T12:07:25+0000",
            "authors": "Mathilde Cousin (20 Minutes)",
            "themes": ["Société"],
            "tags": ["taylor swift", "états-unis", "musique", "théories du complot"],
            "medias": [
                {
                    "url": "https://defacto-observatoire.fr/download/Medias/20-Minutes/Fact-checks/Mais-pourquoi-autant-de-theories-du-complot-au-sujet-de-Taylor-Swift/WebHome/1200x768_une-fan-argentine?rev=1.1"
                }
            ],
            "claimReviews": [],
            "isBasedOnUrl": "https://www.20minutes.fr/arts-stars/culture/musique/4068014-20231224-pourquoi-autant-theories-complot-sujet-taylor-swift#xtor=RSS-149",
        },
        {
            "id": "Medias/Factuel/Fact-checks/Non-le-Gardasil-un-vaccin-contre-les-papillomavirus-ne-contient-pas-de-mort-au-rat",
            "url": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Non-le-Gardasil-un-vaccin-contre-les-papillomavirus-ne-contient-pas-de-mort-au-rat/",
            "channel": {
                "id": "Medias/Factuel",
                "name": "Factuel - AFP",
                "url": "https://factuel.afp.com/",
            },
            "datePublished": "2023-11-28T09:35:10+0000",
            "authors": "AFP France",
            "themes": ["Santé", "Science"],
            "tags": ["Sante"],
            "medias": [
                {
                    "url": "https://defacto-observatoire.fr/download/Medias/Factuel/Fact-checks/Non-le-Gardasil-un-vaccin-contre-les-papillomavirus-ne-contient-pas-de-mort-au-rat/WebHome/d89bd59860a8a6b8ae9ddd29757cfbce143fef9a-ipad.jpg?rev=1.1"
                }
            ],
            "claimReviews": [
                {
                    "itemReviewed": {
                        "author": {
                            "name": "sources multiples",
                            "url": None,
                            "sameAs": None,
                            "logo": None,
                            "@type": "Person",
                        },
                        "datePublished": "2023-11-22",
                        "appearance": {
                            "url": "https://www.facebook.com/marylene.ditmylene/posts/pfbid02QWK5A39qmvnknJW1G9HEa13EFrsTuQnPVmaW2SKvR323bcn5sTCi87T16KukqTdsl"
                        },
                        "@type": "Claim",
                    },
                    "author": {
                        "name": "AFP",
                        "url": "https://factcheck.afp.com/",
                        "sameAs": "https://twitter.com/AFPFactCheck",
                        "logo": {
                            "url": "https://www.afp.com/sites/all/themes/custom/afpcom/logo.png",
                            "@type": "ImageObject",
                        },
                        "@type": "Organization",
                    },
                    "reviewRating": {
                        "ratingValue": "1",
                        "bestRating": "5",
                        "worstRating": "1",
                        "alternateName": "Faux",
                        "@type": "Rating",
                    },
                    "datePublished": "2023-11-28 08:27",
                    "url": "",
                    "claimReviewed": "Le vaccin Gardasil contient de la mort aux rats et tue des jeunes filles",
                    "@context": "https://schema.org",
                    "@type": "ClaimReview",
                },
                {
                    "itemReviewed": {
                        "author": {
                            "name": "multiples",
                            "url": None,
                            "sameAs": None,
                            "logo": None,
                            "@type": "Person",
                        },
                        "datePublished": "2023-10-12",
                        "appearance": {
                            "url": "https://www.facebook.com/groups/958321254610945/posts/1750528682056861/"
                        },
                        "@type": "Claim",
                    },
                    "author": {
                        "name": "AFP",
                        "url": "https://factcheck.afp.com/",
                        "sameAs": "https://twitter.com/AFPFactCheck",
                        "logo": {
                            "url": "https://www.afp.com/sites/all/themes/custom/afpcom/logo.png",
                            "@type": "ImageObject",
                        },
                        "@type": "Organization",
                    },
                    "reviewRating": {
                        "ratingValue": "1",
                        "bestRating": "5",
                        "worstRating": "1",
                        "alternateName": "faux",
                        "@type": "Rating",
                    },
                    "datePublished": "2023-11-28 08:27",
                    "url": "",
                    "claimReviewed": "Il y a de la mort aux rats dans le Gardasil, un vaccin très dangereux",
                    "@context": "https://schema.org",
                    "@type": "ClaimReview",
                },
            ],
            "isBasedOnUrl": "https://factuel.afp.com/doc.afp.com.34643H9",
        },
    ]
}


if __name__ == "__main__":
    unittest.main()
