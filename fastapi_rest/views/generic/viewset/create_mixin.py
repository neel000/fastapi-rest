from fastapi import status
import asyncio
from fastapi_rest.views.generic.mixin.handle_row_data import HandleRowData

class CreateMixin(HandleRowData):
    models = None
    refresh = True
    
    def perform_create(self, status, instance):
        return self.handle_data(instance)

    def post(self):
        schema, message = asyncio.run(self.request_handle_schema())
        if not schema:
            self.status_code=status.HTTP_400_BAD_REQUEST
            return {"message":str(message)}, 
                
        _status, instance = schema.save(session=self.session, refresh=self.refresh)

        if not _status:
            self.status_code=status.HTTP_400_BAD_REQUEST
            return {"message":instance}
                
        self.status_code = status.HTTP_201_CREATED
        data = self.perform_create(status=_status, instance=instance)
        return data
        
class AsyncCreateMixin:
    models = None
    
    async def perform_create(self, *args, **kwargs):
        return

    async def post(self):
        schema, message = await self.request_handle_schema()
        
        if not schema:
            self.status_code=status.HTTP_400_BAD_REQUEST
            return {"message":str(message)}, 
    
        session = await self.session
        _status, instance = await schema.async_save(session=session)
        await session.close()

        if not _status:
            self.status_code=status.HTTP_400_BAD_REQUEST
            return {"message":instance}
                
        self.status_code = status.HTTP_201_CREATED
        await self.perform_create(_status=_status, instance=instance)
        return instance.model_dump()

