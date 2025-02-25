from fastapi_rest import models
from datetime import datetime, UTC
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

class TestModel(models.Model):
    __tablename__ = "test_model"
    name = models.CharField(max_length=30, unique=True)
    age = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    


class BaseModel(models.Model):
    __abstract__ = True
    name = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=False)
    created_at = Column(
        DateTime, default=datetime.now(UTC)
    )

class Category(BaseModel):
    __tablename__ = "Category"
    sub_category = relationship("SubCategory", back_populates="category", )


class SubCategory(BaseModel):
    __tablename__ = "SubCategory"
    category_id = Column(Integer, ForeignKey("Category.id"), nullable=False)
    category = relationship(Category, back_populates="sub_category")
    
    