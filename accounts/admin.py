from django.contrib import admin
from .models import UserDetailsModel


class userDetailsAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'mname', 'dateofbirth', 'email', 'gender', 'country', 'state', 'file', 'created')


# # Register your models here.
admin.site.register(UserDetailsModel, userDetailsAdmin)
