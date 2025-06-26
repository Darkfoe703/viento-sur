from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math


class CustomPageNumberPagination(PageNumberPagination):
    # TODO: Configurar el tamaño de página según tus necesidades.
    # En prod. dejar en 20
    page_size = 5

    def get_paginated_response(self, data):
        total_pages = math.ceil(self.page.paginator.count / self.page_size)

        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": total_pages,
                "current_page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
