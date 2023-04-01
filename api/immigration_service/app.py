from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel
from typing import Optional
from enum import Enum
import http3
import logging
import uvicorn


class RiskLevel(str, Enum):
    """
    Enum to represent the risk levels for passengers.
    """
    all = "all"
    medium = "medium"
    high = "high"


mars_colonies = {
    1 : "New Washington",
    2 : "Liberty Base",
    3 : "Europa Outpost",
    4 : "Xin Tian Di",
    5 : "Mangalyaan Nagar",
    6 : "Rodina Station",
}

app = FastAPI()
logging.basicConfig(level=logging.INFO)


@app.get("/")
def read_root():
    logging.info(" Immigration root endpoint called")
    return {"message": "Hello from immigration"}


# Service is notified when a new passenger is added to the system
# it would request the new passenger data using http3
@app.post("/immigration/notify/new_passengers")
async def handle_notification():
    base_url = "0.0.0.0:3030"
    # get passengers from the passenger service
    r = await http3.get(base_url + "/passengers/new")
    passengers = r.json()

    for passenger in passengers:
        colony_id = next((colony_id for colony_id, name in mars_colonies.items() if name == passenger["colony"]), None)
        logging.info("Colony id: " + str(colony_id))

    # Request colony rules from colony service
    # r = await http3.get(base_url + "/colonies")

    

        # If passenger is eligible based on colony rules
        #   ask for granting colony resources
        #       if passenger is granted colony resources send visa request to colony service 
        #       upon receiving confirmation update passenger status: "visa_granted"
        #   else passenger is not granted colony resources
        #       update passenger status: "visa_denied"
        # if the passenger is not eligible for automatic visa grant change passengers status to "flagged"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3030)


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