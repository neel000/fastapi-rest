from fastapi_rest.responses import Response
from .db import Session, AsyncSession, SessionMixin, AsyncSessionMixin
from .serializer import TestModelSerializer, TestModel
from fastapi_rest.generic.viewset import ModelViewSet, AsyncModelViewSet
from .filters import TestModelFilter

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

