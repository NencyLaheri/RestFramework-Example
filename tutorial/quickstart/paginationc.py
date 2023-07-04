from rest_framework.pagination import CursorPagination

class custompagination(CursorPagination):

    page_size=2
    ordering='id'