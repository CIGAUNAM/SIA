from django.db import models

from nucleo.models import User

# Create your models here.

class SIAYearModelCounter(models.Model):
    model = models.CharField(max_length=20)
    users = models.ManyToManyField(User)
    year = models.IntegerField()
    counter = models.IntegerField()

    def __str__(self):
        return "{} : {}".format(self.model, str(self.year))

    class Meta:
        unique_together = ['model', 'year']
        ordering = ['model', 'year']

class SIAUserModelCounter(models.Model):
    model = models.CharField(max_length=20)
    user = models.ForeignKey(User)
    year = models.IntegerField()
    counter = models.IntegerField()

    def __str__(self):
        return "{} : {}".format(self.model, str(self.year))

    class Meta:
        unique_together = ['model', 'year']
        ordering = ['model', 'year']