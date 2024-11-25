from fastapi_rest import models

class TestModel(models.Model):
    __tablename__ = "test_model"
    name = models.CharField(max_length=30, unique=True)
    age = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)