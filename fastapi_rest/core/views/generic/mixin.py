INSTANCE_NOT_FOUND = "INSTANCE_NOT_FOUND"
QUERY_NOT_FOUND = "QUERY_NOT_FOUND"

class QuerySetMixin:
    lookup_fields = "id"
    
    def get_instance_data(self):
        return self.kwargs.get("instance")
    
    def get_queryset(self):
        return self.session.query(self.models)

    async def get_object(self):
        attr = getattr(self.models, self.lookup_fields)
        instance = self.get_instance_data()
        if not instance:
            return INSTANCE_NOT_FOUND
        queryset = self.get_queryset()
        data = queryset.filter(attr==instance).first()
        return data if data else QUERY_NOT_FOUND
        
class SchemaMixin:
    schema_class = None
    def get_schema_class(self):
        return self.schema_class

class SchemaValidationMixin:

    async def __handle_payload(self, partial):
        
        content_type = self.request.headers.get("Content-Type")

        if not content_type:
            payload = None

        elif content_type == "application/json":
            payload = await self.request.json()

        elif content_type.startswith("multipart/form-data"):
            data = await self.request.form()
            payload = data._dict
        else:
            payload = None

        if partial:
            schema = self.get_schema_class()
            new_payload = schema(**partial).dict()
            new_payload.update(**payload)
            return new_payload
        return payload

    async def request_handle_schema(self, partial=None):
        payload = await self.__handle_payload(partial)
        
        if payload is None:
            return None, "Content type is invalid"
        
        try:
            schema_class = self.get_schema_class()
            return schema_class(**payload), None
        except Exception as e:
            return None, e

