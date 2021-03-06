from django.db import models
from django.contrib.auth.models import User

# Create your models here.

type_choices = (
('Wedding','Wedding Photographer'),
('Event','Event Photographer')
# more types to come.
)

# model for associating photographer data with the user object
class PGRData(models.Model):
	user = models.OneToOneField(User)	# the user object to link to.
	avatar = models.ImageField(upload_to="test_folder")
	name = models.CharField(max_length=50)
	desc = models.CharField(max_length=300)	# description of the photographer
	city = models.CharField(max_length=50) # city field used for searching.
	type = models.CharField(max_length=50, choices = type_choices)# type of photographer
	email = models.EmailField(max_length = 100) # email id.. although it's a redundant field....
	
# model for storing documents associated with a photographer like portfolio images, legal documents etc.
class Document(models.Model):
	pgr = models.ForeignKey(User)
	doc = models.FileField(upload_to="repository")
	visible = models.BooleanField(default='true')
	index = models.IntegerField()