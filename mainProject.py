#@Autores:
#            Kevin Jiménez
#            Kimberly Lumbi
#            Hector Guillen

import first_lvl as fl
import xml.etree.ElementTree as ET
import json
import os, sys
import multiprocessing
from time import sleep, time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import random
from bs4 import BeautifulSoup
import requests

xmlDoc = ET.parse("games.xml")
data = xmlDoc.getroot()

'''Declaro el diccionario para posteriormente agregarle datos para crear el JSON,
ademas tambien declaro variables de tipo lista para almacenas los datos de los juegos'''
DicJSON = {}
DicJSON['juegos'] = []

'''Lista de objetos tipo juego'''
listaJuegos = []

#Third Level
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

# Second Level
PATH = "C:\Program Files (x86)\chromedriver.exe"
op = webdriver.ChromeOptions()
op.add_argument('headless')

def init_driver1():
    driver1 = webdriver.Chrome(PATH, options=op)
    driver1.wait = WebDriverWait(driver1, 10)
    return driver1
def init_driver2():
    driver2 = webdriver.Chrome(PATH, options=op)
    driver2.wait = WebDriverWait(driver2, 10)
    return driver2

def txtTiempo(txt):
    eliminar = "MainStoryHus"
    for i in range(len(eliminar)):
        txt = txt.replace(eliminar[i], "")
    txt = txt.replace(".", ",")
    return txt.strip() + "h"

def scraper_metacritic(Game):
    try:
        key = random.choice(list(Users.keys()))
        item = Users[key]
        User = {"User-agent": item}
        req = requests.get(Game.metacriticUrl, headers=User)
        soup = BeautifulSoup(req.content, "lxml")
        Score = soup.find('span', {'itemprop': 'ratingValue'}).get_text().strip()
        Game.metacritic = Score
    except: 
        scraper_metacritic(Game)
    return

def scraper_hltb(Game):
    try:
        key = random.choice(list(Users.keys()))
        key = random.choice(list(Users.keys()))
        item = Users[key]
        User = {"User-agent": item}
        req = requests.get(Game.hltbUrl, headers=User)
        soup = BeautifulSoup(req.content, "lxml")
        Time = soup.find('li', {'class': 'short time_100'}).get_text().strip()
        Time = txtTiempo(Time)
        Game.hltb = Time
    except: 
        scraper_hltb(Game)
    return


def multiprocesamientoSecond(listaJuegos):
    simpleThread = []
    NHilos = 150
    hora_inicial = time()
    for Game in listaJuegos:
        simpleThread.append(threading.Thread(target=scraper_metacritic, args=[Game]))
        simpleThread[-1].start()
        simpleThread.append(threading.Thread(target=scraper_hltb, args=[Game]))
        simpleThread[-1].start()
        simpleThread.append(threading.Thread(target= multiprocesamientoThird, args=[Game]))
        simpleThread[-1].start()
        
    for i in range(NHilos):
            simpleThread[i].join()

    llenarDIC()
    crearJSON(DicJSON['juegos'])
    hora_final = time()
    print(f'Tiempo de Duración: {hora_final-hora_inicial} segundos')

    return

#First Level

def iniciar_procesos(listaJuegos):
    procesos = []
    hora_inicial = time()
    sublista1 = listaJuegos[:13]
    sublista2 = listaJuegos[13: 26]
    sublista3 = listaJuegos[26:38]
    sublista4 = listaJuegos[38:]
    #En el primer nivel de parelelismo, llamamos al segundo nivel

    for i in range(12):
        if i != 12:
            p1 = multiprocessing.Process(target= multiprocesamientoSecond,  args= sublista1[i])
            p1.start()
            procesos.append(p1)

            p2 = multiprocessing.Process(target= multiprocesamientoSecond,  args= sublista2[i])
            p2.start()
            procesos.append(p2)

            p3 = multiprocessing.Process(target= multiprocesamientoSecond,  args= sublista3[i])
            p3.start()
            procesos.append(p3)

            p4 = multiprocessing.Process(target= multiprocesamientoSecond,  args= sublista4[i])
            p4.start()
            procesos.append(p4)

        else:
            p3 = multiprocessing.Process(target= multiprocesamientoSecond,  args= sublista3[i])
            p3.start()
            procesos.append(p3)

            p4 = multiprocessing.Process(target= multiprocesamientoSecond,  args= sublista4[i])
            p4.start()
            procesos.append(p4)

        for proceso in procesos:
            proceso.join()

    llenarDIC()
    crearJSON(DicJSON['juegos'])
    hora_final = time()
    print(f'Tiempo de Duración: {hora_final-hora_inicial} segundos')


'''Clase para guardar obejtos tipo juego desde la info del xml'''
class Juegos:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.consola = ""
        self.metacriticUrl = ""
        self.hltbUrl = ""
        self.dixUrl = ""
        self.psUrl = ""
        self.image = ""
        self.dixPrice = ""
        self.dixSale = ""
        self.psPrice = ""
        self.psSale = ""
        self.hltb = ""
        self.metacritic = ""

    def setInfo(self, id, name, consola, metacriticUrl, hltbUrl, dixUrl, psUrl, image):
        self.id = id
        self.name = name
        self.consola = consola
        self.metacriticUrl = metacriticUrl
        self.hltbUrl = hltbUrl
        self.dixUrl = dixUrl
        self.psUrl = psUrl
        self.image = image

'''Funcion para rellenar el diccionario para la creacion del json'''
def llenarDIC():
    for i in listaJuegos:
        DicJSON['juegos'].append({
            'id' : i.id,
            'name': i.name,
            'consola': i.consola,
            'metacritic': i.metacritic,
            'hltb': i.hltb,
            'precioPSstore': i.psPrice,
            'descuentoPSstore': i.psSale,
            'precioDixGamer': i.dixPrice,
            'descuentoDixGamer': i.dixSale,
            'imagen' : i.image})

'''Función para crear el archivo JSON'''
def crearJSON(data, fileName = "gamesJSON.json"):
    with open(fileName, "w") as f:
        json.dump(data, f)

'''Funcion que crea los objetos'''
def crearObjetos():
    for i in data:
        J = Juegos()
        id = i.attrib['id']
        name = i[0].text
        consola = i[1].text
        metacritic = i[2].text
        hltb = i[3].text
        dixUrl = i[4].text
        psUrl = i[5].text
        image = i[6].text
        J.setInfo(id, name, consola, metacritic, hltb, dixUrl, psUrl, image)
        listaJuegos.append(J)
    return


if __name__ == '__main__':
    crearObjetos()
    multiprocesamientoSecond(listaJuegos)
    
