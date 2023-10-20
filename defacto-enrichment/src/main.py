import json

from src.cleanup import cleanup
from src.flatten_json import flatten_all_the_exported_data
from src.get_data import get_data
from src.load_env_var import load_environment_variables
from src.update_metadata import update_metadata


def main():
    endpoint = load_environment_variables()

    # Export new data from the database
    exported_data = get_data(endpoint=endpoint)

    # Flatten the data into CSV files
    flatten_all_the_exported_data(data=exported_data)

    # Feed the flattened files to minet / minall
    update_metadata()

    # Delete temp files
    cleanup()

    # Save in ./data some information relevant to later analyses
    with open("./data/fact-check_info.json", "w") as of:
        info = {
            fc["id"]: {
                "date": fc.get("published"),
                "rating": fc.get("claim-review", {}).get("reviewRating"),
            }
            for fc in exported_data
            if fc.get("claim-review")
        }
        json.dump(info, of, indent=4)


if __name__ == "__main__":
    main()
