from django.contrib import admin
from .models import Member


@admin.register(Member)
class ProfileAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ['first_name', 'last_name', 'date_of_birth',
                    'email', 'followers', 'membername', 'id']
