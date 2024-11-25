from .base import ViewSet, AsyncViewSet
from .create_mixin import CreateMixin, AsyncCreateMixin
from ..mixin.serializer_mixin import SerializerMixin, SerializerValidationMixin


class CreateView(
    CreateMixin, ViewSet, 
    SerializerMixin, SerializerValidationMixin
):...

class AsyncCreateView(
    AsyncCreateMixin, AsyncViewSet,
    SerializerMixin, SerializerValidationMixin
):...