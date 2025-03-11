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
    name: str = "Get human feedback and save"
    description: str = (
        "Ask the human user to give a feedback and retrieve the provided response."
        "If the human is satisfied, he can savec the letter."
    )
    args_schema: Type[BaseModel] = human_feedback_input

    def _run(self,argument:str) -> str:
        try:
            splited = argument.split("```")
            if len(splited)>3: raise
            filtered = [ string for string in splited if "json" in string]
            if len(filtered) != 1: raise
            cleaned = (filtered[0]).replace("json\n","").replace("json","")
        except:
            return(""" Remember that the tool argument should look like:
                   
Here is the draft of the motivation letter in JSON format:

```json
(put the json structure here)
```

Details about what you need the user to give a feedback about.
                   """)
        
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            #print(f"JSON parsing failed: {e}")
            #print(f"The str we tried to parse was \n {cleaned}")
            return(f"JSON parsing failed: {e}")
            # Handle error here

         # Full structure available
        json_str_propre = json.dumps(data, indent=2)

        pydantic_letter = MotivationLetter.model_validate_json( json_str_propre )

        letter_for_feedback = letter_writer._letter_for_feedback(pydantic_letter)
        latex_letter = letter_writer._letter_from_pydantic(pydantic_letter)

        print(80*"_")
        print(letter_for_feedback)
        print(80*"_")
        print(splited[-1])
        print(80*"_")
        print("Are you satisfied with the provided content?\n Type 'save' to keep the current version")
        print(80*"_")
        response = input()
        print(80*"_")

        if response == "save":
            try:
                with open("output/motivation_letter_from_tool.tex", 'w', encoding='utf-8') as file:
                    file.write(latex_letter)
                return("Your great letter was accepted by the human and successfully saved \n\n" + cleaned)
            except Exception as e:
                return(f"Error writing to file: {str(e)}")
            

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
            return(f"JSON parsing failed: {e}")
            # Handle error here
        
        # Full structure available
        json_str_propre = json.dumps(data, indent=2)

        pydantic_letter = MotivationLetter.model_validate_json( json_str_propre )

        latex_letter = self._letter_from_pydantic(pydantic_letter)

        return latex_letter

    @staticmethod
    def _letter_for_feedback(pydantic_letter: MotivationLetter) -> str:
        """Generates a motivation letter from a Pydantic model."""
        sender = pydantic_letter.sender
        recipient = pydantic_letter.recipient
        content = pydantic_letter.content

        letter = f"""
    % ========== SENDER INFO ==========
    % Strategic purpose: Professional presentation of contact details
    {sender.name} 
    {sender.address} 
    {sender.email} 
    {sender.phone} 

    % ========== RECIPIENT INFO ==========
    % Strategic purpose: Demonstrate targeted application
    {recipient.name or ''} 
    {recipient.institution}
    {recipient.department or ''} 
    {recipient.address or ''}

    % ========== SUBJECT LINE ==========
    % Strategic purpose: Immediate context setting
    {pydantic_letter.subject}

    ________________________________________________________________________

    % ========== FORMAL OPENING ==========
    {content.formal_opening}

    % ========== OPENING PARAGRAPH ==========
    % Strategic purpose: Establish relevance + value proposition
    {content.opening_paragraph}

    % ========== CORE PARAGRAPH 1 ==========
    {content.core_paragraph_1}

    % ========== CORE PARAGRAPH 2 ==========
    {content.core_paragraph_2}

    % ========== CORE PARAGRAPH 3 ==========
    {content.career_decision_paragraph}

    % ========== LAST PARAGRAPH ==========
    % Strategic purpose: Reinforce enthusiasm + call to action
    {content.closing_paragraph}

    % ========== GRATITUDE AND AVAILABILITY ==========
    {content.formal_closing}

    % ========== FORMAL CLOSING ==========
    {content.final_greeting}
    
    {sender.name}
    """
        return letter

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


import PyPDF2

class PdfReaderToolInput(BaseModel):
    """Input schema for PDF to Text conversion tool."""
    pdf_path: str = Field(..., description="Path to the PDF file to read")

class PdfReaderTool(BaseTool):
    name: str = "PDF reader"
    description: str = (
        "Read a PDF file and return its content"
    )
    args_schema: Type[BaseModel] = PdfReaderToolInput

    def _run(self, pdf_path: str) -> str:
        """Convert PDF to text with comprehensive error handling."""
        try:
            # Read PDF file
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                
                # Extract text from all pages
                text = []
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:  # Handle empty pages
                        text.append(page_text)
                
                if not text:  # Handle PDFs with no extractable text
                    return("PDF contains no extractable text (might be scanned/image-based)")
                
                return '\n'.join(text)
                
        except FileNotFoundError:
            return(f"File not found: {pdf_path}")
        except PermissionError:
            return(f"Permission denied for file: {pdf_path}")
        except PyPDF2.errors.PdfReadError:
            return("Invalid or corrupted PDF file")
        except Exception as e:
            return(f"Conversion failed: {str(e)}")


if __name__ == "__main__": 
    PdfReader = PdfReaderTool()
    #print( PdfReader._run( pdf_path="input/job_posting.pdf" ) )
    print( PdfReader._run( pdf_path="input/m2_cnn_v6_anglais.pdf" ) )