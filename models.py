from mongoengine import Document, StringField, IntField

class Medicines(Document):
    med_id = IntField()
    name = StringField()
    manufacturers = StringField()
    salt_composition = StringField()
    medicine_type = StringField()
    stock = StringField()
    primary_use = StringField()
    packaging = StringField()
    package = StringField()
    quantity = IntField()
    product_form = StringField()
    mrp = IntField()
    country_of_origin = StringField()
