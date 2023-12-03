from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('<str:user>/', views.search, name='search'),
    path('report/', views.report, name='report'),
    path('list/', views.list, name='list'),
]
