"""Classes and types used throughout the project."""

from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel

from src.text_utils import indent

section_text = list[str]
multisection_text = dict[str, list[str]]


class SummarizationMethod(Enum):
    """Available summarization method."""

    TEXTRANK = "TEXTRANK"
    BART = "BART"
    GPT3 = "GPT3"


class SummarizationConfiguration(BaseModel):
    """Configuration for a summarization."""

    method: SummarizationMethod
    config_kwargs: Optional[dict[str, Union[float, str, bool]]] = None


class ScientificArticleText(BaseModel):
    """Organized text of a scientific article."""

    Abstract: section_text
    Introduction: section_text
    Methods: multisection_text
    Results: multisection_text
    Discussion: section_text

    def __str__(self) -> str:
        """Get a string representation of the scientific article text."""
        msg = f"Abstract: {len(self.Abstract)} paragraph(s)\n"
        msg += f"Introduction: {len(self.Introduction)} paragraph\n"
        msg += f"Methods: {len(self.Methods)} sections\n"
        msg += f"Results: {len(self.Results)} sections\n"
        msg += f"Discussion: {len(self.Discussion)} paragraph(s)"
        return msg

    def __repr__(self) -> str:
        """Get a string representation of the scientific article text."""
        return str(self)


class ScientificArticle(BaseModel):
    """Scientific article."""

    title: str
    url: str
    text: ScientificArticleText

    def __str__(self) -> str:
        """Get a string representation of the scientific article."""
        msg = self.title + "\n"
        msg += f"(url: {self.url})\n"
        msg += indent(str(self.text))
        return msg

    def __repr__(self) -> str:
        """Get a string representation of the scientific article."""
        return str(self)


class SummarizedScientificArticle(ScientificArticle):
    """The results of summarizing an article."""

    config: SummarizationConfiguration
    summary: ScientificArticleText

    def __str__(self) -> str:
        """Get a string representation of the scientific article summary."""
        msg = self.title + "\n"
        msg += f"(url: {self.url})\n"
        msg += "\n"
        msg += " Original text:\n"
        msg += indent(str(self.text))
        msg += "\n"
        msg += " Summarized text:\n"
        msg += indent(str(self.summary))

        return msg

    def __repr__(self) -> str:
        """Get a string representation of the scientific article summary."""
        return str(self)
