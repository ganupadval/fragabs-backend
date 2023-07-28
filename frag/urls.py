from django.urls import path, include
from .views import  *
urlpatterns = [
    path('', set_data), #{'title':"", 'abstarct':"", 'data':""}
    path('get-data', get_data), #{'title':""}
    path('get-titles', get_title),
    path('delete', delete_data)
]
