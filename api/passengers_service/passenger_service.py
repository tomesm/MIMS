import time
from fastapi import FastAPI, HTTPException, UploadFile, File
from uuid import uuid4
import json
import uvicorn

import passenger_dao as ph
from requests import PutPassengerRequest
import logging
import httpx
 
app = FastAPI()
logging.basicConfig(level=logging.DEBUG)


@app.get("/")
def read_root():
    return {"message": "Baby, You Make Me Wish I Had Three Hands."}


@app.post("/passengers")
async def create_passenger(request: PutPassengerRequest):
    item = {
        "id": str(uuid4()),
        "flight_id": request.flight_id,
        "first_name": request.first_name,
        "last_name": request.last_name,
        "age": request.age,
        "criminal_record": request.criminal_record,
        "health_status": request.health_status,
        "colony": request.colony,
        "skills": request.skills,
        "specialization": request.specialization,
        "ticket_number": request.ticket_number,
        "status": "new",
    }
    error = ph.create_passenger(item)
    if error:
        raise HTTPException(status_code=404, detail=f"Error creating passenger: {error}")
    return {"passenger:": item}


# Create passengers bulk
@app.post("/passengers/bulk")
async def create_passengers(file: UploadFile = File(...)):
    content = await file.read()
    passengers = json.loads(content)
    # error = ph.create_passengers(passengers) # this is not working for now
    for passenger in passengers:
        # logging.info("Passenger:" + str(passenger))
        item = {
            "id": str(uuid4()),
            "flight_id": passenger["flight_id"],
            "first_name": passenger["first_name"],
            "last_name": passenger["last_name"],
            "age": passenger["age"],
            "criminal_record": passenger["criminal_record"],
            "health_status": passenger["health_status"],
            "colony": passenger["colony"],
            "skills": passenger["skills"],
            "specialization": passenger["specialization"],
            "ticket_number": passenger["ticket_number"],
            "status": "new",
        }
        # logging.info("Passenger item:" + str(item))
        error = ph.create_passenger(item)
        if error:
            raise HTTPException(status_code=404, detail=f"Error creating passenger: {error}")

    # Notify the immigration
    await _notify_immigration()
    return {"message:": "Bulk passengers created"}


@app.get("/passengers")
async def list_passengers():
    items = ph.list_passengers()
    # if not items:
    #     raise HTTPException(status_code=404, detail=f"No passengers found")
    # return {"passengers": items}
    return items

@app.get("/passengers/status")
async def list_by_status(status: str):
    items = ph.list_by_status(status)
    return items

@app.get("/passengers/{passenger_id}")
async def get_passenger(passenger_id: str):
    item = ph.get_passenger(passenger_id)
    # if not item:
    #     raise HTTPException(status_code=404, detail=f"Passenger {passenger_id} not found")
    return item


@app.put("/passengers")
async def update_passenger(passenger_id: str, request: PutPassengerRequest):
    item = ph.get_passenger(passenger_id)
    if item:
        update_data = request.dict(exclude_unset=True)
        updated_item = {**item, **update_data}
        return {"passenger": ph.update_passenger(passenger_id, updated_item)}
    else:
        raise HTTPException(status_code=404, detail=f"Passenger {passenger_id} not found")


@app.delete("/passengers/{passenger_id}")
async def delete_passenger(passenger_id: str):
    error = ph.delete_passenger(passenger_id)
    if error:
        raise HTTPException(status_code=404, detail=f"Passenger {passenger_id} not found")
    return { "deleted_passenger_id": passenger_id }
    

# Delete all passengers
@app.delete("/passengers")
async def delete_passengers():
    error = ph.delete_passengers()
    if error:
        raise HTTPException(status_code=404, detail=f"Error deleting passengers: {error}")
    return { "message": "All passengers deleted" }



async def _notify_immigration():
    async with httpx.AsyncClient() as client:
        r = await client.post("http://0.0.0.0:3031" + "/immigration/notify/new_passengers")
    return r.json()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3030)
