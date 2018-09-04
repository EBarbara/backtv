import requests
from decouple import config

URL = "http://tgftp.nws.noaa.gov/data/observations/metar/stations/SBRJ.TXT"

proxyDict = {
    "http": config('HTTP_PROXY'),
    "https": config('HTTP_PROXY')
}


def read():
    print(proxyDict)
    contents = requests.get(URL, proxies=proxyDict).content
    del contents
    json = {
        "temperature": "NULL"
    }
    return json
