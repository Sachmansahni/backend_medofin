import json
from fastapi import FastAPI,APIRouter,Path,Query,Body,Depends,HTTPException
from mongoengine import connect,Q
from models import Medicines
from pydantic import BaseModel
from urllib.parse import quote_plus
import re

app2=APIRouter()



@app2.get("/search_medicines")
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

