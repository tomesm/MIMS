import datetime
import time
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.param_functions import Path
from uuid import uuid4
import uvicorn
import json
import random


import logging

import resource_dao
import rule_dao
import colony_dao
from requests import PutColonyResourceRequest, PutImmigrationRuleRequest, PutColonyRequest
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
logging.basicConfig(level=logging.INFO)


class VisaResponse(BaseModel):
    id: int
    duration: int
    issue_date: datetime
    immigration_counter_id: int
    colony_id: int


@app.get("/")
def read_root():
    return {"message": "Hello from colony service"}


######### Visas #########

@app.post("/colonies/{colony_id}/visas", response_model=VisaResponse)
async def create_visa(colony_id: int):
    # Check if the colony and passenger exist
    colony = colony_dao.get_colony(colony_id)

    if not colony:
        raise HTTPException(status_code=404, detail="Colony or passenger not found")
    # Set visa attributes (customize these as needed)
    visa_duration = 90  # Set the visa duration (in days)
    issue_date = datetime.now()  # Set the visa issue date
    immigration_counter_id = 1  # Set the immigration counter ID (customize this)

    # Insert the new visa record into the database
    # visa_id = visa_dao.create_visa(
    #     colony_id,
    #     passenger_id,        
    #     visa_duration,
    #     issue_date,
    #     immigration_counter_id,
    # )

    # Return the created visa
    return VisaResponse(
        id=visa_id,
        duration=visa_duration,
        issue_date=issue_date,
        immigration_counter_id=immigration_counter_id,
        colony_id=colony_id,
    )

######### Colonies  #########




# Create colony
@app.post("/colonies")
async def create_colony(request: PutColonyRequest):
    item = {
        "id": str(uuid4()),
        "name": request.name,
        "inhabitants": request.inhabitants
    }
    error = colony_dao.create_colony(item)
    if error:
        raise HTTPException(status_code=404, detail=f"Error creating colony: {error}")
    return {"colony:": item}

# Get a colony  by id
@app.get("/colonies/{colony_id}")
async def get_colony(colony_id):
    item = colony_dao.get_colony(colony_id)
    # if item is None:
    #     raise HTTPException(status_code=404, detail=f"Colony not found: {colony_id}")
    # return {"colony:": item}
    return item

# Get all colonies
@app.get("/colonies")
async def list_colonies():
    items = colony_dao.list_colonies()
    return {"colonies:": items}


@app.put("/colonies/{colony_id}")
async def update_colony(colony_id, request: PutColonyRequest):
    # Fetch the existing colony from your data source (e.g., list or database)
    item = colony_dao.get_colony(colony_id)
    if not item:
        raise HTTPException(status_code=404, detail="Colony not found")
    if item:
        update_data = request.dict(exclude_unset=True)
        updated_item = {**item, **update_data}
        return {"colony": colony_dao.update_colony(colony_id, updated_item)}
    else:
        raise HTTPException(status_code=404, detail=f"Colony {colony_id} not found")
    


# Delete colony
@app.delete("/colonies/{colony_id}")
async def delete_colony(colony_id):
    error = colony_dao.delete_colony(colony_id)
    if error:
        raise HTTPException(status_code=404, detail=f"Error deleting colony: {error}")
    return {"message": f"Colony {colony_id} deleted"}


############ Resources ############

# API endpoint for grant resource request
@app.post("/colonies/{colony_id}/resources/grant")
async def grant_resource(colony_id):
    # Get resource for the colony_id
    # Check if resource is available
    # If available, grant resource
    # If not available, return message

    # for POC demo just mock the response
    # Generate a random number between 0 and 1
    random_number = random.random()

    if random_number <= 0.9:  # 90% probability of success
        return {"message": f"Resources granted"}
    else:  # 10% probability of error
        raise HTTPException(status_code=404, detail="Resources could not be granted")


# Create resource for given colony
@app.post("/colonies/{colony_id}/resources")
async def create_resource(colony_id, request: PutColonyResourceRequest):
    item = {
        "id": str(uuid4()),
        "colony_id": colony_id,
        "resource_type": request.resource_type,
        "quantity": request.quantity
    }
    error = resource_dao.create_resource(item)
    if error:
        raise HTTPException(status_code=404, detail=f"Error creating resource: {error}")
    return {"resource:": item}


