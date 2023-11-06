import json
from fastapi import FastAPI,Path,Query,Body,Depends,HTTPException
from models import users
from mongoengine import connect
from mongoengine.queryset.visitor import Q 
from random import random
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import timedelta,datetime
from jose import jwt
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username,password):
    try:
        user=json.load(users.objects.get(username=username).to_json())
        password_check=pwd_context.verify(["password"])
        return password_check
    except users.DoesNotExist:
        return False 

app=FastAPI()
connect(db="mycollection",host="localhost",port=27017)

SECRET_KEY='COPY THE SECRET KEY HERE CREATED BY USING opensslm rand -hex 32'
ALGORITHM="HS256"
def create_access_token(data:dict,expires_delta:timedelta):
    to_encode=data.copy()
    expire=datetime.utcnow()+expires_delta
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token")
def login(form_data:OAuth2PasswordRequestForm=Depends()):
     username=form_data.username
     password=form_data.password
     if authenticate_user(username,password):
        access_token=create_access_token(
            data={"sub":username},expires_delta=timedelta(minutes=30)
        )
        return{"access_token":access_token,"token_type":"bearer"}
     else:
        raise HTTPException(status_code=400,detail="incorrect username or password")
     

@app.get("/")
def home(token:str=Depends(oauth2_scheme)):
    return{"message":"hello world"}




@app.get("/get_all_users")
def get_all_users():
    Users=users.objects().to_json()
    user_list=json.loads(Users)
    return{"users":user_list}




@app.get("/get_users/{user_id}")
def get_user(user_id:int=Path(...,gt=0)):
    User=users.objects.get(user_id=user_id)
    user_dict={
        "user_id":User.user_id,
        "username":User.username,
        "password":User.password
    }
    return {"user":user_dict.username}


@app.get("/get_otp/{username}")
def get_employee(username):                        
    user=users.objects.get(username=username)             
    returnotp=0
    if user:
        returnotp=user.otp
        newotp=otp()
        user.otp = newotp
        user.save()
        return {"message": "OTP updated successfully"}
    return {"message": "User not found"}
    return returnotp



@app.get("/get_userpassword/{username}")
def get_employee(username):                        
	user=users.objects.get(username=username)             
	employee_dict={
		"password":user.password
		}
	return employee_dict



class NewUser(BaseModel):
    username:str
    password:str
    user_id:int
    otp:int

def otp():
     return random()*1000000

@app.post("/add_user")
def add_user(user:NewUser):
	new_user=users(username=user.username,
				password=get_password_hash(user.password),
				user_id=user.user_id,
				otp=otp())
	new_user.save()
	return{"message":"user added successfully"}

#   updating the otp 
@app.put("/update_otp/{username}")
def update_otp(username: str):
    user = users.objects.get(username=username)
    if user:
        newotp=otp()
        user.otp = newotp
        user.save()
        return {"message": "OTP updated successfully"}
    return {"message": "User not found"}
