from fastapi_rest.views import View, AsyncView
from fastapi_rest.auth.mixin import AccessMixin, AsyncAccessMixin

class ViewSet(AccessMixin, View):...

class AsyncViewSet(AsyncAccessMixin, AsyncView):...