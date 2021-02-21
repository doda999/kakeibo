from django.contrib import admin
from .models import Expence,Category_out,Revenue,Category_in

# Register your models here.
admin.site.register(Expence)
admin.site.register(Category_out)
admin.site.register(Revenue)
admin.site.register(Category_in)