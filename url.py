from app import app

from model.orgaos import (
    list_orgaos,
    list_vistas,
    list_acervo,
    list_acervo_classe,
    financeiro,
    financeiro_agrupado
)

from model.usuarios import (
    get_foto
)

from model.clima import (
    read_clima
)

from model.news import(
    read_news
)

__all__=[
    'list_orgaos',
    'list_vistas',
    'list_acervo',
    'get_foto',
    'list_acervo_classe',
    'financeiro',
    'financeiro_agrupado',
    'read_clima',
    'read_news'
]