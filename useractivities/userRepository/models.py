from django.db import models


class TaskTable(models.Model):
    edit_username = models.TextField()
    taskProject = models.TextField()
    tasktype = models.TextField()
    task = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class TaskMessage(models.Model):
    edit_username = models.TextField(null=True)
    spec_user = models.TextField()
    message = models.TextField()
    visible = models.BooleanField(default=True)
    notification = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    objects = models.Manager()


class Kintai(models.Model):
    edit_username = models.TextField(null=True)
    type = models.TextField(null=True)
    teiji = models.TextField(null=True)
    overtime = models.TextField(null=True)
    Date = models.DateField(null=True, blank=False, auto_now_add=True)
    created_month = models.CharField(max_length=100, null=True, blank=False)
    Month = models.CharField(max_length=100, null=True, blank=False)
    time = models.TimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    kakunin = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)


class Btrip(models.Model):
    edit_username = models.TextField(null=True)
    type = models.TextField(null=True)
    B_money = models.TextField(null=True)
    gout = models.TextField(null=True)
    Date = models.DateField(null=True, blank=False, auto_now_add=True)
    created_month = models.CharField(max_length=100, null=True, blank=False)
    Month = models.CharField(max_length=100, null=True, blank=False)
    time = models.TimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    kakunin = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

class Chat(models.Model):
    username = models.TextField(null=True)
    chat = models.TextField(null=True)
    room = models.TextField(null=True)
    time = models.DateTimeField(auto_now_add=True)

class jinkenhi(models.Model):
    edit_username = models.TextField(null=True)
    user_id = models.IntegerField(null=True)
    department = models.TextField(null=True)
    product_id = models.IntegerField(null=True)
    itemname = models.TextField(null=True)
    kaigai = models.TextField(null=True)
    percentage = models.IntegerField(null=True)
    Date = models.DateField(null=True, blank=False, auto_now_add=True)
    created_month = models.CharField(max_length=100, null=True, blank=False)
    Month = models.CharField(max_length=99, null=True, blank=False)
    time = models.TimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    kakunin = models.BooleanField(default=False)