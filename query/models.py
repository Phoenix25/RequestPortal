from django.db import models
from django.contrib.auth.models import User

# Create your models here.

type_choices = (
('1','Wedding Photographer'),
('2','Event Photographer')
# more types to come.
)

class PGRData(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=50)
	desc = models.CharField(max_length=300)
	city = models.CharField(max_length=50)
	type = models.CharField(max_length=50, choices = type_choices)
	email = models.EmailField(max_length = 100)
	