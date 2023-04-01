import time
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.param_functions import Path
from uuid import uuid4
import uvicorn
import json


import logging

import resource_dao
import rule_dao
import colony_dao
from models import PutColonyResourceRequest, PutImmigrationRuleRequest, PutColonyRequest


app = FastAPI()
logging.basicConfig(level=logging.INFO)


@app.get("/")
def read_root():
    return {"message": "Hello from colony service"}


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

# Update colony
@app.put("/colonies/{colony_id}")
async def update_colony(colony_id, request: PutColonyRequest):
    item = {
        "id": colony_id,
        "name": request.name,
        "inhabitants": request.inhabitants
    }
    error = colony_dao.update_colony(colony_id, item)
    if error:
        raise HTTPException(status_code=404, detail=f"Error updating colony: {error}")
    return {"colony:": item}

# Delete colony
@app.delete("/colonies/{colony_id}")
async def delete_colony(colony_id):
    error = colony_dao.delete_colony(colony_id)
    if error:
        raise HTTPException(status_code=404, detail=f"Error deleting colony: {error}")
    return {"message": f"Colony {colony_id} deleted"}


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
    return {"resources:": items}

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
    error = rule_dao.update_rule(item)
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



# @app.post("/colonies/resources")
# async def create_resource(request: PutColonyResourceRequest):
#     item = {
#         "id": str(uuid4()),
#         "colony_id": str(uuid4()),
#         "name": request.name,
#         "air": request.air,
#         "lodging": request.lodging,
#         "food": request.food,
#         "water": request.water
#     }
#     error = resource_dao.create_resource(item)
#     if error:
#         raise HTTPException(status_code=404, detail=f"Error creating resource: {error}")
#     return {"resource:": item}


# @app.get("/colonies/resources")
# async def get_resources():
#     resources = resource_dao.list_resources()
#     if resources is None:
#         raise HTTPException(status_code=404, detail=f"Error getting resourcs")
#     return {"resource:": resources}


# @app.get("/colonies/resources/{id}")
# async def get_resource(id):
#     resource = resource_dao.get_resource(id)
#     if resource is None:
#         raise HTTPException(status_code=404, detail=f"Error getting resource")
#     return {"resource:": resource}


# @app.put("/colonies/resources/{id}")
# async def update_resource(id, request: PutColonyResourceRequest):
#     item = {
#         "id": id,
#         "colony_id": request.colony_id,
#         "name": request.name,
#         "air": request.air,
#         "lodging": request.lodging,
#         "food": request.food,
#         "water": request.water
#     }
#     error = resource_dao.update_resource(id, item)
#     if error:
#         raise HTTPException(status_code=404, detail=f"Error updating resource: {error}")
#     return {"resource:": item}


# @app.delete("/colonies/resources/{id}")
# async def delete_resource(id):
#     error = resource_dao.delete_resource(id)
#     if error:
#         raise HTTPException(status_code=404, detail=f"Error deleting resource")
#     return {"message": "Resource deleted"}


# @app.delete("/colonies/resources")
# async def delete_resources():
#     error = resource_dao.delete_resources()
#     if error:
#         raise HTTPException(status_code=404, detail=f"Error deleting resources")
#     return {"message": "Resources deleted"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3032)

