from rest_framework.pagination import PageNumberPagination


class RecipePagination(PageNumberPagination):
    page_size = 6


class LimitPagination(RecipePagination):
    page_size_query_param = 'limit'
