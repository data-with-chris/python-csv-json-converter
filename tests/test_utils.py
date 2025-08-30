import json

import src.file_utils as fu

import csv

import pytest


def test_read_csv(tmp_path: str) -> None:
    """
    This function tests the behavior of the CSV reader utility.

    It verifies that a well-formed CSV file is correctly read into a list of dictionaries,
    that a missing file raises a FileNotFoundError. Temporary files are used to isolate test data.

    Args:
        tmp_path: a pytest fixture providing a temporary directory for test files

    Returns:
        None
    """
    test_file = tmp_path / "test.csv"
    with open(test_file, "w", newline="") as f:
        dict_writer = csv.DictWriter(f, ["name","age"])
        dict_writer.writeheader()
        dict_writer.writerows([{"name":"John", "age": '22'}, {"name": "Alice", "age": '30'}])
    assert fu.read_csv(str(test_file)) == (
        [{"name": "John", "age": '22'}, {"name": "Alice", "age": '30'}]
    )
    with pytest.raises(FileNotFoundError):
        fu.read_csv("file_that_does_not_exist.csv")


def test_write_csv(tmp_path) -> None:
    """
    This function tests the CSV writer utility by writing data to a file and reading it back.

    It verifies that a list of dictionaries is correctly written to a CSV file and that the
    resulting file can be read back into the same structure using a CSV reader.

    Args:
        tmp_path: a pytest fixture providing a temporary directory for test files

    Returns:
        None
    """
    test_file = tmp_path / "test.csv"
    data = [{"name":"John", "age": '22'}, {"name": "Alice", "age": '30'}]
    fu.write_csv(data, str(test_file))
    with open(str(test_file), "r") as f:
        dict_reader = csv.DictReader(f)
        csv_data = [row for row in dict_reader]
        assert csv_data == data


def test_read_json(tmp_path) -> None:
    """
    This function tests the JSON reader utility with valid, missing, and malformed files.

    It confirms that a properly formatted JSON file is read correctly into a list of dictionaries,
    that attempting to read a non-existent file raises FileNotFoundError, and that
    reading a malformed JSON file raises a JSONDecodeError.

    Args:
        tmp_path: a pytest fixture providing a temporary directory for test files

    Returns:
        None
    """
    test_file = tmp_path / "test.json"
    with open(test_file, "w", newline="") as f:
        data = [{
            "name": "John",
            "age": 22},
            {"name": "Alice",
            "age": 30}]
        json.dump(data, f, indent=4)
    assert fu.read_json(str(test_file)) == data
    with pytest.raises(FileNotFoundError):
        fu.read_json("file_that_does_not_exist.json")

    error_file = tmp_path / "bad.json"
    with open(error_file, "w") as f:
        f.write('{"name": "John", "age": 22,,,}')
    with pytest.raises(json.JSONDecodeError):
        fu.read_json(str(error_file))


def test_write_json(tmp_path) -> None:
    """
    This function tests the JSON writer utility by writing data to a file and reading it back.

    It verifies that a list of dictionaries is correctly serialized to JSON format and that
    the resulting file can be read back into the same Python object using a JSON loader.

    Args:
        tmp_path: a pytest fixture providing a temporary directory for test files

    Returns:
        None
    """
    test_file = tmp_path / "test.csv"
    data = [{"name": "John", "age": 20}, {"name": "Alice", "age": 30}]
    fu.write_json(data, str(test_file))
    with open(str(test_file), "r") as f:
        test_data = json.load(f)
        assert data == test_data

