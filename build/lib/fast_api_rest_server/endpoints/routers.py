from fastapi import APIRouter, HTTPException
from typing import Union


router = APIRouter()


@router.post("/", response_model=Union[SQLParser, ErrorResponse])
def sqlparser(sqlInput: SQLParserInput):
    print(f"parser request: {sqlInput}")
    try:
        # query, dq_dimensions, dq_measures, rule, rule_function, rule_measure, rule_condition, rule_threshold = parse_sql_statement(sqlInput.sql)

        # {"query": "SELECT * FROM REPLICN_HANA.TRNFRM_ECC_ENT.SCD_CONTRACT_STATUS_DX(NOLOCK)", "dq_dimensions": [],
        #  "dq_measures": [], "rule_function": "Count", "rule_measure": "", "rule_condition": "", "rule_threshold": ""}


        # if double quotes are as prefix and suffix of the sql query, remove them
        if sqlInput.sql.startswith('"') and sqlInput.sql.endswith('"'):
            sqlInput.sql = sqlInput.sql[1:-1]

        result = parse_sql_statement(sqlInput.sql)
        # Check if the result is an error response
        if isinstance(result, dict) and "error" in result:
            print(f"Error: {result['error']}")
            return {
                "Error": result['error']
            }
        else:
            query, dq_dimensions, dq_measures, rule, rule_function, rule_measure, rule_condition, rule_threshold = result
            print(f"SQL Parser Result: {query}, {dq_dimensions}, {dq_measures}, {rule}")
            # return result

            response = {
                "query": f"{query}",
                "dq_dimensions": dq_dimensions,
                "dq_measures":  dq_measures,
                "rule_function" : rule_function,
                "rule_measure" : rule_measure,
                "rule_condition" : rule_condition,
                "rule_threshold" : rule_threshold
            }

            return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
