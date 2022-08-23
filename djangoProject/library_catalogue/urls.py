from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:title>/', views.detail, name='detail'),
    path('<str:title>/results/', views.results, name='results')
]