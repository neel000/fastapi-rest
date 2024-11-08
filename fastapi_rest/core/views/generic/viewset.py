from fastapi_rest.core.auth.mixin import AccessMixin
from .base import ListMixin, CreateMixin, UpdateMixin, DeleteMixin
from .mixin import (
    QuerySetMixin, SchemaValidationMixin, 
    SchemaMixin
)
from fastapi_rest.core.views import View

class ViewSet(AccessMixin, View):
    pass

class ListViewSet(
    ListMixin, ViewSet,
    QuerySetMixin, SchemaMixin
    ):
    pass 

class CreateViewSet(
    CreateMixin, ViewSet,
    SchemaMixin, SchemaValidationMixin
    ):
    pass

class UpdateViewSet(
    UpdateMixin, ViewSet, 
    QuerySetMixin, SchemaMixin, 
    SchemaValidationMixin
    ):
    pass

class DeleteViewSet(DeleteMixin, ViewSet, QuerySetMixin):
    pass 


class ModelViewSet(
    ListMixin, CreateMixin, UpdateMixin, DeleteMixin, 
    ViewSet, QuerySetMixin, SchemaValidationMixin, 
    SchemaMixin
    ):
    pass
