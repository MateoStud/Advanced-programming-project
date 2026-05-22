"""
detail_view.py
--------------
Die Detail-Seite: ein einzelner ETF wird ausgewaehlt, ein Anlagebetrag
und eine Anzahl Jahre festgelegt - die App zeigt, was man am Ende hat.
"""

from nicegui import ui

from database import get_session
from dao import ETFDAO
from services import RenditeService


def detail_seite() -> None:
    """Baut die Detail-Seite auf."""
    ui.label("Detail-Analyse").classes("text-3xl font-bold mb-4")

    # Navigation
    with ui.row().classes("mb-6 gap-2"):
        ui.button("Startseite",
                  on_click=lambda: ui.navigate.to("/")) \
            .props("flat color=primary")
        ui.button("Detail-Analyse",
                  on_click=lambda: ui.navigate.to("/detail")) \
            .props("flat color=primary")
        ui.button("Vergleich",
                  on_click=lambda: ui.navigate.to("/vergleich")) \
            .props("flat color=primary")

    # ETFs aus der DB holen
    with get_session() as session:
        etfs = ETFDAO(session).get_all()

    if not etfs:
        ui.label("Bitte zuerst auf der Startseite einen ETF anlegen.") \
            .classes("text-gray-500 italic")
        return

    options = {etf.id: f"{etf.name} ({etf.symbol})" for etf in etfs}

    # === Eingabe-Bereich ===
    with ui.card().classes("w-full mb-4"):
        ui.label("Eingaben").classes("text-xl font-semibold")

        etf_select = ui.select(options=options, label="ETF") \
            .classes("w-full")

        with ui.row().classes("w-full gap-4"):
            anlagebetrag_input = ui.number(
                "Anlagebetrag", value=10000, format="%.2f"
            ).classes("flex-grow")
            jahre_input = ui.number(
                "Anlagedauer (Jahre)", value=10, format="%.0f", min=1, max=60
            ).classes("flex-grow")

        ter_checkbox = ui.checkbox("TER von der Rendite abziehen",
                                   value=True)

        ergebnis_container = ui.column().classes("w-full mt-4")

        def berechnen():
            ergebnis_container.clear()

            if etf_select.value is None:
                ui.notify("Bitte einen ETF auswaehlen.", type="warning")
                return

            if (anlagebetrag_input.value is None
                    or anlagebetrag_input.value <= 0):
                ui.notify("Anlagebetrag muss groesser als 0 sein.",
                          type="warning")
                return

            if jahre_input.value is None or jahre_input.value < 1:
                ui.notify("Anlagedauer muss mindestens 1 Jahr sein.",
                          type="warning")
                return

            with get_session() as session:
                etf = ETFDAO(session).get_by_id(etf_select.value)

            service = RenditeService()
            prognose = service.berechne(
                etf=etf,
                anlagebetrag=float(anlagebetrag_input.value),
                jahre=int(jahre_input.value),
                ter_abziehen=ter_checkbox.value,
            )

            with ergebnis_container:
                _zeige_ergebnis(etf, prognose)

        ui.button("Rendite berechnen",
                  on_click=berechnen) \
            .props("color=primary").classes("mt-2")


def _zeige_ergebnis(etf, prognose) -> None:
    """Zeigt die Prognose-Zahlen und das Diagramm an."""

    # === Kennzahlen-Karten ===
    with ui.row().classes("w-full gap-4"):
        with ui.card().classes("flex-grow"):
            ui.label("Anlagebetrag").classes("text-sm text-gray-600")
            ui.label(f"{prognose.anlagebetrag:,.2f}") \
                .classes("text-2xl font-bold")
            ui.label("am Anfang").classes("text-xs text-gray-500")

        with ui.card().classes("flex-grow"):
            ui.label("Endwert").classes("text-sm text-gray-600")
            ui.label(f"{prognose.endwert:,.2f}") \
                .classes("text-2xl font-bold")
            ui.label(f"nach {prognose.jahre} Jahren") \
                .classes("text-xs text-gray-500")

        with ui.card().classes("flex-grow"):
            ui.label("Gewinn").classes("text-sm text-gray-600")
            farbe = ("text-green-600" if prognose.gewinn >= 0
                     else "text-red-600")
            ui.label(f"{prognose.gewinn:+,.2f}") \
                .classes(f"text-2xl font-bold {farbe}")
            ui.label(f"{prognose.gewinn_prozent:+.2f} %") \
                .classes("text-xs text-gray-500")

        with ui.card().classes("flex-grow"):
            ui.label("Effektive Rendite p.a.") \
                .classes("text-sm text-gray-600")
            ui.label(f"{prognose.effektive_rendite:.2f} %") \
                .classes("text-2xl font-bold")
            ui.label("nach Kosten").classes("text-xs text-gray-500")

    # === Diagramm: Wertentwicklung ueber die Jahre ===
    with ui.card().classes("w-full mt-4"):
        ui.label(f"Wertentwicklung von {etf.name}") \
            .classes("text-lg font-semibold")

        jahre_labels = [f"Jahr {i}" for i in range(prognose.jahre + 1)]

        ui.echart({
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": jahre_labels},
            "yAxis": {"type": "value", "name": "Wert", "scale": True},
            "series": [{
                "type": "line",
                "data": [round(w, 2) for w in prognose.werte_pro_jahr],
                "smooth": True,
                "areaStyle": {},
            }],
            "grid": {"left": 70, "right": 20, "top": 30, "bottom": 50},
        }).classes("w-full h-80")
