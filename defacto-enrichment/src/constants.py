from pathlib import Path

CONFIG = Path.cwd().joinpath("config.json")

DATA_DIR = Path.cwd().joinpath("data")
DATA_DIR.mkdir(exist_ok=True)

MINALL_OUTPUT = DATA_DIR.joinpath("minall-output")
