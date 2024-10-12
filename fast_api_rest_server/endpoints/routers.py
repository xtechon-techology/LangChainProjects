from fastapi import APIRouter, HTTPException
from typing import Union
from schemas.parsers import Summary
from chains.expert_role.linkedin_profile_summarizer_with_parser_for_app import linkedin_summarizer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter()


@router.post("/", response_model=Summary)
def sqlparser(query: str) -> Union[Summary, HTTPException]:
    try:
        results: Summary = linkedin_summarizer(query=query)

        response = Summary(
            summary=results[0].get("summary"),
            facts=results[0].get("facts")
        )
        # # return response
        # # return JSONResponse(content=jsonable_encoder(response))
        # response = Summary(
        #     summary="This is a summary",
        #     facts=["Fact 1", "Fact 2"]
        # )
        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

