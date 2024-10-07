from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    Error: str

class SQLParserInput(BaseModel):
    sql: str


class SQLParser_old(BaseModel):
    query: str
    dq_dimensions: list
    dq_measures: list
    rule: str

class SQLParser(BaseModel):
    query: Optional[str]
    dq_dimensions: list
    dq_measures: list
    rule_function: Optional[str]
    rule_measure: Optional[str]
    rule_condition: Optional[str]
    rule_threshold: Optional[str]


