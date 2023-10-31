from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('herbs/', views.herbs_index, name='index'),
  path('herbs/<int:herb_id>/', views.herbs_detail, name='detail'),
]