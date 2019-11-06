from django.db import models


class TaskItem(models.Model):
    # category = models.TextField()
    # content = models.TextField()
    # variety = models.TextField()
    edit_username = models.TextField()
    category_yesterday = models.TextField()
    category_today = models.TextField()
    category_bad = models.TextField()
    category_other = models.TextField()
    yesterday = models.TextField()
    today = models.TextField()
    bad = models.TextField()
    other = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.today

class TaskUser(models.Model):
    edit_username = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class TaskType(models.Model):
    tasktype = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    
class TaskProject(models.Model):
    taskProject=models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class Task(models.Model):
    task=models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class TaskTable(models.Model):
    edit_username = models.TextField()
    taskProject=models.TextField()
    tasktype = models.TextField()
    task=models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

# def __unicode___(self):
#     return self.edit_username