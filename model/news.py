from decouple import config
import feedparser
import json
from operator import itemgetter

from app import app

proxyDict = {
    "http": config('HTTP_PROXY'),
    "https": config('HTTP_PROXY')
}


@app.route("/api/news", methods=['GET'])
def read_news():
    ebc = feedparser.parse(
        'http://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml'
    )
    valor_politica = feedparser.parse('https://www.valor.com.br/politica/rss')
    valor_brasil = feedparser.parse('https://www.valor.com.br/brasil/rss')

    arr = []

    for entry in valor_politica.entries:
        arr.append(
            {
                'source': 'Valor Econômico - Política',
                'title': entry.title,
                'summary': entry.summary,
                'href': entry.links[0].href,
                'published': entry.published,
                'published_parsed': entry.published_parsed
            }
        )

    for entry in valor_brasil.entries:
        arr.append(
            {
                'source': 'Valor Econômico - Brasil',
                'title': entry.title,
                'summary': entry.summary,
                'href': entry.links[0].href,
                'published': entry.published,
                'published_parsed': entry.published_parsed
            }
        )

    for entry in ebc.entries:
        arr.append(
            {
                'source': 'Empresa Brasil de Comunicação',
                'title': entry.title,
                'summary': entry.summary[0:200],
                'href': entry.links[0].href,
                'published': entry.published,
                'published_parsed': entry.published_parsed
            }
        )

    sorted(
        arr,
        key=itemgetter("published_parsed")
    )

    return json.dumps(arr)
