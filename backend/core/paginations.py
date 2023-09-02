from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class LimitPagination(PageNumberPagination):
    page_size = settings.NUM_OBJECTS_ON_PAGE
    page_size_query_param = 'limit'
