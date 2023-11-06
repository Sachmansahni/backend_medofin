from mongoengine import Document,StringField,IntField
class users (Document):
    username=StringField()
    password=StringField()
    user_id=IntField()
    otp=IntField()
