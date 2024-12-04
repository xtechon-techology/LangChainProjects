# from typing import List, Dict, Any
# from langchain.output_parsers import PydanticOutputParser
#
# from pydantic import BaseModel, Field
# from typing import List, Dict, Any
#
# class Summary(BaseModel):
#     summary: str = Field(description="summary")
#     facts: List[str] = Field(description="interesting facts about them")
#
#     def to_dict(self) -> Dict[str, Any]:
#         return {"summary": self.summary, "facts": self.facts}
#
#
# summary_parser = PydanticOutputParser(pydantic_object=Summary)

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Any, Dict


class Summary(BaseModel):
    summary: str
    facts: List[str]


# Create parser for Summary
summary_parser = PydanticOutputParser(pydantic_object=Summary)

# Test it
output_data = Summary(summary="Test Summary", facts=["Fact 1", "Fact 2"])
print(output_data.dict())
