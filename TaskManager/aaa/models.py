from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import TextField


# Create your models here.


class CustomUser (AbstractUser):

    owner = "OW"
    manager = "MN"
    contributor = "CT"
    viewer = "VW"
    roles_choices = {
        owner : "Owner",
        manager : "Manager",
        contributor : "Contributor",
        viewer : "Viewer",
    }
    role = models.CharField(max_length=2, choices=roles_choices, default="VW" )

    def __str__(self):
        return "username : {0} , password : {1} , role : {2}".format(self.username, self.password, self.role)


class UserProfile(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    bio = TextField(max_length=400, null=True, blank=True)
    skills = TextField(max_length=300, null=True, blank=True)
