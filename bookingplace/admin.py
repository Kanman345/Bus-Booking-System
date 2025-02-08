from django.contrib import admin
from .models import CustomUser, Bus, Route, Booking, Wallet
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Booking)
admin.site.register(Wallet)