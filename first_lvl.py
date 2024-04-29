import second_lvl as sl
import multiprocessing
from time import sleep, time


def iniciar_procesos(listaJuegos):
    procesos = []
    hora_inicial = time()
    sublista1 = listaJuegos[:13]
    sublista2 = listaJuegos[13: 26]
    sublista3 = listaJuegos[26:38]
    sublista4 = listaJuegos[38:]


    #En el primer nivel de parelelismo, llamamos al segundo nivel
    p = multiprocessing.Process(target= sl.multiprocesamientoSecond,  args= sublista1)
    p.start()
    procesos.append(p)

    p = multiprocessing.Process(target= sl.multiprocesamientoSecond,  args= sublista2)
    p.start()
    procesos.append(p)

    p = multiprocessing.Process(target= sl.multiprocesamientoSecond,  args= sublista3)
    p.start()
    procesos.append(p)

    p = multiprocessing.Process(target= sl.multiprocesamientoSecond,  args= sublista4)
    p.start()
    procesos.append(p)

    for proceso in procesos:
        proceso.join()

    hora_final = time()
    print(f'Tiempo de Duración: {hora_final-hora_inicial} segundos')
  

    