import django_filters
from .models import JobApplication


class JobApplicationFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=JobApplication.STATUS_CHOICES)
    company_name = django_filters.CharFilter(lookup_expr='icontains')
    role_title = django_filters.CharFilter(lookup_expr='icontains')
    applied_date = django_filters.DateFilter()
    applied_after = django_filters.DateFilter(field_name='applied_date', lookup_expr='gte')
    applied_before = django_filters.DateFilter(field_name='applied_date', lookup_expr='lte')

    class Meta:
        model = JobApplication
        fields = ['status', 'company_name', 'role_title', 'applied_date']