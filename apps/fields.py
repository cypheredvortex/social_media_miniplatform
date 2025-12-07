# apps/fields.py - SAVE THIS EXACTLY
from djongo import models
from bson import ObjectId

class CustomObjectIdField(models.ObjectIdField):
    def __init__(self, *args, **kwargs):
        kwargs['primary_key'] = True
        super().__init__(*args, **kwargs)
    
    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return ObjectId()
        return super().get_db_prep_value(value, connection, prepared)