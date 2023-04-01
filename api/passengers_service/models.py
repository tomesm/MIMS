from pydantic import BaseModel
from typing import Optional

class PutPassengerRequest(BaseModel):
    id: str
    flight_id: int
    first_name: str
    last_name: str
    age: int
    criminal_record: str
    health_status: str
    colony: str 
    skills: str
    specialization: str
    ticketnumber: str
    status: str

