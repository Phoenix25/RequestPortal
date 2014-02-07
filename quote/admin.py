from django.contrib import admin
from quote.models import QuoteRequest
from quote.models import Quote

admin.site.register(QuoteRequest)
admin.site.register(Quote)
# Register your models here.
