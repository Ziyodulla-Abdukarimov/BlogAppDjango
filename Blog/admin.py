from django.contrib import admin
from .models import CustomUser, Client, Staffs, AdminHOD

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Client)
admin.site.register(Staffs)
admin.site.register(AdminHOD)