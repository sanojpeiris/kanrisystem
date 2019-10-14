from django.db import models


class TodoItem(models.Model):
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

