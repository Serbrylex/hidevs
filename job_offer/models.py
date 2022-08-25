from pydantic import BaseModel, Field, EmailStr, HttpUrl
from copyreg import constructor

from fastapi import File

from typing import Optional
import datetime

from enum import Enum

class ContractType(Enum):
    Freelancer = 'Freelancer'
    Halftime = 'Halftime'
    FullTime = 'FullTime' 

class Experience(Enum):
    Junior = 'Junior'
    MidLevel = 'MidLevel'
    Senior = 'Senior'    

# User base model

class JobOffer(BaseModel):
    user_id: str = Field(...)
    company: str = Field(..., min_length=10, max_length=100)
    salary_from: int = Field(..., gt=0)
    salary_to: int = Field(..., gt=salary_from) # No sé
    description: str = Field(..., max_length=10000, min_length=10)
    contract_type: Optional[ContractType] = Field(...)
    experience: Optional[Experience] = Field(...)

class JobOfferSkills(BaseModel):
    skill_id: str = Field(...)
    job_offer_id: str = Field(...)