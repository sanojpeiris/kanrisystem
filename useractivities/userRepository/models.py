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
    notification=models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    objects = models.Manager()

class Kintai(models.Model):
    edit_username = models.TextField(null=True) 
    type = models.TextField(null=True)
    teiji = models.TextField(null=True)
    overtime = models.TextField(null=True)
    Date = models.DateField(null=True, blank=False, auto_now_add=True)
    Month = models.CharField(max_length=100, null=True, blank=False) 
    time = models.TimeField(auto_now_add=True)
    done=models.BooleanField(default=False)
    kakunin=models.BooleanField(default=False)


class Btrip(models.Model):
    edit_username = models.TextField(null=True) 
    type = models.TextField(null=True)
    B_money = models.TextField(null=True)
    gout = models.TextField(null=True)
    Date = models.DateField(null=True, blank=False, auto_now_add=True)
    Month = models.CharField(max_length=100, null=True, blank=False) 
    time = models.TimeField(auto_now_add=True)
    done=models.BooleanField(default=False)
    kakunin=models.BooleanField(default=False)