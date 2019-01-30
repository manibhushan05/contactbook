from django_filters import rest_framework as filters

from contact.models import ContactBook


class ContactBookFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", label="Contact Book Name", lookup_expr='iexact')

    class Meta:
        model = ContactBook
        fields = ['name', ]


class ContactFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", label="Contact Name", lookup_expr='iexact')
    email = filters.CharFilter(field_name="email", label="Contact Email", lookup_expr='iexact')

    class Meta:
        model = ContactBook
        fields = ['name', 'email']
