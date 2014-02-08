from django.db import models
from django.contrib.auth.models import User

import datetime

def make_str(lst):
	ret = []
	for i in lst:
		ret.append((format(i),format(i)))
	return ret
		
class UserData(models.Model):
	user = models.OneToOneField(User)
	address = models.CharField(max_length=200)
	# add other fields...