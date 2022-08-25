from pydantic import BaseModel, Field, EmailStr, HttpUrl, constr
from copyreg import constructor

from fastapi import File

from typing import Optional
import datetime


# User base model

class User(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50        
    )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50
    )
    username: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,        
        gt=0,
        lt= 150
    )
    email: EmailStr = Field(...)
    
    is_superuser: Optional[bool] = Field(default=False)
    is_staff: Optional[bool] = Field(default=False)
    is_active: Optional[bool] = Field(default=True)
    date_jointed: datetime.date
    website: Optional[HttpUrl] = Field(default='')
    phone: Optional[        
        constr(            
            strip_whitespace=True,
            regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$",
        )
    ]
    is_dev: Optional[bool] = Field(default=False)
    is_hiring_manager: Optional[bool] = Field(default=False)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Rodrigo",
                "last_name": "Lopez",
                "age": 30,
                "email": "sbryanma@gmail.com",                           
                "username": "serbrylex",
                "is_superuser": True,
                "is_staff": True,
                "is_active": True,
                "date_jointed": datetime.date.today(),
                "website": "https://serbrylex.com",
                "phone": "+52 9983963548",
                "is_dev": False,
                "is_hiring_manager": False,
                "password": "324yulajsdf"                
            }
        }

# Token to handle autentication

class Token(BaseModel):    
    token: str

# Developer Models

class Dev(BaseModel):

    is_active: Optional[bool] = Field(default=True)
    repository: Optional[HttpUrl] = Field(default='')
    hackerrank: Optional[HttpUrl] = Field(default='')
    leetcode: Optional[HttpUrl] = Field(default='')    
    cover_letter: str = Field(
        ...,
        min_length=20,
        max_length=500
    )

class Languages(BaseModel):    
    language: str = Field(..., min_length=1, max_length=100)

class Certificate(BaseModel):    
    certificate_in: str = Field(..., min_length=10, max_length=100)
    completed_at: datetime.date = Field(...)

class Education(BaseModel):    
    school: str = Field(..., min_length=10, max_length=100)
    start_at: datetime.date = Field(...)
    end_at: datetime.date = Field(...)
    contry: str = Field(..., min_length=10, max_length=200)
    field: str = Field(..., min_length=10, max_length=200)
    description: str = Field(..., min_length=10, max_length=200)
    
class DevSkills(BaseModel):
    skill_id: str = Field(...)    

# Hiring Manager

class HiringManager(BaseModel):    
    is_active: Optional[bool] = Field(default=True)
