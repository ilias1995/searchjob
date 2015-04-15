import django_filters
from models import Job


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['name_town', 'jobtype']

