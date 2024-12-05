from django.urls import re_path

from . import consumers

ws_urlpatterns = [
    re_path(r'TableData/', consumers.TableData.as_asgi()),
    re_path(r'TableDataOpen/', consumers.TableDataOpen.as_asgi()),
]