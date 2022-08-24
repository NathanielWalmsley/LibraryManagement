from django.urls import path

from . import views

app_name = 'catalogue'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:book_id>/', views.detail, name='detail'),
    path('results/', views.SearchResultsView.as_view(), name='results'),
]