from bjs_sqlalchemy.pagination import PageNoPagination
from bjs_sqlalchemy.pagination.async_pagination import (
    PageNoPagination as AsyncPageNoPagination
)
from bjs_sqlalchemy.serializers import ListPaginationSerializer
from sqlalchemy import asc, desc
from fastapi_rest.responses import status
from ..common import INSTANCE_NOT_FOUND, QUERY_NOT_FOUND


class ListCommon:

    @property
    def _order_by(self):
        data = ()
        for item in self.order_by:
            if item.startswith("-"):
                item = item[1:]
                data+=(desc(getattr(self.models, item)),)
            else:
                data+=(asc(getattr(self.models, item)),)
        return data
    
    def _get_filter_data(self):
        # instance = self.kwargs.get("instance")
        # if instance or not self.filter_class:
        #     return self.get_queryset()

        if not self.filter_class:
            return self.get_queryset()
        
        filter_query = self.filter_class(params=self.request.query_params, queryset=self.get_queryset()).qs
        return filter_query
    
    def _serialize_pagination_data(self, data):
        _serializer_class = self.get_serializer_class()
        serializer_class=ListPaginationSerializer(_serializer_class)
        response_model = self._serialize_to_dict_data(data=data, serializer=serializer_class,)
        return response_model if response_model["pagination"] else response_model["results"]

class ListMixin(ListCommon):
    models = None
    pagination_class = PageNoPagination
    order_by = []
    filter_class = None

    def _list_prepare_data(self):
        queryset = self._get_filter_data().order_by(*self._order_by)
        data = self.pagination_class(
            params=self.request.query_params, queryset=queryset
        ).main()
        return data
        
    def prepare_data(self):
        return self._list_prepare_data()
    
    
    
    def _list_serialize_data(self):
        data = self.prepare_data()
        # _serializer_class = self.get_serializer_class()
        # serializer_class=ListPaginationSerializer(_serializer_class)
        
        # response_model = self._serialize_to_dict_data(data=data, serializer=serializer_class,)
        # return response_model if response_model["pagination"] else response_model["results"]
        return self._serialize_pagination_data(data)
        
    
        
    def get(self):
        # instance = self.get_instance_data()
        # if instance:
        #     return self.retrieve()
        return self._list_serialize_data()

class AsyncListMixin(ListCommon):
    models = None
    pagination_class = AsyncPageNoPagination
    order_by = []
    filter_class = None

    async def _list_prepare_data(self):
        session = await self.session
        queryset = self._get_filter_data().order_by(*self._order_by)
        data = await self.pagination_class(
            params=self.request.query_params, queryset=queryset, session=session
        ).main()
        await session.close()
        return data

    async def prepare_data(self):
        return await self._list_prepare_data()

    async def _list_serialize_data(self):
        data = await self.prepare_data()
        return self._serialize_pagination_data(data) 
        
        

    async def get(self):
        # instance = self.get_instance_data()
        # if instance:
        #     return self.retrieve()
        return await self._list_serialize_data()

class CommonRetrieve:
    def _retrieve(self, data):
        if data in [INSTANCE_NOT_FOUND, QUERY_NOT_FOUND]:
            self.status_code=status.HTTP_404_NOT_FOUND
            return {
                "message":f"{self.models.__name__} with {self.lookup_fields}:{self.get_instance_data()} is not found!"
            }
        return self._serialize_to_dict_data(data=data.__dict__)

class DetailMixin(CommonRetrieve):
    def prepare_data(self):
        return self.get_object()

    def get(self):
        data = self.prepare_data()
        return self._retrieve(data)
    
class AsyncDetailMixin(CommonRetrieve):
    async def prepare_data(self):
        return await self.get_object()
        
    async def get(self):
        data = await self.prepare_data()
        return self._retrieve(data)

class ListDetailMixin(ListMixin, DetailMixin):

    def prepare_data(self):
        instance = self.get_instance_data()
        data = self.get_object() if instance else self._list_prepare_data()
        return data
    
    def get(self):
        instance = self.get_instance_data()
        if instance:
            data = self.prepare_data()
            return self._retrieve(data=data)
        return self._list_serialize_data()

class AsyncListDetailMixin(AsyncListMixin, AsyncDetailMixin):
    async def prepare_data(self):
        instance = self.get_instance_data()
        data = await self.get_object() if instance else await self._list_prepare_data()
        return data
    
    async def get(self):
        instance = self.get_instance_data()
        if instance:
            data = await self.prepare_data()
            return self._retrieve(data=data)
        
        return await self._list_serialize_data()

