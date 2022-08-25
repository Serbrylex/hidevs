from fastapi import FastAPI, Body, Query, Path

from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, EmailStr

from users.views import router as users_router


app = FastAPI()
app.include_router(users_router, prefix="", tags=["users"])