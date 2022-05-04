from django.urls import path
from . import views

urlpatterns = [
    path('', views.supers_list),
    path('<int:pk>/', views.super_detail),
    path('all/', views.supers_list_all)
]