from fastapi_rest.views.generic.viewset.base import ViewSet, AsyncViewSet

from fastapi_rest.views.generic.viewset.read_mixin import(
    ListDetailMixin, AsyncListDetailMixin
)
from fastapi_rest.views.generic.viewset.create_mixin import(
    CreateMixin, AsyncCreateMixin
)
from fastapi_rest.views.generic.viewset.update_mixin import(
    UpdateMixin, AsyncUpdateMixin
)
from fastapi_rest.views.generic.viewset.delete_mixin import(
    DeleteMixin, AsyncDeleteMixin
)

from fastapi_rest.views.generic.mixin.instance_mixin import (
    InstanceMixin, AsyncInstanceMixin
)
from fastapi_rest.views.generic.mixin.queryset_mixin import(
    QuerySetMixin, AsyncQuerySetMixin
)
from fastapi_rest.views.generic.mixin.serializer_mixin import (
    SerializerMixin, SerializerTODict, SerializerValidationMixin
)

class ModelViewSet(
    ListDetailMixin, CreateMixin, UpdateMixin, DeleteMixin, ViewSet,
    QuerySetMixin, SerializerTODict,
    InstanceMixin,SerializerValidationMixin,
    SerializerMixin
    ):...

class AsyncModelViewSet(
    AsyncListDetailMixin, AsyncCreateMixin, AsyncUpdateMixin,
    AsyncDeleteMixin, AsyncViewSet, AsyncQuerySetMixin, AsyncInstanceMixin,
    SerializerMixin, SerializerTODict, SerializerValidationMixin

):...

