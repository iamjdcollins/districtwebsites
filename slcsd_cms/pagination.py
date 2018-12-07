from collections import OrderedDict, namedtuple

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CMSPageNumberPagination(PageNumberPagination):
    max_page_size = 50
    page_size_query_param = 'records'

    def get_paginated_response(self, data):
        total_records = self.page.paginator.count
        page = self.page.number
        page_size = self.get_page_size(self.request)
        first_record = (self.page.number - 1) * page_size + 1
        last_record = min(first_record + page_size - 1, total_records)
        number_pages = self.page.paginator.num_pages
        next_page = page + 1 if page < number_pages else None
        prev_page = page - 1 if page > 1 else None
        return Response(OrderedDict([
            ('total_records', total_records),
            ('page', page),
            ('number_pages', number_pages),
            ('page_size', page_size),
            ('first_record', first_record),
            ('last_record', last_record),
            ('next_page', next_page),
            ('prev_page', prev_page),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))
