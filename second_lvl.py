import third_lvl as tl
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

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

def scraper_metacritic(Game, driver):
    juego = Game.metacriticUrl
    driver.get(juego)
    try:
        puntaje = driver.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/a/div/span")))
    except:
        puntaje = "Not Rated"
    Game.metacritic = puntaje.text
    driver.quit()
    return
def scraper_hltb(Game, driver2):
    juego = Game.hltbUrl
    driver2.get(juego)
    tempo = driver2.wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='global_site']/div[3]/div/div[2]/div[1]/ul/li[1]/div")))
    Game.hltb = tempo.text
    driver2.quit()
    return


def multiprocesamientoSecond(listaJuegos):
    simpleThread = []
    NHilos = 1
    for i in listaJuegos:
        driver1 = init_driver1()
        driver2 = init_driver2()
        simpleThread.append(threading.Thread(target=scraper_metacritic, args=[i, driver1]))
        simpleThread[-1].start()
        simpleThread.append(threading.Thread(target=scraper_hltb, args=[i, driver2]))
        simpleThread[-1].start()
        simpleThread.append(threading.Thread(target= tl.multiprocesamientoThird, args=[i]))
        simpleThread[-1].start()
        for i in range(NHilos):
            simpleThread[i].join()
    return
