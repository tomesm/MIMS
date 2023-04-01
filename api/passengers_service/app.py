import time
from fastapi import FastAPI, HTTPException, UploadFile, File
from uuid import uuid4
import json
import uvicorn

import passengers_handler as ph
from models import PutPassengerRequest

 
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Baby, You Make Me Wish I Had Three Hands."}


@app.post("/passengers")
async def create_passenger(request: PutPassengerRequest):
    created_time = int(time.time())
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
        "ticket_number": request.ticketnumber,
        "status": request.status,
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
        item = {
            "passenger_id": str(uuid4()),
            "first_name": passenger["first_name"],
            "last_name": passenger["last_name"],
            "age": passenger["age"],
            "criminal_record": passenger["criminal_record"],
            "health_status": passenger["health_status"],
            "dest_departure": passenger["dest_departure"],
            "dest_arrival": passenger["dest_arrival"],
        }
        error = ph.create_passenger(item)
        if error:
            raise HTTPException(status_code=404, detail=f"Error creating passenger: {error}")

    return {"message:": "Bulk passengers created"}


@app.get("/passengers")
async def list_passengers():
    items = ph.list_passengers()
    if not items:
        raise HTTPException(status_code=404, detail=f"No passengers found")
    return {"passengers": items}


@app.get("/passengers/{passenger_id}")
async def get_passenger(passenger_id: str):
    item = ph.get_passenger(passenger_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Passenger {passenger_id} not found")
    return item

@app.get("/passengers/flagged")
async def get_flagged_passenger():
    items = ph.list_flagged_passengers()
    if not items:
        raise HTTPException(status_code=404, detail=f"No flagged opassenger not found")
    return items


@app.put("/passengers")
async def update_passenger(passenger_id: str, request: PutPassengerRequest):
    item = ph.get_passenger(passenger_id)
    if item:
        item["first_name"] = request.first_name
        item["last_name"] = request.last_name
        item["age"] = request.age
        item["criminal_record"] = request.criminal_record
        item["health_status"] = request.health_status
        item["dest_departure"] = request.dest_departure
        item["dest_arrival"] = request.dest_arrival
        return {"passenger": ph.update_passenger(passenger_id, item)}
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



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3030)
