from rest_framework import filters


class CustomSearch(filters.SearchFilter):
    search_param = "search"
