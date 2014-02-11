from django.db import models
from django.contrib.auth.models import User

import datetime

# model to store User data (customers.. not photographers.)
class UserData(models.Model):
	user = models.OneToOneField(User)
	address = models.CharField(max_length=200)
	# add other fields...