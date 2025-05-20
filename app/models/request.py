from pydantic import BaseModel, Field, validator

class CodeInput(BaseModel):
    code: str = Field(..., description="The source code to be reviewed.")
    language: str = Field(default="python", description="Programming language of the code.")

    @validator("code")
    def code_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Code input cannot be empty.")
        return v
