from bjs_sqlalchemy.serializers import Serializer as ModelSerializer
from .models import TestModel

class TestModelSerializer(ModelSerializer):
    name:str
    age:int

    class Meta:
        models = TestModel
    
    class Config:
        from_attributes=True