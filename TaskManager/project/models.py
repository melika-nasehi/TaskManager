from django.db import models
from aaa.models import CustomUser


# Create your models here.


class Project (models.Model):
    title = models.CharField(max_length=100)

    public = "PB"
    private = "PV"
    access_choices = {
        public : "Public" ,
        private : "Private" ,
    }
    access = models.CharField(max_length=2, choices=access_choices)

    users = models.ManyToManyField(CustomUser)

    personal = "PR"
    work = "WR"
    team = "TM"
    category_choices = {
        personal : "Personal",
        work : "Work",
        team : "Team",
    }
    category = models.CharField(max_length=2, choices=category_choices)

    is_archived = models.BooleanField(default=False)

    startDate = models.DateField()
    endDate = models.DateField()

    theme = models.CharField(max_length=50)

    def __str__(self):
        return f"title : {self.title} , access : {self.access} , users : {self.users}"