from pydantic import BaseModel, Field


# User base model

class Skills(BaseModel):

    skill: str = Field(...)