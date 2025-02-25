from bjs_sqlalchemy.serializers import Serializer as ModelSerializer, BaseSerializer
from .models import TestModel, Category, SubCategory
from typing import Optional
from datetime import datetime
from sqlalchemy.engine.row import Row
from pydantic import model_validator

class TestModelSerializer(ModelSerializer):
    name:str
    age:int

    class Meta:
        models = TestModel
    
    class Config:
        from_attributes=True

class CategorySerializer(ModelSerializer):
    name:str
    is_active:Optional[bool] = False
    created_at:Optional[datetime] = None
    total_subcategory:Optional[int] = 0

    @model_validator(mode='before')
    def get_total_subcategory(cls, values):
        if values.__class__ == Row:
            instance = values[0]
            instance.total_subcategory = values.total_subcategory
            return instance
        return values

    class Meta:
        models = SubCategory

    class Config:
        from_attributes=True

class CategoryDetailSerializer(BaseSerializer):
    id:int
    name:str
    is_active:Optional[bool] = False

    class Config:
        from_attributes=True

class SubCategorySerializer(ModelSerializer):
    name:str
    category_id:int
    is_active:Optional[bool] = False
    created_at:Optional[datetime] = None
    category:Optional[CategoryDetailSerializer] = None

    class Meta:
        models = SubCategory
        extra_keys = {'category'}

    class Config:
        from_attributes=True
    
    def is_valid(self, session, payload):
        category_id = payload.get('category_id')
        error = []
        if not session.query(Category).filter(Category.id==category_id).first():
            error.append({"category_id":"Invalid Category ID"})
        
        if len(payload.get('name')) < 5:
            error.append({"name":"Name should be minimum 5 character."})
        if error:
            return False, error
        return super().is_valid(session, payload)