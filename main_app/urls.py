from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('herbs/', views.herbs_index, name='index'),
  path('herbs/<int:herb_id>/', views.herbs_detail, name='detail'),
  path('herbs/create/', views.HerbCreate.as_view(), name='herbs_create'),
  path('herbs/<int:pk>/update/', views.HerbUpdate.as_view(), name='herbs_update'),
  path('herbs/<int:pk>/delete/', views.HerbDelete.as_view(), name='herbs_delete'),
  path('herbs/<int:herb_id>/add_watering/', views.add_watering, name='add_watering'),
]