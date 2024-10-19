from django.urls import path
from . import views

urlpatterns = [
    path('api/nba-props/', views.get_nba_props, name='nba_props'),
]