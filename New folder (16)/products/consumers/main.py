from fastapi import FastAPI,APIRouter
from mongoengine import connect
app=FastAPI()

connect(db="medofin_medicine",host="localhost",port=27017)

from products.consumers.__init__ import app2
from pharmacy.retrieve_db.by_name import app3
from pharmacy.retrieve_db.by_salt import app4
from pharmacy.retrieve_db.by_symptom import app5
from pharmacy.retrieve_db.get_all_medicines import app6
app.include_router(app2)
app.include_router(app3)
app.include_router(app4)
app.include_router(app5)
app.include_router(app6)



