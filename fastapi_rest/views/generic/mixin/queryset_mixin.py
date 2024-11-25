from sqlalchemy.future import select

class QuerySetMixin:
    def get_queryset(self):
        return self.session.query(self.models)

class AsyncQuerySetMixin:
    def get_queryset(self):
        return select(self.models)