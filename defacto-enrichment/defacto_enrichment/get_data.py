import os
from typing import Dict

import requests
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


def get_data() -> Dict:
    endpoint = os.environ["ENDPOINT"]
    try:
        with Progress(
            TextColumn("{task.description}"), SpinnerColumn(), TimeElapsedColumn()
        ) as progress:
            progress.add_task("[bold yellow]Retrieving data")
            response = requests.get(endpoint)
            response.raise_for_status()
            response = response.json()
    except Exception as e:
        raise e
    else:
        if isinstance(response, dict) and response.get("data"):
            return response
        else:
            raise KeyError
