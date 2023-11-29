import json
from fastapi import FastAPI,Path,Query,Body,Depends,HTTPException
from mongoengine import connect,Q
from models import Medicines
from pydantic import BaseModel
from urllib.parse import quote_plus

app=FastAPI()

connect(db="medofin_medicine",host="localhost",port=27017)

class NewMedicine(BaseModel):
    med_id:int
    name:str
    manufacturers:str
    salt_composition:str
    medicine_type:str
    stock:str
    primary_use:str
    packaging:str
    package:str
    quantity:int
    product_form:str
    mrp:int
    country_of_origin:str



@app.post("/add_medicine")
def add_medicine(medicine: NewMedicine):
    try:
        new_medicine = Medicines(
            med_id=medicine.med_id,
            name=medicine.name,
            manufacturers=medicine.manufacturers,
            salt_composition=medicine.salt_composition,
            medicine_type=medicine.medicine_type,
            stock=medicine.stock,
            primary_use=medicine.primary_use,
            packaging=medicine.packaging,
            package=medicine.package,
            quantity=medicine.quantity,
            product_form=medicine.product_form,
            mrp=medicine.mrp,
            country_of_origin=medicine.country_of_origin
        )
        new_medicine.save()
        return {"message": "Medicine added successfully", "medicine_id": str(new_medicine.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/get_all_medicines")
def get_all_medicines():
    medicines=Medicines.objects().to_json()
    medicine_list=json.loads(medicines)
    return{"Medicines":medicine_list}


from urllib.parse import quote_plus

# ...

import re

# ...

@app.get("/get_medicines_by_salt/{salt_name}")
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






@app.get("/get_medicines_by_name/{name}")
def get_medicines_by_name(name: str = Path(..., title="Name")):
   
    escaped_name = re.escape(name)   
    medicines = Medicines.objects(name__iregex=f".*{escaped_name}.*")   
    
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
        raise HTTPException(status_code=404, detail="No medicines found with the specified name.")

    return {"medicines": medicines_list}






@app.get("/get_medicines_by_symptom/{symptom}")
def get_medicines_by_symptom(symptom: str = Path(..., title="Symptom")):
   
    escaped_symptom = re.escape(symptom)    #re.escape escape the special characters in the salt 
    medicines = Medicines.objects(primary_use__iregex=f".*{escaped_symptom}.*")    #f".*{ecaped_salt_name},*" is the regular expression pattern,it matches any part of the salt_composition
    
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








@app.get("/search_medicines")
def search_medicines(
    search_query: str = Query(None, title="Search Query")
):
    # Define a query based on the provided parameter
    query = Q()

    if search_query:
        escaped_search_query = re.escape(search_query)
        query = (
            Q(salt_composition__iregex=f".*{escaped_search_query}.*") |
            Q(name__iregex=f".*{escaped_search_query}.*") |
            Q(primary_use__iregex=f".*{escaped_search_query}.*")
        )

    # Perform the database query
    medicines = Medicines.objects(query)

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
        raise HTTPException(status_code=404, detail="No medicines found with the specified criteria.")

    return {"medicines": medicines_list}
