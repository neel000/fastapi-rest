class SerializerMixin:
    serializer_class = None
    def get_serializer_class(self):
        return self.serializer_class

class SerializerTODict:
    def _serialize_to_dict_data(self, data, serializer=None,):
        serializer = serializer if serializer else self.get_serializer_class()
        return serializer(**data).model_dump()

class SerializerValidationMixin:

    async def __handle_payload(self, partial):
        content_type = self.request.headers.get("Content-Type")

        if content_type is None:
            return None

        if content_type == "application/json":
            payload = await self.request.json()

        elif content_type.startswith("multipart/form-data"):
            data = await self.request.form()
            payload = data._dict
        else:
            payload = {}

        if partial:
            serializer = self.get_serializer_class()
            new_payload = serializer(**partial).model_dump()
            new_payload.update(**payload)
            return new_payload
        return payload

    async def request_handle_schema(self, partial=None):
        payload = await self.__handle_payload(partial)

        if payload is None:
            return None, "Content type is invalid"

        try:
            serializer_class = self.get_serializer_class()
            
            return serializer_class(**payload), None
        except Exception as e:
            return None, e


