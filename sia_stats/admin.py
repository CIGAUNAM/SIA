from django.contrib import admin

# Register your models here.

from .models import SIAYearModelCounter, SIAUserModelCounter

admin.site.register(SIAYearModelCounter)
admin.site.register(SIAUserModelCounter)
