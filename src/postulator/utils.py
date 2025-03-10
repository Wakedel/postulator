import json
from pathlib import Path
from typing import Dict, Any

import json
from pydantic import ValidationError
import requests
import time

def save_json_to_file(json_data, file_path):
    """
    Save a JSON object to a file.

    :param json_data: The JSON object to save.
    :param file_path: The path to the file where the JSON object will be saved.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        print(f"JSON data successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the JSON data: {e}")
        

def read_json_from_file(file_path):
    """
    Read a JSON file and return its contents as a Python dictionary.

    :param file_path: The path to the JSON file to read.
    :return: The contents of the JSON file as a Python dictionary.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        print(f"JSON data successfully read from {file_path}")
        return data
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"The file {file_path} is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred while reading the JSON file: {e}")


def load_json_into_pydantic(file_path, model):
    """
    Load a JSON file and parse it into a Pydantic model.

    :param file_path: The path to the JSON file to read.
    :param model: The Pydantic model to parse the JSON data into.
    :return: An instance of the Pydantic model with the JSON data.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        print(f"JSON data successfully read from {file_path}")

        # Parse the JSON data into the Pydantic model
        pydantic_object = model(**data)
        print("JSON data successfully loaded into Pydantic model")
        return pydantic_object
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"The file {file_path} is not a valid JSON file.")
    except ValidationError as e:
        print(f"Validation error while parsing JSON data: {e}")
    except Exception as e:
        print(f"An error occurred while reading the JSON file: {e}")


def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration inputs from a JSON file
    
    Args:
        config_path: Path to config file (default: config.json)
    
    Returns:
        Dictionary with configuration inputs
    
    Raises:
        FileNotFoundError: If config file is missing
        JSONDecodeError: If config file is invalid
    """
    path = Path(config_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {path.resolve()}")
    
    with open(path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config