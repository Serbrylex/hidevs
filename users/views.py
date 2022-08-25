from fastapi import APIRouter, Body, Query, Path, Request

from pydantic import EmailStr, HttpUrl

from typing import Optional

from secrets import token_bytes
from base64 import b64encode

import datetime

from db import db

# Models
from .models import (
    User, Token, Dev, Languages, Certificate, Education, DevSkills, HiringManager
)

isOwner = 'isOwner'

def valid_credentials(validateIfOwner: bool):

    def decorator_valid(func):
        def wrapper(*args, **kwargs):        
            token = args['request'].headers['access_token']
            db.update('hidevs', 'users', [{'id': id, "body": { 'is_dev': True }}])
            
            res = db.sql(f'Select user_id From hidevs.tokens where token={token}')
            if res == None:
                return {'message': 'You did not have permisions'}

            if validateIfOwner:
                res = db.sql(f'Select * from hidevs.users where id = (Select user_id From hidevs.tokens where token={token})')
                if res == None:
                    return {'message': 'You are not the owner'}
            func(*args, **kwargs)

        return wrapper
    return decorator_valid

router = APIRouter()

@router.post('/sigup/')
def signup(data: User = Body(...)): # recibimos un json tipo user
    res = db.insert('hidevs', 'user', [{"body": data['body']}])
    print(res)
    print('*'*20)
    users = db.sql('SELECT * FROM hidevs.users')
    return dict(users)        

@router.post('/login/')
def login(
    user: str = Body(...),
    password: str = Body(...)
):
    user = db.sql(f'Select * From hidevs.users Where email={user} and password={password}')
    if user != None:
        token = db.sql(f'Select * From hidevs.tokens Where user_id={user.id}')
        if token == None or token.expire < datetime.time:
            access_token = b64encode(token_bytes(32)).decode()
        else:
            access_token = token.access_token

    return dict({ 'user': user, 'access_token': access_token })

@router.patch('/update-profile/{id}/')
def update_profile(
    id: str,
    first_name: Optional[str] = Query(default = None, min_length=1, max_length=50),
    last_name: Optional[str] = Query(default = None, min_length=1, max_length=50),
    username: Optional[str] = Query(default = None, min_length=1, max_length=50),
    age: Optional[int] = Query(default = None, ge=0, le=150),
    email: Optional[EmailStr] = Query(default = None),
    website: Optional[HttpUrl] = Query(default = None),
    phone: Optional[str] = Query(default = None, min_length=1, max_length=50),
    is_dev: Optional[bool] = Query(default = None),
    is_hiring_manager: Optional[bool] = Query(default = None)
):
    records = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'age': age,
        'email': email,
        'website': website,
        'phone': phone,
        'is_dev': is_dev,
        'is_hiring_manager': is_hiring_manager
    }

    keys = records.keys()
    while len(keys) > 0:
        if records[keys[len(keys-1)]] == None:
            records.pop(keys[len(keys-1)])
            keys.pop()    

    res = db.update('hidevs', 'users', [{'id': id, "body": records}])

    return dict(res)
            
@valid_credentials(True)
@router.post('/add-dev-roll/{id}')
def add_dev_roll(
    id: str, 
    request: Request,
    dev: Dev = Body(...),
    languages: list[Languages] = Body(...),
    certificate: list[Certificate] = Body(...),
    education: list[Education] = Body(...),
    dev_skills: list[DevSkills] = Body(...)
):

    token = request.headers['access_token']
    db.update('hidevs', 'users', [{'id': id, "body": { 'is_dev': True }}])        
    
    dev_data = {
        'user_id': id,
        **dev
    }

    dev = db.insert('hidevs', 'devs', [{"body": dev_data}])

    for lan in languages:
        data_l = {
            'dev_id': dev.id,
            **lan
        }
        db.insert('hidevs', 'languages', [{"body": data_l}])

    for lan in certificate:
        data_l = {
            'dev_id': dev.id,
            **lan
        }
        db.insert('hidevs', 'certificate', [{"body": data_l}])

    for lan in education:
        data_l = {
            'dev_id': dev.id,
            **lan
        }
        db.insert('hidevs', 'education', [{"body": data_l}])

    for skill in dev_skills:        
        skill_a = db.insert('hidevs', 'skills', [{"body": skill}])
        data = {
            'skill_id': skill_a.id,
            'dev_id': dev.id
        }
        db.insert('hidevs', 'dev_skills', [{"body": data}])

    return dict(dev)


@valid_credentials(True)
@router.post('/add-hiring-manager-roll/{id}')
def add_hiring_manager_roll(
    id: str, 
    request: Request
):
    res = db.insert('hidevs', 'hiring_manager', [{"body": {'is_active': True}}])
    return res


@router.get('/profile/{id}')
def profile(
    id: str
):
    data = {
        **user,
    }
    user = db.search_by_value('hidevs', 'users', [id], "*", get_attributes=['*'])

    if user.is_dev:
        dev = db.search_by_value('hidevs', 'dev', attribute='user_id', value=user.id)
        languages = db.search_by_value('hidevs', 'languages', attribute='dev_id', value=dev.id)
        certificate = db.search_by_value('hidevs', 'certificate', attribute='dev_id', value=dev.id)
        education = db.search_by_value('hidevs', 'education', attribute='dev_id', value=dev.id)        
        skills = db.sql(f'Select * From skills where skill_id=(Select id From dev_skills where dev_id={dev.id})')
        
        data = {
            **data,
            **dev,
            **languages,
            **certificate,
            **education,
            **skills,
        }

        
    if user.is_hiring_manager:
        data = {
            **data,
            'is_active': True,            
        }

    return dict(data)
