from django.contrib.auth.models import User
from useractivities.userRepository.models import TodoItem
import django_filters


class TaskFilter(django_filters.FilterSet):
    # # date = django_filters.NumberFilter(field_name="date_joined", lookup_expr="year")
    # date_range = django_filters.DateRangeFilter(name='date')
    # date = django_filters.DateRangeFilter(label='Date_Range')

    class Meta:
        model = TodoItem
        fields = [
            "edit_username",
            "category_today",
            "today",
            "time",
            "date", ]
