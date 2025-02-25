from ..common import INSTANCE_NOT_FOUND, QUERY_NOT_FOUND

class CommonInstance:
    lookup_fields = "id"

    def get_instance_data(self):
        return self.kwargs.get("pk")

    def _instance(self):
        if not hasattr(self.models, self.lookup_fields):
            return None
        
        attr = getattr(self.models, self.lookup_fields)
        instance = self.get_instance_data()

        if instance:
            query = self.get_queryset().filter(attr==instance)
            return query
        
        return None

class InstanceMixin(CommonInstance):

    def get_object(self):
        instance = self._instance()
        if not instance:
            return INSTANCE_NOT_FOUND
        data = instance.first()
        return data if data else QUERY_NOT_FOUND

class AsyncInstanceMixin(CommonInstance):
    async def get_object(self):
        instance = self._instance()
       
        if instance is None:
            return INSTANCE_NOT_FOUND
        
        session = await self.session
        results = await session.execute(instance)
        await session.close()
        data = results.scalars().first()
        return data if data else QUERY_NOT_FOUND
