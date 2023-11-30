import json
from fastapi import FastAPI,APIRouter,Path,Query,Body,Depends,HTTPException
from mongoengine import connect,Q
from models import Medicines
from pydantic import BaseModel
from urllib.parse import quote_plus
import re

app3=APIRouter()



@app3.get("/get_medicines_by_salt/{salt_name}")
def get_medicines_by_salt(salt_name: str = Path(..., title="Salt Name")):
   
    escaped_salt_name = re.escape(salt_name)    #re.escape escape the special characters in the salt 
    medicines = Medicines.objects(salt_composition__iregex=f".*{escaped_salt_name}.*")    #f".*{ecaped_salt_name},*" is the regular expression pattern,it matches any part of the salt_composition
    
    # Convert the queryset to a list of dictionaries
    medicines_list = [
        {
            "med_id": medicine.med_id,
            "name": medicine.name,
            "manufacturers": medicine.manufacturers,
            "salt_composition": medicine.salt_composition,
            "medicine_type": medicine.medicine_type,
            "stock": medicine.stock,
            "primary_use": medicine.primary_use,
            "packaging": medicine.packaging,
            "package": medicine.package,
            "quantity": medicine.quantity,
            "product_form": medicine.product_form,
            "mrp": medicine.mrp,
            "country_of_origin": medicine.country_of_origin
        }
        for medicine in medicines
    ]
    
    if not medicines_list:
        raise HTTPException(status_code=404, detail="No medicines found with the specified salt.")

    return {"medicines": medicines_list}



