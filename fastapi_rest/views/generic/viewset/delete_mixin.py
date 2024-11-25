from ..common import INSTANCE_NOT_FOUND, QUERY_NOT_FOUND
from fastapi import status

class DeleteMixin:
    models = None
    def delete(self):
        data = self.get_object()
        if data in [INSTANCE_NOT_FOUND, QUERY_NOT_FOUND]:
            self.status_code=status.HTTP_404_NOT_FOUND
            return {
                "message":f"{self.models.__name__} with {self.lookup_fields}:{self.get_instance_data()} is not found!"
            }
                
        data.delete(session=self.session)
        self.status_code = status.HTTP_204_NO_CONTENT
        return

class AsyncDeleteMixin:
    models = None
    async def delete(self):
        data = await self.get_object()
        
        if data in [INSTANCE_NOT_FOUND, QUERY_NOT_FOUND]:
            self.status_code=status.HTTP_404_NOT_FOUND
            return {
                "message":f"{self.models.__name__} with {self.lookup_fields}:{self.get_instance_data()} is not found!"
            }
        
        session = await self.session
        await data.async_delete(session=session)
        await session.close()
        self.status_code = status.HTTP_204_NO_CONTENT
        return

