"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from pydantic_ai import Agent, TextContent
from pydantic_ai.models import Model

from infrastructure.adapter.external.study_program_agent_parser.output import (
    StudyProgramOutput,
)


class PydanticAiStudyProgramAgentParser:
    """
    Agent parser implementation using PydanticAI.
    """

    __SYSTEM_PROMPT = """
        You are an expert system for extracting structured data from text documents. Your current context domain is educational and institutional documents from Chile.

        Important Note: The input documents you will process are written in Spanish. You must process the Spanish text and extract it exactly as written.

        Your goal is to analyze the provided text (in Markdown format) and precisely extract the necessary information to fulfill the required output data schema.

        Operating Guidelines:
        1. Literal Extraction: Extract the information faithfully to the original text. Do not summarize, interpret, or invent content.
        2. Schema Adaptability: Identify and extract any entity, list, or field requested by the output schema, looking for its logical correspondence within the document's structure.
        3. Missing Data: If the document does not contain information for a specific field in the schema, omit it, return a null value (`null`), or an empty list (`[]`), depending on the data type.
        4. Strict Output: Generate strictly the required data structure. Do not include introductory text, explanations, or markdown formatting tags outside the resulting JSON.
    """

    __USER_PROMPT = """
        Analyze the following document (written in Spanish) and extract the required information according to the configured output schema.
    """

    def __init__(self, model: Model):
        self.agent = Agent(
            model,
            output_type=StudyProgramOutput,
            system_prompt=PydanticAiStudyProgramAgentParser.__SYSTEM_PROMPT,
        )

    async def run(self, content: str) -> StudyProgramOutput:
        """
        Run the agent asynchronously with the given prompt.
        """
        result = await self.agent.run(
            [
                PydanticAiStudyProgramAgentParser.__USER_PROMPT,
                TextContent(
                    content=content,
                    metadata={"source": "program.md"},
                ),
            ]
        )
        return result.output
