from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=32)
