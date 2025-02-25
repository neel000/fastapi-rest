from ..common import INSTANCE_NOT_FOUND, QUERY_NOT_FOUND
from fastapi import status
import asyncio
from sqlalchemy.engine.row import Row
from fastapi_rest.views.generic.mixin.handle_row_data import HandleRowData

class UpdateMixin(HandleRowData):
    models = None
    refresh = True

    def perform_update(self, status, instance):
        return self.handle_data(instance)
    
    def __response(self, schema, instance):
        
        instance = self.handle_row_data(instance)
        _status, instance = schema.save(
            session=self.session, instance=instance, refresh=self.refresh
        )

        # print(instance)

        # if not _status:
        #     self.status_code=status.HTTP_400_BAD_REQUEST
        #     return {"message":instance}
        
        # data = self.perform_update(status=_status, instance=instance)
        # return data
        return {}
        

    def put(self):
        schema, message = asyncio.run(self.request_handle_schema())
        
        if not schema:
            self.status_code=status.HTTP_400_BAD_REQUEST
            return {"message":str(message)}
                
        data = self.get_object()
        
        if data in [INSTANCE_NOT_FOUND, QUERY_NOT_FOUND]:
            self.status_code=status.HTTP_404_NOT_FOUND
            return {"message":f"{self.models.__name__} with {self.lookup_fields}:{self.get_instance_data()} is not found!"}, 
                
        return self.__response(schema, instance=data)
    
         
    def patch(self):
        data = self.get_object()
        if data in [INSTANCE_NOT_FOUND, QUERY_NOT_FOUND]:
            self.status_code=status.HTTP_404_NOT_FOUND
            return {
                "message":f"{self.models.__name__} with {self.lookup_fields}:{self.get_instance_data()} is not found!"
                }
            
        schema, message = asyncio.run(self.request_handle_schema(partial=data.__dict__))
        if not schema:
            self.status_code=status.HTTP_400_BAD_REQUEST
            return {"message":str(message)}
                
        return self.__response(schema, instance=data)

class AsyncUpdateMixin:
    models = None
    
    async def perform_update(self, *args, **kwargs):
        return
    
    async def __response(self, schema, instance):
        session = await self.session
        _status, instance = await schema.async_save(
            session=session, instance=instance, refresh=False
        )
        
        await session.close()

        if not _status:
            self.status_code=status.HTTP_400_BAD_REQUEST
            return {"message":instance}
        
        await self.perform_update(status=_status, instance=instance)
        return instance.model_dump()
        
    async def put(self):
        schema, message = await self.request_handle_schema()
        
        if not schema:
            self.status_code=status.HTTP_400_BAD_REQUEST
            return {"message":str(message)}
                
        data = await self.get_object()
        
        if data in [INSTANCE_NOT_FOUND, QUERY_NOT_FOUND]:
            self.status_code=status.HTTP_404_NOT_FOUND
            return {"message":f"{self.models.__name__} with {self.lookup_fields}:{self.get_instance_data()} is not found!"}, 
                
        return await self.__response(schema, instance=data)

    async def patch(self):
        data = await self.get_object()
        if data in [INSTANCE_NOT_FOUND, QUERY_NOT_FOUND]:
            self.status_code=status.HTTP_404_NOT_FOUND
            return {
                "message":f"{self.models.__name__} with {self.lookup_fields}:{self.get_instance_data()} is not found!"
                }
            
        schema, message = await self.request_handle_schema(partial=data.__dict__)
        if not schema:
            self.status_code=status.HTTP_400_BAD_REQUEST
            return {"message":str(message)}
                
        return await self.__response(schema, instance=data)
        
   