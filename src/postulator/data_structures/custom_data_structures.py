from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class SenderInfo(BaseModel):
    """Sender's information."""
    name: str = Field(..., description="Full name of the sender.")
    address: str = Field(..., description="Postal address of the sender.")
    email: str = Field(..., description="Email address of the sender.")
    phone: str = Field(..., description="Phone number of the sender.")

class RecipientInfo(BaseModel):
    """Recipient's information."""
    name: Optional[str] = Field(None, description="Name of the recipient (optional).")
    institution: str = Field(..., description="Name of the institution/company.")
    department: Optional[str] = Field(None, description="Department/division (optional).")
    address: Optional[str] = Field(None, description="Address of the institution (optional).")

class Paragraph(BaseModel):
    strategic_purpose: str = Field(..., description="Strategic purpose of the paragraph in the argumentation")
    content: str = Field(..., description="Content of the paragraph")

class LetterContent(BaseModel):
    """Content of the motivation letter."""
    formal_opening: str = Field(..., description="FORMAL OPENING")
    opening_paragraph: Paragraph = Field(..., description="OPENING PARAGRAPH. Establish relevance + last formation + overview of motivation") #Strategic purpose: Establish relevance + value proposition")
    core_paragraph_1: Paragraph = Field(..., description="CORE PARAGRAPH 1")
    core_paragraph_2: Paragraph = Field(..., description="CORE PARAGRAPH 2")
    career_decision_paragraph: Paragraph = Field(..., description="CORE PARAGRAPH 3")
    closing_paragraph: Paragraph = Field(..., description="LAST PARAGRAPH. Strategic purpose: Reinforce enthusiasm + call to action")
    formal_closing: str = Field(..., description="GRATITUDE AND AVAILABILITY")
    final_greeting: str = Field(..., description="FORMAL CLOSING")

class MotivationLetter(BaseModel):
    """Complete motivation letter model."""
    sender: SenderInfo = Field(..., description="Sender's information.")
    recipient: RecipientInfo = Field(..., description="Recipient's information.")
    subject: str = Field("Motivation letter", description="Subject of the letter.")
    content: LetterContent = Field(..., description="Content of the letter.")