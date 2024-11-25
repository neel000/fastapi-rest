from .base import ViewSet, AsyncViewSet
from .update_mixin import UpdateMixin, AsyncUpdateMixin
from ..mixin.queryset_mixin import QuerySetMixin, AsyncQuerySetMixin
from ..mixin.serializer_mixin import SerializerMixin, SerializerValidationMixin
from ..mixin.instance_mixin import InstanceMixin, AsyncInstanceMixin


class UpdateView(
    UpdateMixin, ViewSet, 
    QuerySetMixin, InstanceMixin, 
    SerializerMixin, SerializerValidationMixin
    ):...

class AsyncUpdateView(
    AsyncUpdateMixin, AsyncViewSet,
    AsyncQuerySetMixin, AsyncInstanceMixin,
    SerializerMixin, SerializerValidationMixin
):...