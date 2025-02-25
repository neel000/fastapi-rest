from fastapi_rest.views.generic.viewset.base import ViewSet, AsyncViewSet
from .create_mixin import CreateMixin, AsyncCreateMixin
from ..mixin.serializer_mixin import SerializerMixin, SerializerValidationMixin
from ..mixin.queryset_mixin import QuerySetMixin, AsyncQuerySetMixin

class CreateView(
    CreateMixin, ViewSet, QuerySetMixin,
    SerializerMixin, SerializerValidationMixin
):...

class AsyncCreateView(
    AsyncCreateMixin, AsyncViewSet,AsyncQuerySetMixin,
    SerializerMixin, SerializerValidationMixin
):...