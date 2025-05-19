from etl.transform.transform_from_json import main as transform_main
from etl.transform.transform_clean import main as clean_main
from etl.transform.transform_for_visualisation import main as vs_main


# Main function for transform
def main():
    transform_main()
    clean_main()
    vs_main()


if __name__ == "__main__":
    main()
