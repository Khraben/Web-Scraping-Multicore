#@Autores:
#            Kevin Jiménez
#            Kimberly Lumbi
#            Hector Guillen

import first_lvl as fl
import xml.etree.ElementTree as ET
import json
import os, sys

xmlDoc = ET.parse("games.xml")
data = xmlDoc.getroot()

'''Declaro el diccionario para posteriormente agregarle datos para crear el JSON,
ademas tambien declaro variables de tipo lista para almacenas los datos de los juegos'''
DicJSON = {}
DicJSON['juegos'] = []

'''Lista de objetos tipo juego'''
listaJuegos = []

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
    fl.iniciar_procesos(listaJuegos)
    llenarDIC()
    crearJSON(DicJSON['juegos'])
    exit()