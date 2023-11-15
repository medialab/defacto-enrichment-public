import sqlite3
from pathlib import Path

from src.compiler import Compiler

TEMP_DIR = Path(__file__).parent.joinpath("tmp")
TEMP_APPEARANCES = TEMP_DIR.joinpath("appearances.csv")
TEMP_FACT_CHECKS = TEMP_DIR.joinpath("fact_checks.csv")
TEMP_SHARED_CONTENT = TEMP_DIR.joinpath("shared_content.csv")
DB = TEMP_DIR.joinpath("sqlite.db")


def combine_files(directory: str, output: str):
    # Set up
    connection = sqlite3.connect(DB)
    compiler = Compiler(connection)

    # Combine files
    for file in Path(directory).iterdir():
        print("\n", file)
        # call Compiler -> flatten -> coalesce
        compiler(file)

    # Write final CSV files to output directory
    output_dir = Path(output)
    output_dir.mkdir(exist_ok=True)
    TEMP_FACT_CHECKS.rename(output_dir.joinpath("fact_checks.csv"))
    TEMP_APPEARANCES.rename(output_dir.joinpath("appearances.csv"))
    TEMP_SHARED_CONTENT.rename(output_dir.joinpath("shared_content.csv"))
