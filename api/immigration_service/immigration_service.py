from fastapi import FastAPI
import logging
import uvicorn
import httpx
import random
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

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

colonies = {
    "de1685b3-3d2d-439d-9476-85ce6f9fc54a": "New Washington",
    "5ece00f1-b090-44dc-9803-e973f87392b7": "Liberty Base",
    "7ecd6406-9978-45a4-8406-77e84fff33bc": "Europa Outpost",
    "71be8b58-13e8-495f-967b-97429be84906": "Xin Tian Di",
    "70542b48-51b9-4498-9f09-1185189da7b0": "Mangalyaan Nagar",
    "52d474af-f112-4967-83af-db8559d3e94a": "Rodina Station",
}

passengers_service_base_url = "http://0.0.0.0:3030"
colony_service_base_url = "http://0.0.0.0:3032"

visa_types = [6, 12, 18, 24]


@app.get("/")
def read_root():
    logging.info(" Immigration root endpoint called")
    return {"message": "Hello from immigration"}


# apply for visa
@app.post("/immigration/visa/apply/{passenger_id}")
async def apply_for_visa(passenger_id: str):
    
        r = httpx.get(f"http://0.0.0.0:3030/passengers/{passenger_id}")
        if r.status_code == 200:
            passenger= r.json()
            # logging.info("Passenger: " + passenger)

            status = passenger["status"]
            if status == "flagged":
                return {"status": "flagged", "message": "Visa can not be granted automatically to flagged passengers"}
            elif status == "visa_denied":
                return {"status": "visa_denied"}
            else: 
                parts = status.split(',')
                # Extract the values
                status = parts[0]
                visa_type = int(parts[1])
                
                # mock visa granting
                passenger["status"] = "visa_granted"
                passenger["visa_id"] = str(uuid4())
                await _update_passenger(passenger)
                return {"status": "visa_granted", "visa_id": passenger["visa_id"], "visa_type": visa_type}
                




# Service is notified when a new passenger is added to the system and starts automatic visa process
@app.post("/immigration/notify/new_passengers")
async def handle_notification():
    passengers = await _get_new_passengers()
    for passenger in passengers:
        colony_id = next((key for key, value in colonies.items() if value == passenger["colony"]), None)

        colony_rules = await _get_colony_rules(colony_id)

        if _evaluate_passenger(passenger, colony_rules):
            url = f"http://0.0.0.0:3032/colonies/{colony_id}/resources/grant"
            r = httpx.post(url)
            if r.status_code == 200:
                visa_type = random.choice(visa_types)
                passenger["status"] = "visa_pre_granted" + "," + str(visa_type)
                logging.info("Passenger is pre-approved with resources for " + str(visa_type) + " months: " + str(passenger["first_name"] + " " + passenger["last_name"]))
                await _update_passenger(passenger)
            else:
                passenger["status"] = "visa_denied"
                logging.info("Passenger is denied: " + str(passenger["first_name"] + " " + passenger["last_name"]))
                await _update_passenger(passenger)
        # if the passenger is not eligible for automatic visa grant change passengers status to "flagged"
        else:
            logging.info("Passenger is flagged: " + str(passenger["first_name"] + " " + passenger["last_name"]))
            # update passenger status: "flagged"
            passenger["status"] = "flagged"
            # send updated pasenger back to passenger service via httpx
            await _update_passenger(passenger)
        

async def _update_passenger(passenger):
    passenger_id = passenger["id"]
    r = httpx.put(f"http://0.0.0.0:3030/passengers?passenger_id={passenger_id}", json=passenger)



def _evaluate_rule(passenger, rule) -> bool:
    rule_type = rule["rule_type"]
    if rule_type == "age":
        return int(passenger["age"]) >= int(rule["description"])
    elif rule_type == "criminal_record":
        return passenger["criminal_record"] == rule["description"]
    elif rule_type == "health_status":
        return passenger["health_status"] == rule["description"]
    elif rule_type == "skills":
        return rule["description"] in passenger["skills"]
    elif rule_type == "specialization":
        return rule["description"] in passenger["specialization"]
    else:
        return False

def _evaluate_passenger(passenger, colony_rules) -> bool:
    rules = colony_rules.get("rules:")
    for rule in rules:
        if not _evaluate_rule(passenger, rule):
            return False
    return True


async def _get_new_passengers():
    async with httpx.AsyncClient() as client:
        r = await client.get(passengers_service_base_url + "/passengers")
    return r.json()


async def _get_colony_rules(colony_id):
    passengers_service_base_url = "http://0.0.0.0:3032"
    # get passengers from the passenger service
    async with httpx.AsyncClient() as client:
        r = await client.get(passengers_service_base_url + f"/colonies/{colony_id}/rules")
    return r.json()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3031)

