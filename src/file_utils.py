import csv

import json

from pathlib import Path

def read_csv(filename: str) -> list[dict[str, str]]:
    """
    This function reads a CSV file and returns it as a list of dictionaries.

    Each key is a column header, and each row value is a string. A context manager
    is used to safely open and close the file.

    Args:
        filename: the name of the CSV file

    Returns:
        A list of dictionaries representing the rows in the csv file.
    """
    with open(filename, "r", encoding="utf-8", newline="") as csv_file:
        dict_reader = csv.DictReader(csv_file)
        return [row for row in dict_reader]


def read_json(filename: str) -> list[dict[str, str]]:
    """
    This function reads a JSON file and returns it as a list of dictionaries.

    Assuming the file contains an array of JSON objects. Each object converted to a
    dictionary and key/value pairs are retained. A context manager is used
    to safely open and close the file.

    Args:
        filename: the name of the JSON file

    Returns:
        A list of dictionaries representing each JSON object in the file.
    """
    with open(filename, "r") as json_file:
        return json.loads(json_file.read())


def convert_file(filename: str, output_format: str) -> None:
    """
    Converts a CSV file to JSON, or a JSON file to CSV.

    The file to convert and selected output are checked to ensure the
    correct conversion functions are called.

    The function checks the current file format and calls the appropriate
    conversion function. If the input file format and the desired output
    format are the same, no action is taken. If the output format is invalid,
    a ValueError is raised.

    Args:
        filename: the name of the file to convert.
        output_format: the format to convert the file to.

    Returns:
        None
    """
    file = Path(filename)
    output_format = output_format.lower().lstrip(".")
    if file.suffix == ".json" and output_format == "csv":
        write_csv(read_json(filename), file.with_suffix('.csv').name)
    elif file.suffix == ".csv" and output_format == "json":
        write_json(read_csv(filename), file.with_suffix('.json').name)
    elif file.suffix[1:] == output_format:
        pass
    else:
        raise ValueError(f"{output_format} is not supported.")


def write_csv(data: list[dict[str, str]], outfile: str) -> None:
    """
    This functions writes a list of dictionaries to a CSV file.

    The dictionary keys are used as column headers, and each value
    is converted to a row of comma separated values.

    Args:
        data: the list of dictionaries to write to the CSV file.
        outfile: the name of the file to write to. A context manager
        is used to safely open and close the file.

    Returns:
        None
    """
    with open(outfile, "w", encoding="utf-8", newline="") as csv_file:
        write = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        write.writeheader()
        write.writerows(data)


def write_json(data: list[dict[str, str]], outfile: str) -> None:
    """
    This functions writes a list of dictionaries to a JSON file.

    The list of dictionaries is converted to an array of JSON objects,
    key/value pairs are retained. A context manager is used to safely
    open and close the file.

    Args:
        data: the list of dictionaries to write to the JSON file.
        outfile: the name of the file to write to.

    Returns:
        None
    """
    with open(outfile, "w") as json_file:
        json.dump(data, json_file, indent=4)