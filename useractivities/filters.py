from django.contrib.auth.models import User
from useractivities.userRepository.models import TaskItem,TaskTable
import django_filters


class TaskFilter(django_filters.FilterSet):

    #task= django_filters.CharFilter(tasktype='2今日やること', lookup_expr='icontains', label="Put Label Here")
    # class Meta:
    #     model = TaskTable
    #     fields = [
    #         "edit_username",
    #         "taskProject",
    #         "tasktype",
    #         "task",
    #         "time",
    #         "date", ]

    class Meta:
        model = TaskTable
        exclude=['tasktype=2今日やること']
        fields = {
            'edit_username': ['exact', 'contains'],
            'taskProject': ['exact', 'contains'],
            'tasktype': ['exact', 'contains'],
            'task': ['exact', 'contains'],
            'time': ['exact', 'contains'],
            'date': ['exact', 'contains'],
        }