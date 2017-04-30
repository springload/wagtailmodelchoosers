import rest_framework.pagination as pagination
from rest_framework.response import Response


class GenericModelPaginator(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'page': self.page.number,
            'num_pages': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
        })
