"""
 This file was created on October 15th, 2016
 by Deborah Venuti

 Contributors: Deborah Venuti, Gene Ryasnianskiy, Alexander Sumner

Last updated on: November 19, 2016
Updated by: Alexander Sumner
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Gene Ryasnianskiy added image model
class stegaImage(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.uploader.id, filename)
    
    uploader = models.ForeignKey(User, unique=False)
    FinalImage = models.ImageField(upload_to=user_directory_path)
    BaseImage = models.ImageField(upload_to=user_directory_path)
    TarFile = models.FileField(upload_to=user_directory_path)
    Created_on = models.DateTimeField(default = datetime.now)
      
#Alexander Sumner added extracted file model
class stegaExtractedFile(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.uploader.id, filename)
    
    uploader = models.ForeignKey(User, unique=False)
    file = models.FileField(upload_to=user_directory_path)

class tempFile(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.uploader.id, filename)
    
    uploader = models.ForeignKey(User, unique=False)
    file = models.FileField(upload_to=user_directory_path)