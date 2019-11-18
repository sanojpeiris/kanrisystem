from django.db import models

class TaskTable(models.Model):
    edit_username = models.TextField()
    taskProject=models.TextField()
    tasktype = models.TextField()
    task=models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

# def __unicode___(self):
#     return self.edit_username

class TaskMessage(models.Model):
    edit_username = models.TextField(null=True)
    spec_user = models.TextField()
    message=models.TextField()
    visible=models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)