from pydantic import BaseModel
from typing import Optional

class PutColonyResourceRequest(BaseModel):
    id: str
    colony_id: str
    name: str
    air: int
    lodging: int
    food: int
    water: int

class PutImmigrationRuleRequest(BaseModel):
    id: str
    colony_id: str
    rule_type: str
    description: str


class PutColonyRequest(BaseModel):
        id: str
        name: str
        inhabitants: int
    