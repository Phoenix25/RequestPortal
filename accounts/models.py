from django.db import models
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User

import datetime
#courses_list = ((),())
#institute_list = ((),())
courses = (
('B.Tech','B.Tech'),
('M.Tech','M.Tech'),
('M.S.','M.S.'),
('M.A.','M.A.'),
('M.B.A.','M.B.A.')
)
def make_str(lst):
	ret = []
	for i in lst:
		ret.append((format(i),format(i)))
	return ret
		
class UserData(models.Model):
	user = models.OneToOneField(User)
	
	address = models.CharField(max_length=200)
	institute = models.CharField( max_length=50)
	hostel_bool = models.BooleanField(default = 'TRUE')
	hostel = models.CharField(max_length = 40)
	department = models.CharField(max_length = 40)
	
	# Soft code the next line ASAP.
	# batchof = models.ChoiceField(choices = make_str(range(1955,datetime.datetime.now().year+1)))
	batchof = models.CharField(choices = make_str(range(1955,datetime.datetime.now().year+1)),max_length=10)
	graduation_date = models.DateField(default='2013-01-01')
	course = models.CharField(choices = courses,max_length = 100)