import argparse
from configparser import ConfigParser


def main():
    parser = argparse.ArgumentParser(description="Show contents of a file")
    parser.add_argument(
        "file", help="The file which needs to be shown", type=str)
    parser.add_argument("config", help="Config file", type=str)
    parser_args = parser.parse_args()

    config = ConfigParser()
    config.read(parser_args.config)
    line_numbers = config["DEFAULT"].getboolean("show_line_numbers")

    try:
        with open(parser_args.file, mode="r") as file:
            if line_numbers:
                line_count = 1
                for line in file:
                    print("{} {}".format(line_count, line))
                    line_count = line_count + 1
            else:
                for line in file:
                    print(line)
    except FileNotFoundError:
        print("Given file was not found")
    except PermissionError:
        print("No permissions to read file")


if __name__ == "__main__":
    main()
