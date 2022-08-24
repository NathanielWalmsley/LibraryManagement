from django.urls import path

from . import views

app_name = 'catalogue'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:book_id>/', views.detail, name='detail'),
    path('<int:book_id>/results/', views.results, name='results')
]