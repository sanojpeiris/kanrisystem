from django.contrib.auth.models import User
from useractivities.userRepository.models import TaskTable
import django_filters


class TaskFilter(django_filters.FilterSet):

    class Meta:
        model = TaskTable
        fields = [
            "edit_username",
            "taskProject",
            "tasktype",
            "task",
            "time",
            "date", ]

