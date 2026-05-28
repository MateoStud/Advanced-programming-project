"""
main.py - Entry point of the application.

Steps:
1. Set up the database (creates etf_app.db with 10 ETFs on first run).
2. Build the DAO and the service.
3. Register the three pages.
4. Start the NiceGUI web server.

Run with:
    python main.py
"""

from nicegui import ui

from etf_app.data_access.db import Database
from etf_app.data_access.dao import ETFDAO
from etf_app.services.forecast_service import ForecastService
from etf_app.ui.etf_page import etf_page
from etf_app.ui.forecast_page import forecast_page
from etf_app.ui.compare_page import compare_page


# === 1. Set up the database ====================================
database = Database()
database.init()  # create tables + seed 10 ETFs if empty

# === 2. Build the DAO and the service ==========================
dao = ETFDAO(database.engine)
service = ForecastService()


# === 3. Register the three pages ===============================
@ui.page("/")
def start():
    etf_page(dao)


@ui.page("/renditerechner")
def renditerechner():
    forecast_page(dao, service)


@ui.page("/vergleich")
def vergleich():
    compare_page(dao, service)


# === 4. Start the web server ===================================
# reload=False so the database is not initialised twice.
ui.run(title="ETF-Vergleicher", reload=False)
