from django.shortcuts import render
from .models import Herb

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def herbs_index(request):
  herbs = Herb.objects.all()
  return render(request, 'herbs/index.html', {
    'herbs': herbs
  })

def herbs_detail(request, herb_id):
  herb = Herb.objects.get(id=herb_id)
  return render(request, 'herbs/detail.html', {
    'herb': herb
  })