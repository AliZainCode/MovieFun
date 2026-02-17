from rest_framework.pagination import CursorPagination


class MoviePagination(CursorPagination):

    page_size = 20
    ordering = "-created_at"   # VERY IMPORTANT
