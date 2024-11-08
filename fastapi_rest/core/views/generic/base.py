from fastapi_rest.core.views import JSONResponse, status
from ...pagination import PageNoPagination
from sqlalchemy import asc, desc
from fastapi_rest.core.schemas import pagination_response_schema 
from .mixin import QUERY_NOT_FOUND, INSTANCE_NOT_FOUND


class ListMixin:
    models = None
    pagination_class = PageNoPagination
    order_by = []
    filter_class = None

    @property
    def __order_by(self):
        data = ()
        for item in self.order_by:
            if item.startswith("-"):
                item = item[1:]
                data+=(desc(getattr(self.models, item)),)
            else:
                data+=(asc(getattr(self.models, item)),)
        return data

    def get_filter_data(self):
        instance = self.kwargs.get("instance")
        if instance or not self.filter_class:
            return self.get_queryset()
        filter_query = self.filter_class(params=self.request.query_params, queryset=self.get_queryset()).qs
        return filter_query

    async def __list_prepare_data(self):
        queryset = self.get_filter_data().order_by(*self.__order_by)
        data = await PageNoPagination(params=self.request.query_params, queryset=queryset).main()
        return data

    async def prepare_data(self):
        instance = self.get_instance_data()
        data = await self.get_object() if instance else await self.__list_prepare_data()
        return data
    
    def serialize_to_dict_data(self, data, schema=None,):
        schema = schema if schema else self.get_schema_class()
        return schema(**data).dict()
    
    async def __list_serialize_data(self):
        data = await self.prepare_data()
        _schema_class = self.get_schema_class()
        schema_class=pagination_response_schema(_schema_class)
        response_model = self.serialize_to_dict_data(data=data, schema=schema_class,)
        return response_model if response_model["pagination"] else response_model["results"]

    async def retrieve(self):
        data = await self.prepare_data()
        if data in [INSTANCE_NOT_FOUND, QUERY_NOT_FOUND]:
            return JSONResponse(
                content={"message":f"{self.models.__name__} with {self.lookup_fields}:{self.get_instance_data()} is not found!"}, 
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return self.serialize_to_dict_data(data=data.__dict__)
        
    async def get(self):
        instance = self.get_instance_data()
        if instance:
            return await self.retrieve()
        return await self.__list_serialize_data()

class CreateMixin:
    models = None
    
    async def perform_create(self, *args, **kwargs):
        return

    async def post(self):
        schema, message = await self.request_handle_schema()
        if not schema:
            return JSONResponse(
                content={"message":str(message)}, 
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        _status, instance = await schema.save(session=self.session)

        if not _status:
            return JSONResponse(
                content={"message":instance}, 
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        self.status_code = status.HTTP_201_CREATED
        await self.perform_create()
        return instance.dict()

class UpdateMixin:
    models = None
    
    async def perform_update(self, *args, **kwargs):
        return
    
    async def __response(self, schema, instance):
        _status, instance = await schema.save(session=self.session, instance=instance)

        if not _status:
            return JSONResponse(
                content={"message":instance}, 
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        await self.perform_update()
        return instance.dict()

    async def put(self):
        schema, message = await self.request_handle_schema()
        
        if not schema:
            return JSONResponse(
                content={"message":str(message)}, 
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = await self.get_object()
        if data in [INSTANCE_NOT_FOUND, QUERY_NOT_FOUND]:
            return JSONResponse(
                content={"message":f"{self.models.__name__} with {self.lookup_fields}:{self.get_instance_data()} is not found!"}, 
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return await self.__response(schema, instance=data)
        
    async def patch(self):
        data = await self.get_object()
        if data in [INSTANCE_NOT_FOUND, QUERY_NOT_FOUND]:
            return JSONResponse(
                content={"message":f"{self.models.__name__} with {self.lookup_fields}:{self.get_instance_data()} is not found!"}, 
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        schema, message = await self.request_handle_schema(partial=data.__dict__)
        if not schema:
            return JSONResponse(
                content={"message":str(message)}, 
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        return await self.__response(schema, instance=data)
    
class DeleteMixin:
    models = None
    async def delete(self):
        data = await self.get_object()
        if data in [INSTANCE_NOT_FOUND, QUERY_NOT_FOUND]:
            return JSONResponse(
                content={"message":f"{self.models.__name__} with {self.lookup_fields}:{self.get_instance_data()} is not found!"}, 
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        await data.delete(session=self.session)
        self.status_code = status.HTTP_204_NO_CONTENT
        return

