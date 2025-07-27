from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from aaa.models import CustomUser
from project.models import Project
from django.db.models import CASCADE



# Create your models here.
#Tag, Task, SubTask, Comment , Log

class Tag (models.Model):
    title = models.CharField(max_length=20)


class Task (models.Model):
    title = models.CharField(max_length=100)
    users = models.ManyToManyField(CustomUser)
    project = models.ForeignKey(Project, on_delete=CASCADE)

    status_choice = {
        "CM" : "completed",
        "IP" : "in_progress",
        "NS" : "not_started",
    }
    status = models.CharField(max_length=2, choices=status_choice)

    priority = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        help_text="enter value between 1 and 5 :"
     )

    start_date = models.DateField()
    complete_date = models.DateField(blank=True, null=True)
    deadline = models.DateField()
    tags = models.ManyToManyField(Tag, blank=True)
    related_to = models.ManyToManyField('self', related_name="related_tasks", symmetrical=False, blank=True, null=True, default=None)
    attached_file = models.FileField(upload_to="file_attached/", blank=True,null =True, default=None)
    is_completed = models.BooleanField(default=False)




class SubTask (models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    related_task = models.ForeignKey(Task, related_name="sub_tasks", on_delete=models.CASCADE)


class Comment (models.Model):
    text = models.TextField(max_length=500)
    published_date_time = models.DateTimeField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name="comments", on_delete=CASCADE)


class Log (models.Model):
    description = models.TextField(max_length=200)
    time_date = models.DateTimeField()
    user = models.ForeignKey(CustomUser, on_delete=CASCADE)
    task = models.ForeignKey(Task, on_delete=CASCADE)


