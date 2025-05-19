import os
import sys
from config.env_config import setup_env
from etl.extract.extract import main as extract_main
from etl.transform.transform import main as transform_main


def main():
    run_env_setup()

    print("Extracting data...")
    extract_main()
    print("Data extraction complete.")

    print("Transforming data...")
    transform_main()
    print("Data transformation complete.")

    print(
        f"ETL pipeline run successfully in "
        f'{os.getenv("ENV", "error")} environment!'
    )


def run_env_setup():
    print("Setting up environment...")
    setup_env(sys.argv)
    print("Environment setup complete.")


if __name__ == "__main__":
    main()
