from pydantic import BaseModel
from typing import Optional

class PutImmigrationRuleRequest(BaseModel):
    colony_id: int
    name: str
    air: int
    lodging: int
    food: int
    water: int