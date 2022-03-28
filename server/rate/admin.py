from django.contrib import admin

# Register your models here.
from .models import ModuleInstance, Professor, Module, Rating

admin.site.register(Professor)  
admin.site.register(Module)
admin.site.register(ModuleInstance)
admin.site.register(Rating)