from .base import ViewSet, AsyncViewSet
from .delete_mixin import DeleteMixin, AsyncDeleteMixin
from ..mixin.queryset_mixin import QuerySetMixin, AsyncQuerySetMixin
from ..mixin.instance_mixin import InstanceMixin, AsyncInstanceMixin

class DeleteView(
    DeleteMixin, ViewSet, 
    QuerySetMixin, InstanceMixin
):...

class AsyncDeleteView(
  AsyncDeleteMixin, AsyncViewSet, 
  AsyncQuerySetMixin, AsyncInstanceMixin
  ):...