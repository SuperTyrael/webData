from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('list_modules/', views.list_modules, name='list_modules'),
    path('view/', views.view, name='view'),
    path('average/', views.average, name='average'),
    path('rating/', views.rating, name='rating'),
]
