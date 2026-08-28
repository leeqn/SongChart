from .api import api
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('api/',api.urls),
    path('scrobbles/',views.scrobbles,name='scrobbles'),
    path('analytics/',views.analytics,name='analytics'),
    path('settings/',views.analytics,name='settings'),
]
