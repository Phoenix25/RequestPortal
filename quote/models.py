from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class QuoteRequest(models.Model):
	source = models.ForeignKey(User, related_name="Customer")
	target = models.ForeignKey(User, related_name="Photographer")
	desc = models.CharField(max_length = 50)
	location = models.CharField(max_length = 50)
	
class Quote(models.Model):
	req = models.ForeignKey(QuoteRequest)
	desc = models.CharField(max_length = 200)
	price_range = models.CharField(max_length = 100)