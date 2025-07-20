from pydantic import BaseModel
from typing_extensions import TypedDict
from typing import Set 

# Schema for the response of the /question endpoint
class QAResponse(TypedDict):
    answer: str
    Sources: Set[str]

# Schema for the request body of the /question endpoint
class QuestionRequest(BaseModel):
    question: str