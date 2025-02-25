
class HandleRowData:
    def handle_row_data(self, data):
        return data
    
    def handle_data(self, instance):
        if self.refresh:return instance.model_dump()
        data = self.get_queryset().filter(self.models.id==instance).first()
        data = self.handle_row_data(data)
        serializer = self.serializer_class(**data.__dict__)
        return serializer.model_dump()