from fastapi import FastAPI
import logging
import uvicorn
import httpx



colonies = {
    "de1685b3-3d2d-439d-9476-85ce6f9fc54a": "New Washington",
    "5ece00f1-b090-44dc-9803-e973f87392b7": "Liberty Base",
    "7ecd6406-9978-45a4-8406-77e84fff33bc": "Europa Outpost",
    "71be8b58-13e8-495f-967b-97429be84906": "Xin Tian Di",
    "70542b48-51b9-4498-9f09-1185189da7b0": "Mangalyaan Nagar",
    "52d474af-f112-4967-83af-db8559d3e94a": "Rodina Station",
}


app = FastAPI()
logging.basicConfig(level=logging.INFO)


@app.get("/")
def read_root():
    logging.info(" Immigration root endpoint called")
    return {"message": "Hello from immigration"}


# Service is notified when a new passenger is added to the system
# it would request the new passenger data using httpx
@app.post("/immigration/notify/new_passengers")
async def handle_notification():
    passengers = await _get_new_passengers()
    # logging.info("Passengers: " + str(passengers))
    for passenger in passengers:
        colony_id = next((key for key, value in colonies.items() if value == passenger["colony"]), None)
        # logging.info("Colony id: " + str(colony_id))

        colony_rules = await _get_colony_rules(colony_id)
        logging.info("Colony rules: " + str(colony_rules))    

        if _evaluate_passenger(passenger, colony_rules):
            # ask for granting colony resources
            # if passenger is granted colony resources send visa request to colony service 
            # upon receiving confirmation update passenger status: "visa_granted"
            # else passenger is not granted colony resources
            # update passenger status: "visa_denied"
            # log which passenger name is eligible for automatic visa grant
            logging.info("Passenger is eligible for automatic visa grant: " + str(passenger["first_name"] + " " + passenger["last_name"]))

    

        # If passenger is eligible based on colony rules
        #   ask for granting colony resources
        #       if passenger is granted colony resources send visa request to colony service 
        #       upon receiving confirmation update passenger status: "visa_granted"
        #   else passenger is not granted colony resources
        #       update passenger status: "visa_denied"
        # if the passenger is not eligible for automatic visa grant change passengers status to "flagged"





def _evaluate_rule(passenger, rule) -> bool:
    if rule.rule_type == "age":
        return passenger.age >= int(rule.description)
    elif rule.rule_type == "criminal_record":
        return passenger.criminal_record == rule.description
    elif rule.rule_type == "health_status":
        return passenger.health_status == rule.description
    elif rule.rule_type == "skills":
        return rule.description in passenger.skills
    elif rule.rule_type == "specialization":
        return rule.description in passenger.specialization
    else:
        return False

def _evaluate_passenger(passenger, rules) -> bool:
    for rule in rules:
        logging.info("Evaluating rule: " + str(rule))
        if not _evaluate_rule(passenger, rule):
            return False
    return True



async def _get_new_passengers():
    passengers_service_base_url = "http://0.0.0.0:3030"
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


# @app.get("/immigration/filter")
# async def get_risky_passengers():
#     response = db.scan()
#     filtered_passengers = []
#     # Add the filtered passengers to the array
#     for item in response['Items']:
#         if item.get('criminal_record') or item.get('health_status'):
#             filtered_passengers.append(item)

#     # If there are more items to fetch, continue scanning the table
#     while 'LastEvaluatedKey' in response:
#         response = db.scan(
#             ExclusiveStartKey=response['LastEvaluatedKey']
#         )
#         for item in response['Items']:
#             if item.get('criminal_record') and item.get('health_status'):
#                 filtered_passengers.append(item)

#     return filtered_passengers if filtered_passengers else {"message": "No risky passengers found"}






    

# - `POST /immigration/counters`: Create a new immigration counter
# - `GET /immigration/counters`: Get a list of immigration counters
# - `PUT /immigration/counters/{id}`: Update an immigration counter
# - `DELETE /immigration/counters/{id}`: Delete an immigration counter
# - `POST /immigration/counters/{id}/assign`: Assign a user to an immigration counter
# - `POST /immigration/counters/{id}/unassign`: Unassign a user from an immigration counter
# - `POST /immigration/visas`: Process a passenger visa application
# - `PUT /immigration/visas/{id}`: Update visa status
# - `GET /immigration/metrics`: Get average visa processing time