from django.urls import path
from . import views

urlpatterns = [
    path('api/wnba-props/', views.get_wnba_props, name='wnba_props'),
]
