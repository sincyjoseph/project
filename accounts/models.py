from django.db import models

# Create your models here.
class UserDetailsModel(models.Model):
    fname = models.CharField(max_length=255, default='NULL')
    lname = models.CharField(max_length=255, default='NULL')
    mname = models.CharField(max_length=255, default='NULL')
    dateofbirth = models.DateField(max_length=10)
    email = models.EmailField(max_length=255)
    gender = models.CharField(max_length=50, default='NULL')
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/%Y/%m/%d/', default=0)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    objects = models.Manager()

