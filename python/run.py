from src import crearScraper

scraper=crearScraper(1990)

partidos=scraper.obtenerPartidos()

print(partidos)