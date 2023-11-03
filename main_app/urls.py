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
  path('herbs/<int:herb_id>/add_photo/', views.add_photo, name='add_photo'),
  path('herbs/<int:herb_id>/assoc_fertiliser/<int:fertiliser_id>/', views.assoc_fertiliser, name='assoc_fertiliser'),
  path('herbs/<int:herb_id>/unassoc_fertiliser/<int:fertiliser_id>/', views.unassoc_fertiliser, name='unassoc_fertiliser'),
  path('fertilisers/', views.FertiliserList.as_view(), name='fertilisers_index'),
  path('fertilisers/<int:pk>/', views.FertiliserDetail.as_view(), name='fertilisers_detail'),
  path('fertilisers/create/', views.FertiliserCreate.as_view(), name='fertilisers_create'),
  path('fertilisers/<int:pk>/update/', views.FertiliserUpdate.as_view(), name='fertilisers_update'),
  path('fertilisers/<int:pk>/delete/', views.FertiliserDelete.as_view(), name='fertilisers_delete'),
]