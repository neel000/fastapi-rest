from bjs_sqlalchemy.filters import FilterSet
from .models import TestModel

class TestModelFilter(FilterSet):
    class Meta:
        model = TestModel
        fields = {'name', 'name__icontains'}