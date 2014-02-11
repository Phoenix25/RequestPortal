from django.db import models
from django.contrib.auth.models import User

# Create your models here.

type_choices = (
('1','Wedding Photographer'),
('2','Event Photographer')
# more types to come.
)

# model for associating photographer data with the user object
class PGRData(models.Model):
	user = models.OneToOneField(User)	# the user object to link to.
	name = models.CharField(max_length=50)
	desc = models.CharField(max_length=300)	# description of the photographer
	city = models.CharField(max_length=50) # city field used for searching.
	type = models.CharField(max_length=50, choices = type_choices)# type of photographer
	email = models.EmailField(max_length = 100) # email id.. although it's a redundant field....
	