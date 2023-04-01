import time
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.param_functions import Path
from uuid import uuid4
import json
import uvicorn
import http3
from pydantic import BaseModel
from typing import Optional

import rule_dao


app = FastAPI()

class PutImmigrationRuleRequest(BaseModel):
    colony_id: Optional[int] = None
    name: str
    air: int
    lodging: int
    food: int
    water: int

@app.get("/")
def read_root():
    return {"message": "Hello from colony service"}


# - `POST /colonies/{id}/rules`: Create immigration rules
@app.post("colonies/rules")
async def create_rule(request: PutImmigrationRuleRequest):
    created_time = int(time.time())
    item = {
        
        "colony_id": 3,
        "name": request.name,
        "air": request.air,
        "lodging": request.lodging,
        "food": request.food,
        "water": request.water
    }
    error = rule_dao.create_rule(item)
    if error:
        raise HTTPException(status_code=404, detail=f"Error creating rule: {error}")
    return {"rule:": item}


# - `GET /colonies/{id}/rules`: Get immigration rules
@app.get("/colonies/rules")
async def get_rules(id: id):
    rules = rule_dao.get_rules(id)
    if rules is None:
        raise HTTPException(status_code=404, detail=f"Error getting rules")
    return {"rules:": rules}


@app.get("/colonies/rules/{id}")
async def get_rule(id: id):
    rule = rule_dao.get_rule(id)
    if rule is None:
        raise HTTPException(status_code=404, detail=f"Error getting rule")
    return {"rule:": rule}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3031)


# - `POST /colonies`: Create a new colony
# - `GET /colonies`: Get a list of colonies
# - `PUT /colonies/{id}`: Update a colony
# - `DELETE /colonies/{id}`: Delete a colony
# - `POST /colonies/{id}/rules`: Create immigration rules
# - `GET /colonies/{id}/rules`: Get immigration rules
# - `PUT /colonies/{id}/rules/{ruleId}`: Update immigration rules
# - `DELETE /colonies/{id}/rules/{ruleId}`: Delete immigration rules
# - `POST /colonies/{id}/visas`: Create a visa
# - `GET /colonies/{id}/visas`: Get a list of visas
# - `PUT /colonies/{id}/visas/{visaId}`: Update a visa
# - `DELETE /colonies/{id}/visas/{visaId}`: Delete a visa
# - `GET /colonies/{id}/arrivals`: Retrieve planned arrivals data