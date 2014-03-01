from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
	pgr = models.ForeignKey(User, related_name="Customer1")
	source = models.ForeignKey(User, related_name="Photographer1")
	rating = models.IntegerField(choices=((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')))
	desc = models.CharField(max_length = 300)
	
class ReviewToken(models.Model):
	user = models.ForeignKey(User, related_name="Customer2")
	pgr = models.ForeignKey(User, related_name="Photographer2")
	active = models.BooleanField(default='true')