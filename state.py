from typing_extensions import TypedDict, List

from pydantic import model_validator

class GraphState(TypedDict):
    query: str| None = None
    # category: str
   
    response: str| None = None
    history:List[str]| None = None
    @model_validator(mode="before")
    def validate_fields(cls, values):
        if not values.get("query") and not values.get("response"):
            raise ValueError("Either a or b must be provided")
        return values  # omitting this line will lead to the error
    
from pydantic import BaseModel

class SupervisorOutput(BaseModel):
    response: str


