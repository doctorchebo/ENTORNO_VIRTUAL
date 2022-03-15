from . import views
from django.urls import path

urlpatterns = [
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('',views.homePage,name='home')
]