# Get a resource by id
@app.get("/colonies/{colony_id}/resources/{resource_id}")
async def get_resource(colony_id, resource_id):
    item = resource_dao.get_resource(resource_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Resource not found: {resource_id}")
    return {"resource:": item}

# Get all resources for given colony
@app.get("/colonies/{colony_id}/resources")
async def list_resources(colony_id):
    items = resource_dao.list_resources(colony_id)
    return items

# Update resource
@app.put("/colonies/{colony_id}/resources/{resource_id}")
async def update_resource(colony_id, resource_id, request: PutColonyResourceRequest):
    item = {
        "id": resource_id,
        "colony_id": colony_id,
        "resource_type": request.resource_type,
        "quantity": request.quantity
    }
    error = resource_dao.update_resource(item)
    if error:
        raise HTTPException(status_code=404, detail=f"Error updating resource: {error}")
    return {"resource:": item}


# Delete resource
@app.delete("/colonies/{colony_id}/resources/{resource_id}")
async def delete_resource(colony_id, resource_id):
    error = resource_dao.delete_resource(resource_id)
    if error:
        raise HTTPException(status_code=404, detail=f"Error deleting resource: {error}")
    return {"message": f"Resource {resource_id} deleted"}


############ Rules ############


# Create ImmigrationRule for given colony
@app.post("/colonies/{colony_id}/rules")
async def create_rule(colony_id, request: PutImmigrationRuleRequest):
    # logging.info("Creating rule for colony: %s", colony_id)
    # logging.info("request: %s", request)
    item = {
        "id": str(uuid4()),
        "colony_id": colony_id,
        "rule_type": request.rule_type,
        "description": request.description
    }
    error = rule_dao.create_rule(item)
    if error:
        raise HTTPException(status_code=404, detail=f"Error creating rule: {error}")
    return {"rule:": item}

# List rules for given colony
@app.get("/colonies/{colony_id}/rules")
async def list_rules(colony_id):
    items = rule_dao.list_rules(colony_id)
    return {"rules:": items}


# Get a rule by id
@app.get("/colonies/{colony_id}/rules/{rule_id}")
async def get_rule(colony_id, rule_id):
    item = rule_dao.get_rule(rule_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Rule not found: {rule_id}")
    return {"rule:": item}


# Create bulk request for colony rules
@app.post("/colonies/{colony_id}/rules/bulk")
async def create_bulk_rules(colony_id, file: UploadFile = File(...)):
    # logging.info("Creating bulk rules for colony: %s", colony_id)
    # logging.info("request: %s", request)
    content = await file.read()
    rules = json.loads(content)
    for rule in rules:
        item = {
            "id": str(uuid4()),
            "colony_id": colony_id,
            "rule_type": rule["rule_type"],
            "description": rule["description"]
        }
        error = rule_dao.create_rule(item)
        if error:
            raise HTTPException(status_code=404, detail=f"Error creating bulk rules: {error}")
        
    return {"message:": f"Rules created for colony {colony_id}"}

# Update rule
@app.put("/colonies/{colony_id}/rules/{rule_id}")
async def update_rule(colony_id, rule_id, request: PutImmigrationRuleRequest):
    item = {
        "id": rule_id,
        "colony_id": colony_id,
        "rule_type": request.rule_type,
        "description": request.description
    }
    error = rule_dao.update_rule(rule_id, item)
    if error:
        raise HTTPException(status_code=404, detail=f"Error updating rule: {error}")
    return {"rule:": item}

# Delete one rule
@app.delete("/colonies/{colony_id}/rules/{rule_id}")
async def delete_rule(colony_id, rule_id):
    error = rule_dao.delete_rule(rule_id)
    if error:
        raise HTTPException(status_code=404, detail=f"Error deleting rule: {error}")
    return {"message": "Rule deleted"}


# Delete all rules for given colony
@app.delete("/colonies/{colony_id}/rules")
async def delete_rules(colony_id):
    error = rule_dao.delete_rules(colony_id)
    if error:
        raise HTTPException(status_code=404, detail=f"Error deleting rules: {error}")
    return {"message": "Rules deleted"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3032)

