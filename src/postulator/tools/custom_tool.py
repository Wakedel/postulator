from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field, PrivateAttr


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="The short question the user will answer")

class ask_human(BaseTool):
    name: str = "Ask human"
    description: str = (
        "Ask a question to the human user and retrieve the provided response."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        print(80*"_")
        print(argument)
        print(80*"_")
        response = input("Your answer:\n")
        print(80*"_")
        return response
    
class human_feedback_input(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="The draft of the letter") #"What you need a feedback about and the draft")

class human_feedback(BaseTool):
    name: str = "Get human feedback"
    description: str = (
        "Ask the human user to give a feedback and retrieve the provided response."
    )
    args_schema: Type[BaseModel] = human_feedback_input

    def _run(self,argument:str) -> str:
        # Implementation goes here
        print(80*"_")
        print(argument)
        print(80*"_")
        response = input("Are you satisfied with the provided content?\n")
        print(80*"_")
        return response

class cleaner_input(BaseModel):
    """Input schema for MyCustomTool."""
    text: str = Field(..., description="Your final answer.")


class final_response_cleaner(BaseTool):
    """Tool to clean the agent's final output by removing specified strings."""
    name: str = "Final answer cleaner"
    description: str = "Make sure the final output match the expected format."
    args_schema: Type[BaseModel] = cleaner_input

    # Private attributes (not part of the schema)
    _strings_to_remove: List[str] = PrivateAttr()

    def __init__(self, strings_to_remove: List[str] = [], result_as_answer=False):
        """
        Initializes the CleanAgentOutputTool.

        Args:
            strings_to_remove: A list of strings to remove from the agent's output.
        """
        super().__init__(result_as_answer=result_as_answer)#result_as_answer=result_as_answer)
        self._strings_to_remove = strings_to_remove

    def _run(self, text: str) -> str:
        """
        Cleans the given text by removing the specified strings.

        Args:
            text: The agent's final output text.

        Returns:
            The cleaned text.
        """
        for string_to_remove in self._strings_to_remove:
            text = text.replace(string_to_remove, "")
        return text


class letter_input(BaseModel):
    """Input schema for MyCustomTool."""
    text: str = Field(..., description="The letter in a structured JSON format matching the provided schema.")

import json
from src.postulator.data_structures.custom_data_structures import MotivationLetter

class letter_writer(BaseTool):
    """Tool to clean the agent's final output and write the letter."""
    name: str = "Beautiful letter"
    description: str = "Produce a beautiful letter from your final output."
    args_schema: Type[BaseModel] = cleaner_input

    # Private attributes (not part of the schema)
    _strings_to_remove: List[str] = PrivateAttr()

    def __init__(self, strings_to_remove: List[str] = ['```json\n', '```', '```json'], result_as_answer=True):
        super().__init__(result_as_answer=result_as_answer)#result_as_answer=result_as_answer)
        self._strings_to_remove = strings_to_remove

    def _run(self, text: str) -> str:
        
        # clean the output
        for string_to_remove in self._strings_to_remove:
            text = text.replace(string_to_remove, "")

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {e}")
            print(f"The str we tried to parse was \n {text}")
            # Handle error here
        
        # Full structure available
        json_str_propre = json.dumps(data, indent=2)

        pydantic_letter = MotivationLetter.model_validate_json( json_str_propre )

        latex_letter = self._letter_from_pydantic(pydantic_letter)

        return latex_letter

    @staticmethod
    def _letter_from_pydantic(pydantic_letter: MotivationLetter) -> str:
        """Generates a motivation letter from a Pydantic model."""
        sender = pydantic_letter.sender
        recipient = pydantic_letter.recipient
        content = pydantic_letter.content

        letter = f"""
    \\documentclass[11pt]{{letter}}
    \\usepackage[a4paper, top=25mm, bottom=25mm, left=25mm, right=25mm]{{geometry}}
    \\linespread{{1}}

    \\begin{{document}}
    \\thispagestyle{{empty}}

    % ========== SENDER INFO ==========
    % Strategic purpose: Professional presentation of contact details
    \\hfill {sender.name}\\\\
    \\strut\\hfill {sender.address}\\\\
    \\strut\\hfill {sender.email}\\\\
    \\strut\\hfill {sender.phone}

    % ========== RECIPIENT INFO ==========
    % Strategic purpose: Demonstrate targeted application
    \\vspace{{0.15cm}}
    {recipient.name or ''} \\\\
    {recipient.institution} \\\\
    {recipient.department or ''} \\\\
    {recipient.address or ''}

    % ========== DATE ==========
    \\vspace{{0.15cm}}
    \\hfill \\today

    % ========== SUBJECT LINE ==========
    % Strategic purpose: Immediate context setting
    \\vspace{{0.5cm}}
    \\begin{{large}}
    \\textbf{{{pydantic_letter.subject}}}
    \\end{{large}}

    \\vspace{{0.15cm}}
    \\hrule
    \\vspace{{0.5cm}}

    % ========== FORMAL OPENING ==========
    {content.formal_opening}\\vspace{{0.15cm}}

    % ========== OPENING PARAGRAPH ==========
    % Strategic purpose: Establish relevance + value proposition
    {content.opening_paragraph}

    % ========== CORE PARAGRAPH 1 ==========
    % Strategic purpose: Demonstrate expertise through academic progression
    {content.core_paragraph_1}

    % ========== CORE PARAGRAPH 2 ==========
    % Strategic purpose: Show focused specialization + technical capabilities
    {content.core_paragraph_2}

    % ========== CAREER DECISION PARAGRAPH ==========
    % Strategic purpose: Address potential concerns + show commitment
    {content.career_decision_paragraph}

    % ========== CLOSING PARAGRAPH ==========
    % Strategic purpose: Reinforce enthusiasm + call to action
    {content.closing_paragraph}

    % ========== FORMAL CLOSING ==========
    {content.formal_closing}
    \\vspace{{0.15cm}}

    {content.final_greeting}
    \\vspace{{1cm}}\\\\
    {sender.name}
    \\end{{document}}
    """
        return letter