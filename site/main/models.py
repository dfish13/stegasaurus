"""
 This file was created on October 15th, 2016
 by Deborah Venuti

 Last updated on: October 15th, 2016
 Updated by: Deborah Venuti
"""

from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
