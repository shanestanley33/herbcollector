from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Herb
from .forms import WateringForm

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
  watering_form = WateringForm()
  return render(request, 'herbs/detail.html', {
    'herb': herb, 'watering_form': watering_form
  })

class HerbCreate(CreateView):
  model = Herb
  fields = '__all__'

class HerbUpdate(UpdateView):
  model = Herb
  fields = ['type', 'description']

class HerbDelete(DeleteView):
  model = Herb
  success_url = '/herbs'

def add_watering(request, herb_id):
  # create a ModelForm instance using 
  # the data that was submitted in the form
  form = WateringForm(request.POST)
  # validate the form
  if form.is_valid():
    # We want a model instance, but
    # we can't save to the db yet
    # because we have not assigned the
    # herb_id FK.
    new_watering = form.save(commit=False)
    new_watering.herb_id = herb_id
    new_watering.save()
  return redirect('detail', herb_id=herb_id)