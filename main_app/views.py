import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Herb, Fertiliser, Photo
from .forms import WateringForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def herbs_index(request):
  herbs = Herb.objects.all()
  return render(request, 'herbs/index.html', {
    'herbs': herbs
  })

@login_required
def herbs_detail(request, herb_id):
  herb = Herb.objects.get(id=herb_id)
  id_list = herb.fertilisers.all().values_list('id')
  fertilisers_herb_doesnt_have = Fertiliser.objects.exclude(id__in=id_list)
  watering_form = WateringForm()
  return render(request, 'herbs/detail.html', {
    'herb': herb, 'watering_form': watering_form,
    'fertilisers': fertilisers_herb_doesnt_have
  })

class HerbCreate(LoginRequiredMixin, CreateView):
  model = Herb
  fields = '__all__'

  def form_valid(self, form):
    # self.request.user is the logged in user
    form.instance.user = self.request.user
    # Let the CreateView's form_valid method
    # do its regular work (saving the object & redirecting)
    return super().form_valid(form)

class HerbUpdate(LoginRequiredMixin, UpdateView):
  model = Herb
  fields = ['type', 'description']

class HerbDelete(LoginRequiredMixin, DeleteView):
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

class FertiliserList(LoginRequiredMixin, ListView):
  model = Fertiliser

class FertiliserDetail(LoginRequiredMixin, DetailView):
  model = Fertiliser

class FertiliserCreate(LoginRequiredMixin, CreateView):
  model = Fertiliser
  fields = '__all__'

class FertiliserUpdate(LoginRequiredMixin, UpdateView):
  model = Fertiliser
  fields = ['name', 'color']

class FertiliserDelete(LoginRequiredMixin, DeleteView):
  model = Fertiliser
  success_url = '/fertilisers'

@login_required
def assoc_fertiliser(request, herb_id, fertiliser_id):
  Herb.objects.get(id=herb_id).fertilisers.add(fertiliser_id)
  return redirect('detail', herb_id=herb_id)

@login_required
def unassoc_fertiliser(request, herb_id, fertiliser_id):
  Herb.objects.get(id=herb_id).fertilisers.remove(fertiliser_id)
  return redirect('detail', herb_id=herb_id)

@login_required
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


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # Save the user to the db
      user = form.save()
      # Automatically log in the new user
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup template
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)