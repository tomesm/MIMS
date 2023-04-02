from fastapi import FastAPI
import logging
import uvicorn
import httpx
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the allowed origins here, use "*" to allow all origins
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




@app.get("/")
def read_root():
    logging.info(" Immigration root endpoint called")
    return {"message": "Hello from immigration"}


# Service is notified when a new passenger is added to the system and starts automatic visa process
@app.post("/immigration/notify/new_passengers")
async def handle_notification():
    passengers = await _get_new_passengers()
    # logging.info("Passengers: " + str(passengers))
    for passenger in passengers:
        colony_id = next((key for key, value in colonies.items() if value == passenger["colony"]), None)
        # logging.info("Colony id: " + str(colony_id))

        colony_rules = await _get_colony_rules(colony_id)
        # logging.info("Colony rules: " + str(colony_rules))    

        if _evaluate_passenger(passenger, colony_rules):
            # logging.info("Passenger is eligible for automatic visa grant: " + str(passenger["first_name"] + " " + passenger["last_name"]))
            # ask for granting colony resources
            url = f"http://0.0.0.0:3032/colonies/{colony_id}/resources/grant"
            r = httpx.post(url)
            # upon receiving confirmation update passenger status: "visa_granted"
            if r.status_code == 200:
                passenger["status"] = "visa_pre_granted"
                await _update_passenger(passenger)
                # Send visa request to colony service
                # visa_url = f"http://0.0.0.0:3032/colonies/{colony_id}/visas"
                # r = httpx.post(visa_url)
                # # logging.info("Visa response: " + str(r.json()))

                # if r.status_code == 200:
                #     passenger["visa_id"] = r.json()["visa_id"]
                #     # logging.info(f"Updated passenger with visa: {passenger}")
                #     await _update_passenger(passenger)
            else:
                passenger["status"] = "visa_denied"
                await _update_passenger(passenger)
        # if the passenger is not eligible for automatic visa grant change passengers status to "flagged"
        else:
            logging.info("Passenger is not eligible for automatic visa grant: " + str(passenger["first_name"] + " " + passenger["last_name"]))
            # update passenger status: "flagged"
            passenger["status"] = "flagged"
            # send updated pasenger back to passenger service via httpx
            await _update_passenger(passenger)
        

async def _update_passenger(passenger):
    passenger_id = passenger["id"]
    r = httpx.put(f"http://0.0.0.0:3030/passengers?passenger_id={passenger_id}", json=passenger)


    if r.status_code == 200:
        print("Passenger status updated successfully")
    else:
        print("Failed to update passenger status" + r.text)



def _evaluate_rule(passenger, rule) -> bool:
    rule_type = rule["rule_type"]
    # logging.info("Passenger : " + str(passenger))
    # logging.info("Rule description: " + str(rule["description"]))
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
    
    # get passengers from the passenger service
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

