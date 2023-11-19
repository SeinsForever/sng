from django.contrib import admin

from .models import Structure, Cdng, Debits, History_plan

admin.site.register(Structure)
admin.site.register(Cdng)
admin.site.register(Debits)
admin.site.register(History_plan)


# Register your models here.
