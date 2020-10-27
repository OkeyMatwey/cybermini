from django.contrib import admin
from .models import Location, Nodes, Schedule

admin.site.register(Location)
admin.site.register(Nodes)
admin.site.register(Schedule)