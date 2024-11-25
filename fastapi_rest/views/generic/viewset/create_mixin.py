from fastapi import status
import asyncio

class CreateMixin:
    models = None
    
    def perform_create(self, *args, **kwargs):
        return

    def post(self):
        schema, message = asyncio.run(self.request_handle_schema())
        if not schema:
            self.status_code=status.HTTP_400_BAD_REQUEST
            return {"message":str(message)}, 
                
        _status, instance = schema.save(session=self.session)

        if not _status:
            self.status_code=status.HTTP_400_BAD_REQUEST
            return {"message":instance}
                
        self.status_code = status.HTTP_201_CREATED
        self.perform_create(_status=_status, instance=instance)
        return instance.model_dump()
        
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

