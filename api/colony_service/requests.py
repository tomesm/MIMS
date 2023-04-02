from pydantic import BaseModel
from typing import Optional

class PutColonyResourceRequest(BaseModel):
    colony_id: Optional[str] = None
    name: Optional[str] = None
    air: Optional[str] = None
    lodging: Optional[str] = None
    food: Optional[str] = None
    water: Optional[str] = None

class PutImmigrationRuleRequest(BaseModel):
    colony_id: Optional[str] = None
    rule_type: Optional[str] = None
    description: Optional[str] = None


class PutColonyRequest(BaseModel):
        name: Optional[str] = None
        inhabitants: Optional[int] = None
    