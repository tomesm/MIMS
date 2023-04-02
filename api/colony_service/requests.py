from pydantic import BaseModel
from typing import Optional

class PutColonyResourceRequest(BaseModel):
    colony_id: Optional[str] = None
    name: Optional[str] = None
    air: Optional[int] = None
    lodging: Optional[int] = None
    food: Optional[int] = None
    water: Optional[int] = None

class PutImmigrationRuleRequest(BaseModel):
    colony_id: Optional[str] = None
    rule_type: Optional[str] = None
    description: Optional[str] = None


class PutColonyRequest(BaseModel):
    name: Optional[str] = None
    inhabitants: Optional[int] = None
    