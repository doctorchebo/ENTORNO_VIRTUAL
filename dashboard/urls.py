from django.urls import path
from . import views
from django.views.generic import TemplateView
from . import plotly_app

urlpatterns =[
    path('', views.dashboard ,name='dashboard')
]