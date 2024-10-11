from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class Summary(BaseModel):
    summary: str = Field(description="Summary of Profile")
    facts: List[str] = Field(description="Interesting Facts of Profile")

    def to_dict(self):
        return {"summary": self.summary, "facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)