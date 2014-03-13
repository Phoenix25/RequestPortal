from django.db import models
from django.contrib.auth.models import User


# used to store quotes requested by the user.
class QuoteRequest(models.Model):
	source = models.ForeignKey(User, related_name="ReqSource") # the customer who requested a quote
	target = models.ForeignKey(User, related_name="ReqTarget")# the photographer whose quote the customer requested
	desc = models.CharField(max_length = 500)# description of the job/event.
	location = models.CharField(max_length = 50)# exact location of the event.
	date = models.DateField()
	event = models.CharField(max_length = 100)
	similar = models.IntegerField(max_length = 100)
	
	def __unicode__(self):
		return self.source.username + " to "+ self.target.username + " id: "+ format(self.pk)
# used to store the response to a QuoteRequest
class Quote(models.Model):
	req = models.ForeignKey(QuoteRequest) # the request associated with this response.
	target = models.ForeignKey(User, related_name="QuoteTarget")
	desc = models.CharField(max_length = 200)# description of the response(comments, additional demands etc.
	price_range = models.CharField(max_length = 100)# price quotation of the request.
	
	def __unicode__(self):
		return self.req.source.username + " to "+ self.req.target.username+" reqid: "+self.req.pk + " resid: "+format(self.pk)