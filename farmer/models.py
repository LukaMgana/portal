from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from wanyama.choices import GENDER


class Farmer(models.Model):
    user                    = models.OneToOneField(User, null=True, on_delete = models.CASCADE )
    full_name               = models.CharField(max_length= 255)
    phone                   = models.CharField(max_length=244, null=True, blank=True)
    email                   = models.EmailField(_("Email"), max_length=254, null=True, blank=True)
    gender                  = models.CharField(choices = GENDER, max_length = 255)
    location                = models.CharField(max_length = 244, null=True)
    profile_image           = models.ImageField(_("Profile Image"), upload_to='profile images', null=True, blank=True)


    def __str__(self):
        return str(self.user.username)


