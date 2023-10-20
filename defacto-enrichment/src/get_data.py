import requests
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


def get_data(endpoint: str) -> list:
    try:
        with Progress(
            TextColumn("{task.description}"), SpinnerColumn(), TimeElapsedColumn()
        ) as progress:
            progress.add_task("[bold yellow]Exporting data from De Facto")
            response = requests.get(endpoint)
            response = response.json()
    except Exception as e:
        raise e
    else:
        if isinstance(response, dict) and response.get("data"):
            return response["data"]
        else:
            raise KeyError
