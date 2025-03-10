#!/usr/bin/env python
import sys
import warnings
import json

from datetime import datetime

from postulator.crew import Postulator

from postulator.utils import load_config

from src.postulator.data_structures.custom_data_structures import MotivationLetter

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

"""
import litellm
litellm._turn_on_debug()
"""

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """

    # job_posting : either "url:http..." or "file:postulator/path"
    # personal_writeup : a string giving hopefully usefull information for the current application

    inputs = load_config("config.json")
    inputs["schema"] = json.dumps( MotivationLetter.model_json_schema() )
    
    try:
        Postulator().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "job_posting": "", # either "url:http..." or "file:postulator/path",
        "personal_writeup" : ""
    }
    try:
        Postulator().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Postulator().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Postulator().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
