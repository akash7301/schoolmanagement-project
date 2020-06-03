from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Receipt)
