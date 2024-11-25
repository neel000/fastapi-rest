from .base import ViewSet, AsyncViewSet

from fastapi_rest.views.generic.viewset.read_mixin import (
    ListMixin, AsyncListMixin,
    DetailMixin, AsyncDetailMixin,
    ListDetailMixin, AsyncListDetailMixin
)

from fastapi_rest.views.generic.mixin.queryset_mixin import (
    QuerySetMixin, AsyncQuerySetMixin,
)
from fastapi_rest.views.generic.mixin.instance_mixin import(
    InstanceMixin, AsyncInstanceMixin
)

from fastapi_rest.views.generic.mixin.serializer_mixin import (
    SerializerMixin, SerializerTODict
)


    
class ListView(
    ListMixin, ViewSet, 
    QuerySetMixin, SerializerTODict,
    SerializerMixin
    ):...

class AsyncListView(
    AsyncListMixin, AsyncViewSet, 
    SerializerTODict, AsyncQuerySetMixin, 
    SerializerMixin
):...

class DetailView(
    DetailMixin, ViewSet, 
    QuerySetMixin, InstanceMixin,
    SerializerTODict,SerializerMixin
    ):...

class AsyncDetailView(
    AsyncDetailMixin, AsyncViewSet,
    AsyncQuerySetMixin,
    AsyncInstanceMixin,
    SerializerTODict,
    SerializerMixin
    ):...

class ListDetailView(
    ListDetailMixin, ViewSet,
    QuerySetMixin, SerializerTODict,
    InstanceMixin,
    SerializerMixin
    ):...

class AsyncListDetailView(
    AsyncListDetailMixin, AsyncViewSet,
    AsyncQuerySetMixin, AsyncInstanceMixin,
    SerializerTODict, SerializerMixin
):...

