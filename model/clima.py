import requests
from decouple import config
from metar import Metar


URL = "http://tgftp.nws.noaa.gov/data/observations/metar/stations/SBRJ.TXT"

proxyDict = {
    "http": config('HTTP_PROXY'),
    "https": config('HTTP_PROXY')
}


def read():
    contents = requests.get(URL, proxies=proxyDict).content.decode('UTF-8')
    obs = Metar.Metar('METAR ' + contents.split('\n')[1])
    json = {
        "temperature": str(obs.temp).split(' ')[0]
    }
    return json
