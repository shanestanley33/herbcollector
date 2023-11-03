from django.contrib import admin
from .models import Herb, Watering, Fertiliser, Photo

# Register your models here.
admin.site.register(Herb)
admin.site.register(Watering)
admin.site.register(Fertiliser)
admin.site.register(Photo)