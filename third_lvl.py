import threading
import random
from bs4 import BeautifulSoup
import requests

Users = {
    '0': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2',
    '1': 'Mozilla/5.0 (Windows 95) AppleWebKit/5340 (KHTML, like Gecko) Chrome/39.0.859.0 Mobile Safari/5340',
    '2': 'Mozilla/5.0 (Windows; U; Windows NT 6.0) AppleWebKit/532.46.3 (KHTML, like Gecko) Version/4.0 Safari/532.46.3',
    '3': 'Mozilla/5.0 (Windows NT 5.01) AppleWebKit/5340 (KHTML, like Gecko) Chrome/37.0.879.0 Mobile Safari/5340',
    '4': 'Mozilla/5.0 (Windows 98) AppleWebKit/5350 (KHTML, like Gecko) Chrome/40.0.823.0 Mobile Safari/5350',
    '5': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/5360 (KHTML, like Gecko) Chrome/40.0.814.0 Mobile Safari/5360',
    '6': 'Mozilla/5.0 (Windows; U; Windows NT 5.1) AppleWebKit/533.43.6 (KHTML, like Gecko) Version/4.0.1 Safari/533.43.6',
    '7': 'Mozilla/5.0 (Windows NT 4.0; sl-SI; rv:1.9.2.20) Gecko/20160603 Firefox/36.0',
    '8': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5360 (KHTML, like Gecko) Chrome/40.0.897.0 Mobile Safari/5360',
    '9': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5340 (KHTML, like Gecko) Chrome/37.0.814.0 Mobile Safari/5340',
    '10': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7 rv:6.0; en-US) AppleWebKit/532.30.3 (KHTML, like Gecko) Version/5.0 Safari/532.30.3',
    '11': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2',
    '12': 'Mozilla/5.0 (Windows; U; Windows NT 6.0) AppleWebKit/532.46.3 (KHTML, like Gecko) Version/4.0 Safari/532.46.3',
    '13': 'Mozilla/5.0 (Windows NT 5.01) AppleWebKit/5340 (KHTML, like Gecko) Chrome/37.0.879.0 Mobile Safari/5340',
    '14': 'Mozilla/5.0 (Windows 98) AppleWebKit/5350 (KHTML, like Gecko) Chrome/40.0.823.0 Mobile Safari/5350',
    '15': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/5360 (KHTML, like Gecko) Chrome/40.0.814.0 Mobile Safari/5360',
    '16': 'Mozilla/5.0 (Windows; U; Windows NT 5.1) AppleWebKit/533.43.6 (KHTML, like Gecko) Version/4.0.1 Safari/533.43.6',
    '17': 'Mozilla/5.0 (Windows NT 4.0; sl-SI; rv:1.9.2.20) Gecko/20160603 Firefox/36.0',
    '18': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5360 (KHTML, like Gecko) Chrome/40.0.897.0 Mobile Safari/5360',
    '19': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5340 (KHTML, like Gecko) Chrome/37.0.814.0 Mobile Safari/5340',
    '20': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7 rv:6.0; en-US) AppleWebKit/532.30.3 (KHTML, like Gecko) Version/5.0 Safari/532.30.3'
}

'''Funciones para estandarizar el formato de texto de los precios de las diferentes paginas'''
def txtPrecios(txt):
    eliminar = "DesdeUSD-$"
    for i in range(len(eliminar)):
        txt = txt.replace(eliminar[i], "")
    txt = txt.replace(".", ",")
    return txt.strip() + "$"
def txtDescuentos(txt):
    eliminar = "AhoraunDemPbOF-%"
    for i in range(len(eliminar)):
        txt = txt.replace(eliminar[i], "")
    return txt.strip() + "%"

'''Scrapers con Beautiful Soup'''
def scraper_precios_dixGamer(Game):
    try:
        key = random.choice(list(Users.keys()))
        item = Users[key]
        User = {"User-agent": item}
        req = requests.get(Game.dixUrl, headers=User)
        soup = BeautifulSoup(req.content, "lxml")
        Precio = soup.find('div', {'class': 'price-wrapper'}).get_text().strip()
        Precio = txtPrecios(Precio)
        try:
            Descuento = soup.find('div', {'class': 'badge-inner secondary on-sale'}).get_text().strip()
            Descuento = txtDescuentos(Descuento)
        except:
            Descuento = "0%"
        Game.dixSale = Descuento
        Game.dixPrice = Precio
    except:
        scraper_precios_dixGamer(Game)
    return
def scraper_precios_psStore(Game):
    try:
        key = random.choice(list(Users.keys()))
        item = Users[key]
        User = {"User-agent": item}
        req = requests.get(Game.psUrl, headers=User)
        soup = BeautifulSoup(req.content, "lxml")
        Precio = soup.find('span', {'class': 'psw-h3'}).get_text().strip()
        Precio = txtPrecios(Precio)
        try:
            Descuento = soup.find('span', {'class': 'psw-m-x-3xs psw-m-y-4xs'}).get_text().strip()
        except:
            Descuento = "0 %"
        Descuento = txtDescuentos(Descuento)
        if Descuento == "%":
            Descuento = "0 %"
        Game.psSale = Descuento
        Game.psPrice = Precio
    except:
        scraper_precios_psStore(Game)
    return

'''Funcion que hace el paralelismo'''
def multiprocesamientoThird(Game):
    simpleThread = []
    NHilos = 2
    simpleThread.append(threading.Thread(target=scraper_precios_dixGamer, args=[Game]))
    simpleThread[-1].start()
    simpleThread.append(threading.Thread(target=scraper_precios_psStore, args=[Game]))
    simpleThread[-1].start()
    for i in range(NHilos):
        simpleThread[i].join()
    return