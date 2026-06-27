from django.contrib import admin
from .models import Driver, Load, Truck, Trailer, Customer

admin.site.register(Driver)
admin.site.register(Load)
admin.site.register(Truck)
admin.site.register(Trailer)
admin.site.register(Customer)
