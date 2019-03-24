from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Movies(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    creation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    fav = models.BooleanField()

    class Meta:
        ordering = ['creation']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title