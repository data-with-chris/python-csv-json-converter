import sys

import json

import csv

from src import file_utils as fu

def main() -> None:
    """
    Entry point for the program. Accepts a filename and the desired conversion
    format as command-line arguments.

    The converted file is saved to the same directory the program was run
    from. If an error occurs, an appropriate message is displayed
    and the program exits.

    Returns:
        None
    """
    if len(sys.argv) < 3:
        sys.exit("Usage: python main.py <filename> <csv/json>")
    try:
        filename = sys.argv[1]
        output_as = sys.argv[2]
        fu.convert_file(filename, output_as)
    except FileNotFoundError as e:
        sys.exit(f"File not found: {e}")
    except json.decoder.JSONDecodeError as e:
        sys.exit(f"JSON decode error: {e}")
    except csv.Error as e:
        sys.exit(f"csv error: {e}")
    except Exception as e:
        sys.exit(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()