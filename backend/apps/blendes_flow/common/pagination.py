from drf_spectacular.utils import OpenApiParameter
from rest_framework.pagination import PageNumberPagination


class SmallResultsPagination(PageNumberPagination):
    """Paginacao comum para listas auxiliares e leves."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


def suggested_list_parameters():
    """Retorna parametros comuns das listas paginadas de sugestoes."""
    return [
        OpenApiParameter(
            name="page",
            description="Numero da pagina.",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="page_size",
            description="Quantidade por pagina, limitada a 50.",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="search",
            description="Busca por nome ou descricao.",
            required=False,
            type=str,
        ),
    ]
