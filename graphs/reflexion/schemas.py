from typing import List

from pydantic import BaseModel, Field


class Reflection(BaseModel):
    missing: str = Field(
        description="Identify key information, concepts, or context that should be added to make the answer more complete and accurate."
    )
    superfluous: str = Field(
        description="Identify any unnecessary, redundant, or off-topic information that could be removed without affecting the answer's quality."
    )


class AnswerQuestion(BaseModel):
    """Answer the question and reflect on the answer."""

    answer: str = Field(
        description="Provide a comprehensive, well-structured answer in approximately 250 words. Focus on accuracy, clarity, and relevance to the question."
    )
    reflection: Reflection = Field(
        description="Self-evaluate the answer by analyzing its completeness and conciseness."
    )
    search_queries: List[str] = Field(
        description="Generate 1-3 specific search queries that would help find information to address the identified gaps in the answer. Each query should target missing key information."
    )


class ReviseAnswer(AnswerQuestion):
    """Revise the answer based on the critique and search queries."""

    references: List[str] = Field(
        description="List the sources used to gather information for the revised answer. Each reference should be a numerical citation followed by a URL or other relevant source identifier."
    )
