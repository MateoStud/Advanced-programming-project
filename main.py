"""
main.py
-------
Einstiegspunkt der NiceGUI-Anwendung.

Hier werden die einzelnen Seiten ueber @ui.page registriert und der
Webserver gestartet. Beim Start wird einmal die Datenbank initialisiert.
"""

from nicegui import ui

from database import create_db_and_tables
from views import etf_seite, detail_seite, vergleich_seite


@ui.page("/")
def startseite():
    etf_seite()


@ui.page("/detail")
def detail():
    detail_seite()


@ui.page("/vergleich")
def vergleich():
    vergleich_seite()


# Datenbank und Tabellen anlegen, falls noch nicht vorhanden
create_db_and_tables()

# Webserver starten. reload=False ist wichtig, damit die Datenbank
# nicht doppelt initialisiert wird.
ui.run(title="ETF-Vergleicher", reload=False)
