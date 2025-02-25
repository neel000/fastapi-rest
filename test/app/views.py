from fastapi_rest.responses import Response
from .db import Session, AsyncSession, SessionMixin, AsyncSessionMixin
from .serializer import TestModelSerializer, TestModel, SubCategorySerializer, SubCategory, Category, CategorySerializer
from fastapi_rest.generic.viewset import ModelViewSet, AsyncModelViewSet
from fastapi_rest.views import CreateView, AsyncCreateView, UpdateView
from .filters import TestModelFilter
from fastapi_rest.views import View
from sqlalchemy import func, orm

def home(request):
    return Response(data={"name":"Home"})

async def async_view(request):
    return Response(data={"name":"Async Home"})

def session_test(request):
    db = Session()
    # print(db.bind.url)
    # count = db.query(TestModel).count()
    return Response(data={"url":str(db.bind.url)})

async def async_session_test(request):
    db = await AsyncSession()
    await db.close()
    return Response(data={"url":str(db.bind.url)})

class TestModelViewSet(ModelViewSet, SessionMixin):
    models = TestModel
    serializer_class = TestModelSerializer
    filter_class = TestModelFilter

class TestAsyncModelViewSet(AsyncModelViewSet, AsyncSessionMixin):
    models = TestModel
    serializer_class = TestModelSerializer
    filter_class = TestModelFilter

class TestCreateView(CreateView, SessionMixin):
    models = SubCategory
    serializer_class = SubCategorySerializer
    refresh = False

    def get_queryset(self):
        query = super().get_queryset().options(orm.joinedload(self.models.category))
        return query


class TestUpdateView(UpdateView, SessionMixin):
    models = Category
    serializer_class = CategorySerializer
    refresh = False

    def get_queryset(self):
        return self.session.query(
                Category, func.count(SubCategory.id).label("total_subcategory")
            ).outerjoin(
                SubCategory, SubCategory.category_id == Category.id
            ).group_by(Category.id)
    
    def handle_row_data(self, data):
        instance = data[0]
        instance.total_subcategory = data.total_subcategory
        return instance
        

    