from django.contrib import admin
from .models import CompanyProfile, UserProfile, User

admin.site.register(CompanyProfile)
admin.site.register(UserProfile)
admin.site.register(User)
