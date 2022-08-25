from fastapi import FastAPI, Body, Query, Path

from typing import Optional

from main import app, db

# Models
from .models import JobOffer, JobOfferSkills

@app.get('/job_offers/')
def show_job_offers():
    job_offers = db.search_by_value('hidevs', 'job_offers', "id", "*", get_attributes=['*'])
    return job_offers
