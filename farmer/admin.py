from django.contrib import admin
from .models import Farmer
from django.contrib.auth.models import User

# registering  models from farmer.models onto admin site
admin.site.unregister(User)
admin.site.register(Farmer)