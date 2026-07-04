from typing import TypedDict, Annotated, List, Optional, Literal
import operator
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage

class ASKNOVA(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    tone: Optional[str]

class INTENT(BaseModel):
    tone: Literal["angry", "happy", "sad", "frustrated"] = Field(..., description="You have to find the tone of the user from the query itself, if the user is angry pass 'angry', if the user query denotes that he/she is happy then pass 'happy', if frustrated then pass 'frustrated', if sad then pass 'sad'")