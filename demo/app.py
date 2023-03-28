from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import json
from typing import Optional
from enum import Enum

class RiskLevel(str, Enum):
    """
    Enum to represent the risk levels for passengers.
    """
    all = "all"
    medium = "medium"
    high = "high"

class PassengerService:
    """
    Class to handle passenger-related operations.
    """

    def __init__(self):
        self.passengers = []

    def add_passengers(self, passengers: list):
        """
        Add passengers to the list.

        :param list passengers: List of passengers to add.
        """
        self.passengers = passengers

    def get_passengers(self) -> list:
        """
        Get the list of passengers.

        :return: List of passengers.
        :rtype: list
        """
        return self.passengers

    def get_flagged_passengers(self, risk_level: Optional[RiskLevel]) -> list:
        """
        Get flagged passengers based on the risk level.

        :param Optional[RiskLevel] risk_level: The risk level to filter passengers by.
        :return: List of flagged passengers.
        :rtype: list
        """
        return list(filter(lambda passenger: self._filter_by_risk_level(passenger, risk_level), self.passengers))
    
    def _filter_by_risk_level(self, passenger: dict, risk_level: RiskLevel) -> bool:
        """
        Filter passengers by risk level.

        :param dict passenger: The passenger to evaluate.
        :param RiskLevel risk_level: The risk level to filter by.
        :return: Boolean indicating whether the passenger meets the risk level criteria.
        :rtype: bool
        """
        if risk_level == RiskLevel.all:
            return passenger["health_status"] or passenger["criminal_record"]
        elif risk_level == RiskLevel.medium:
            return passenger["health_status"] and not passenger["criminal_record"]
        elif risk_level == RiskLevel.high:
            return passenger["health_status"] and passenger["criminal_record"]
 
app = FastAPI()
# Serving static files
app.mount("/../static", StaticFiles(directory="static"), name="static")

passenger_service = PassengerService()

# Root endpoint
@app.get("/")
async def read_root():
    """
    Serve the root endpoint with the static index.html file.

    :return: FileResponse with the index.html file.
    :rtype: FileResponse
    """
    return FileResponse("static/index.html")

@app.post("/passengers")
async def prioritize_passengers(file: UploadFile = File(...)):
    """
    Add passengers from the uploaded JSON file.

    :param UploadFile file: The JSON file containing passenger data.
    :return: A message indicating the success of adding passengers.
    :rtype: dict
    """
    content = await file.read()
    passengers = json.loads(content)
    passenger_service.add_passengers(passengers)
    return {"message": "Passengers added successfully"}

@app.get("/passengers")
async def get_passengers():
    """
    Get the list of passengers.

    :return: List of passengers.
    :rtype: list
    """
    return passenger_service.get_passengers()

@app.get("/passengers/risky")
async def get_flagged_passengers(risk_level: Optional[RiskLevel] = RiskLevel.all) -> list:
    """
    Get flagged passengers based on the risk level.

    :param Optional[RiskLevel] risk_level: The risk level to filter passengers by.
    :return: List of flagged passengers.
    :rtype: list
    """
    return passenger_service.get_flagged_passengers(risk_level)

def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()