from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Frags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30, null=True)
    abstract = models.TextField(null=True)
    data = models.JSONField()
    def __str__(self):
	    return self.title
