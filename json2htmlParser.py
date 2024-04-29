import  json
from jinja2 import Environmet, FileSystemLoader

with open("gamesJSON.json", "r") as f:
    games = json.load(f)

fileLoader  = FileSystemLoader("plantillas")
env = Environmet(loader= fileLoader)

rendered = env.get_templete("games.html").render(games = games, title= "Juegos")

# Escribir el HTML en un archivo index.html
fileName = "index.html"
with open(f"./site/{fileName}", "w") as f:
    f.write(rendered)

    