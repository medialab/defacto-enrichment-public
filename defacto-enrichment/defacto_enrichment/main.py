# defacto_enrichment/main.py

"""Module contains class and functions to run the full Defacto-Enrichment workflow.

Exportable modules:

- `App`: Class, which can be initiated with just an output directory and a JSON array, and whose methods can run the entire workflow.
- `main`: Function that retrieves the JSON data, initializes the Minall class, and calls the workflow's methods.

"""

import copy
import json
from pathlib import Path
from typing import Dict, List, Tuple

from defacto_enrichment.constants import DATA_DIR, MINALL_OUTPUT
from defacto_enrichment.flatten import flatten
from defacto_enrichment.get_data import parse_input_data
from defacto_enrichment.rebuild import rebuild
from minall.main import Minall  # type: ignore
from rich import print
from rich.panel import Panel


class App:
    """Intake data, run enrichment, output linked data in 2 CSV files."""

    def __init__(
        self,
        json_object: Dict,
        data_dir: Path = DATA_DIR,
    ) -> None:
        """Prepare the Minall application.

        Register the original JSON object (not JSON array) and the desired output directory. Parse the data items in the JSON object's key "data." Set up the out-files for the 3 types of linked data: fact-checks, appearances, and appearances' shared content.

        Args:
            json_object (Path | None, optional): Path to JSON export of RSS feed. Defaults to None.
            data_dir (Path, optional): Path to directory for enriched CSV files. Defaults to DATA_DIR.
        """

        # Parse JSON export of RSS feed
        self.json_data = json_object
        self.json_data_original_copy = copy.deepcopy(json_object)
        self.data_items = json_object["data"]

        # Manage file paths
        self.appearance_csv = data_dir.joinpath("appearances.csv")
        self.shared_content_csv = data_dir.joinpath("shared_content.csv")
        self.fact_check_csv = data_dir.joinpath("fact_checks.csv")
        self.new_export_json = data_dir.joinpath("enriched-urls.json")

    def flatten_export(self):
        """Flatten array of fact-check articles into 3 CSV files."""

        flatten(
            appearance_file=self.appearance_csv,
            fact_check_file=self.fact_check_csv,
            content_file=self.shared_content_csv,
            data=self.data_items,
        )

    def enrichment(
        self,
        config: str | Dict | None = None,
        with_shared_content_file: bool = True,
        minall_output: Path = MINALL_OUTPUT,
    ):
        """Enrich the flattened CSV files with an instance of the Minall app.

        Args:
            config (str | Dict | None, optional): Minet config in YAML file (str), in parsed object (Dict), or in environment variables (None). Defaults to None.
            with_shared_content_file (bool, optional): Whether to attempt colleciton of shared content. Defaults to True.
            minall_output (Path, optional): Directory for enriched CSV files. Defaults to MINALL_OUTPUT.
        """

        if with_shared_content_file:
            shared_content_file = str(self.shared_content_csv)
        else:
            shared_content_file = None

        # ---------- APPEARANCE ENRICHMENT ------------ #
        minall = Minall(
            database=None,
            config=config,
            output_dir=str(minall_output),
            links_file=str(self.appearance_csv),
            url_col="clean_url",
            shared_content_file=shared_content_file,
            buzzsumo_only=False,
        )
        minall.collect_and_coalesce()
        appearance_file, shared_content_file = minall.export()
        print_panel_indicating_file(
            files=[
                (appearance_file, self.appearance_csv),
                (shared_content_file, self.shared_content_csv),
            ]
        )
        appearance_file.rename(self.appearance_csv)
        shared_content_file.rename(self.shared_content_csv)

        # ----------- FACT CHECK ENRICHMENT ----------- #
        minall = Minall(
            database=None,
            config=config,
            output_dir=str(minall_output),
            links_file=str(self.fact_check_csv),
            url_col="clean_url",
            shared_content_file=None,
            buzzsumo_only=True,
        )
        minall.collect_and_coalesce()
        fact_check_file, _ = minall.export()
        print_panel_indicating_file(files=[(fact_check_file, self.fact_check_csv)])
        fact_check_file.rename(self.fact_check_csv)

    def rebuild_export(self):
        """Rebuild the full, original JSON object from data Minall wrote to the enriched CSV files."""
        # Use normalized data when rebuilding
        self.json_data["data"] = self.data_items
        rebuild(
            database_export=self.json_data,
            appearances_csv=self.appearance_csv,
            shared_content_csv=self.shared_content_csv,
            fact_check_csv=self.fact_check_csv,
        )
        with open(self.new_export_json, "w") as f:
            json.dump(self.json_data, f, indent=4, ensure_ascii=False)


def print_panel_indicating_file(files: List[Tuple[Path, Path]]):
    panel_text = "\n".join(
        f"{t[0].relative_to(Path.cwd())} -> {t[1].relative_to(Path.cwd())}"
        for t in files
    )
    print(Panel(panel_text, title="Rewriting minall enrichment to out-file"))


def main():
    """Main function to intake ClaimReview data and run the enrichment workflow."""
    # Parse input data
    database_export = parse_input_data()

    if database_export:
        # Initialize the app with the data and file paths
        app = App(json_object=database_export)

        # Run the app's 3 steps
        app.flatten_export()
        app.enrichment()
        app.rebuild_export()


if __name__ == "__main__":
    main()
