from fastapi import APIRouter, HTTPException
from typing import Union
from schemas.parsers import Summary


router = APIRouter()


@router.post("/", response_model=Summary)
def sqlparser():
    try:
        response = {
            "summary": "summary",
            "facts": ["fact1", "fact2"]
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

