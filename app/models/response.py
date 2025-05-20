from pydantic import BaseModel, Field
from typing import Optional

class ReviewOutput(BaseModel):
    review: str = Field(..., description="The review comments or suggestions for the submitted code.")
    suggested_fix: Optional[str] = Field(None, description="An optional improved version of the code.")
    score: Optional[float] = Field(None, description="Optional score between 0 and 1 indicating code quality.")
