from fastapi import APIRouter, HTTPException
from typing import Union


router = APIRouter()


@router.post("/", response_model=Union[SQLParser, ErrorResponse])
def sqlparser(sqlInput: SQLParserInput):
    print(f"parser request: {sqlInput}")
    try:


        # response = {
        #     "query": f"{query}",
        #     "dq_dimensions": dq_dimensions,
        #     "dq_measures":  dq_measures,
        #     "rule_function" : rule_function,
        #     "rule_measure" : rule_measure,
        #     "rule_condition" : rule_condition,
        #     "rule_threshold" : rule_threshold
        # }

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
