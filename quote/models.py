from django.db import models
from django.contrib.auth.models import User


# used to store quotes requested by the user.
class QuoteRequest(models.Model):
	source = models.ForeignKey(User, related_name="Customer") # the customer who requested a quote
	target = models.ForeignKey(User, related_name="Photographer")# the photographer whose quote the customer requested
	desc = models.CharField(max_length = 50)# description of the job/event.
	location = models.CharField(max_length = 50)# exact location of the event.
	
# used to store the response to a QuoteRequest
class Quote(models.Model):
	req = models.ForeignKey(QuoteRequest) # the request associated with this response.
	desc = models.CharField(max_length = 200)# description of the response(comments, additional demands etc.
	price_range = models.CharField(max_length = 100)# price quotation of the request.