import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Herb, Fertiliser, Photo
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
  id_list = herb.fertilisers.all().values_list('id')
  fertilisers_herb_doesnt_have = Fertiliser.objects.exclude(id__in=id_list)
  watering_form = WateringForm()
  return render(request, 'herbs/detail.html', {
    'herb': herb, 'watering_form': watering_form
    'fertilisers': fertilisers_herb_doesnt_have
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

class FertiliserList(ListView):
  model = Fertiliser

class FertiliserDetail(DetailView):
  model = Fertiliser

class FertiliserCreate(CreateView):
  model = Fertiliser
  fields = '__all__'

class FertiliserUpdate(UpdateView):
  model = Fertiliser
  fields = ['name', 'color']

class FertiliserDelete(DeleteView):
  model = Fertiliser
  success_url = '/fertilisers'

def assoc_fertiliser(request, herb_id, fertiliser_id):
  Herb.objects.get(id=herb_id).fertilisers.add(fertiliser_id)
  return redirect('detail', herb_id=herb_id)

def unassoc_fertiliser(request, herb_id, fertiliser_id):
  Herb.objects.get(id=herb_id).fertilisers.remove(fertiliser_id)
  return redirect('detail', herb_id=herb_id)

def add_photo(request, herb_id):
  # photo-file maps to the "name" attr on the <input>
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # Need a unique "key" (filename)
    # It needs to keep the same file extension
    # of the file that was uploaded (.png, .jpeg, etc.)
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, cat_id=herb_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', herb_id=herb_id)