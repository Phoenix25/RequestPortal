from django.contrib import admin
from review.models import Review, ReviewToken
# Register your models here.


admin.site.register(Review)
admin.site.register(ReviewToken)