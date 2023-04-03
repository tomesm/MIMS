from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import uvicorn
import json
import random
import logging

from requests import PutColonyResourceRequest, PutImmigrationRuleRequest, PutColonyRequest

import resource_dao
import rule_dao
import colony_dao

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
def read_root():
    return {"message": "Hello from colony service"}


######### Visas #########

@app.post("/colonies/{colony_id}/visas")
async def create_visa(colony_id):
    # Just mock it for now
    return {"visa_id" : str(uuid4())}
    

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
#
# Algorithm description
# Each colony has a minimum limit of resources which can be granted per month
# Each resource request should contain number of months requested.
# If the colony can subtract the requested resources from the available resources 
# without going below the limit, then grant the resource
# refuse if otherwise
resource_limit = {
    "air": 654,
    "lodging": 1,
    "food": 67,
    "water": 100
}

colony_resource = {
    "air": 675756756734,
    "lodging": 34,
    "food": 456,
    "water": 57457567
}
@app.post("/colonies/{colony_id}/resources/grant")
async def grant_resource(colony_id):
    # #Mock it for now
    
    # random_number = random.random()

    # if random_number <= 0.9:  # 90% probability of success
    #     return {"message": f"Resources granted"}
    # else:  # 10% probability of error
    #     raise HTTPException(status_code=404, detail="Resources could not be granted")

    resource_limit = {
    "air": 654,
    "lodging": 1,
    "food": 67,
    "water": 100
    }

    colony_resource = resource_dao.list_resources(colony_id)[0]


    visa_types = [6, 12, 18, 24]

    # Find the maximum number of months that can be granted without going below the limit
    max_grantable_months = 0
    for visa_type in visa_types:
        requested_resources = {key: value * visa_type for key, value in resource_limit.items()}
        can_grant = all(colony_resource[key] - requested_resources[key] >= resource_limit[key] for key in resource_limit)
        
        if can_grant:
            max_grantable_months = visa_type
        else:
            break

    if max_grantable_months == 0:
        raise HTTPException(status_code=444, detail="Resources could not be granted")
    return {"visa_type": max_grantable_months}


# Create resource for given colony
@app.post("/colonies/{colony_id}/resources")
async def create_resource(colony_id, request: PutColonyResourceRequest):
    item = {
        "id": str(uuid4()),
        "colony_id": colony_id,
        "name": request.name,
        "air": request.air,
        "lodging": request.lodging,
        "food": request.food,
        "water": request.water
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
    item = resource_dao.get_resource(resource_id)
    if not item:
        raise HTTPException(status_code=404, detail="Resource not found")
    if item:
        update_data = request.dict(exclude_unset=True)
        updated_item = {**item, **update_data}
        return {"resource": resource_dao.update_resource(colony_id, updated_item)}
    else:
        raise HTTPException(status_code=404, detail=f"Resource {resource_id} not found")


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

