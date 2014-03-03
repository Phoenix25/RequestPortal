
from query.models import PGRData
from django.contrib.auth.models import User
def basic_pgr(request):
	pgrdata_pk = request.GET['pk']
	return {'pgr': PGRData.objects.filter(user = User.objects.filter(pk = request.GET['pk'] ) [0] ) [0]}