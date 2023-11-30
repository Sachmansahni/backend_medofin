import json
from fastapi import FastAPI,APIRouter,Path,Query,Body,Depends,HTTPException
from mongoengine import connect,Q
from models import Medicines
from pydantic import BaseModel
from urllib.parse import quote_plus
import re

app6=APIRouter()


@app6.get("/get_all_medicines")
def get_all_medicines():
    medicines=Medicines.objects().to_json()
    medicine_list=json.loads(medicines)
    return{"Medicines":medicine_list}