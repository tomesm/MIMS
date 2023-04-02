from pydantic import BaseModel
from typing import Optional

class PutPassengerRequest(BaseModel):
    flight_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[str] = None
    criminal_record: Optional[str] = None
    health_status: Optional[str] = None
    colony: Optional[str] = None 
    skills: Optional[str] = None
    specialization: Optional[str] = None
    ticket_number: Optional[str] = None 
    status: Optional[str] = None


