from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
WATERINGS = (
  ('M', 'Monday'),
  ('F', 'Friday'),
)

# Create your models here.
class Fertiliser(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('fertilisers_detail', kwargs={'pk': self.id})


class Herb(models.Model):
  name = models.CharField(max_length=100)
  type = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  fertilisers = models.ManyToManyField(Fertiliser)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # Changing this instance method
  # does not impact the database, therefore
  # no makemigrations is necessary
  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'herb_id': self.id})

  def watered_for_the_week(self):
    return self.watering_set.filter(date=date.today()).count() >= len(WATERINGS)

class Watering(models.Model):
  date = models.DateField('Watering Date')
  water = models.CharField(
    max_length=1,
    choices=WATERINGS,
    default=WATERINGS[0][0]
  )
  # Create a herb_id FK
  herb = models.ForeignKey(
    Herb,
    on_delete=models.CASCADE
  )

  def __str__(self):
    return f"{self.get_water_display()} on {self.date}"

  class Meta:
    ordering = ['-date']

class Photo(models.Model):
  url = models.CharField(max_length=200)
  herb = models.ForeignKey(Herb, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for herb_id: {self.herb_id} @{self.url}"