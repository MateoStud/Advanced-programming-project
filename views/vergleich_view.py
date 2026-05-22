"""
vergleich_view.py
-----------------
Die Vergleichs-Seite: mehrere ETFs auswaehlen, Anlagebetrag und Jahre
festlegen - die App zeigt eine Tabelle und ein Diagramm zum Vergleich.
"""

from nicegui import ui

from database import get_session
from dao import ETFDAO
from services import RenditeService


def vergleich_seite() -> None:
    """Baut die Vergleichs-Seite auf."""
    ui.label("Vergleich mehrerer ETFs").classes("text-3xl font-bold mb-4")

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

    with get_session() as session:
        etfs = ETFDAO(session).get_all()

    if len(etfs) < 2:
        ui.label("Fuer einen Vergleich werden mindestens 2 ETFs benoetigt.") \
            .classes("text-gray-500 italic")
        return

    options = {etf.id: f"{etf.name} ({etf.symbol})" for etf in etfs}

    # === Eingabe-Bereich ===
    with ui.card().classes("w-full mb-4"):
        ui.label("Eingaben").classes("text-xl font-semibold")

        etf_select = ui.select(options=options, label="ETFs",
                               multiple=True) \
            .props("use-chips").classes("w-full")

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

        def vergleichen():
            ergebnis_container.clear()

            ausgewaehlt = etf_select.value or []
            if len(ausgewaehlt) < 2:
                ui.notify("Bitte mindestens 2 ETFs auswaehlen.",
                          type="warning")
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

            service = RenditeService()
            vergleichsdaten = []  # Liste von (etf, prognose)

            with get_session() as session:
                etf_dao = ETFDAO(session)
                for etf_id in ausgewaehlt:
                    etf = etf_dao.get_by_id(etf_id)
                    prognose = service.berechne(
                        etf=etf,
                        anlagebetrag=float(anlagebetrag_input.value),
                        jahre=int(jahre_input.value),
                        ter_abziehen=ter_checkbox.value,
                    )
                    vergleichsdaten.append((etf, prognose))

            with ergebnis_container:
                _zeige_vergleich(vergleichsdaten,
                                 int(jahre_input.value))

        ui.button("Vergleichen", on_click=vergleichen) \
            .props("color=primary").classes("mt-2")


def _zeige_vergleich(vergleichsdaten, jahre) -> None:
    """Zeigt eine Tabelle mit Kennzahlen und ein Diagramm."""

    # === Tabelle mit Kennzahlen ===
    with ui.card().classes("w-full"):
        ui.label("Prognose im Vergleich") \
            .classes("text-lg font-semibold")

        spalten = [
            {"name": "name", "label": "ETF", "field": "name",
             "align": "left"},
            {"name": "rendite", "label": "Effektive Rendite p.a. (%)",
             "field": "rendite"},
            {"name": "anfang", "label": "Anlagebetrag", "field": "anfang"},
            {"name": "ende", "label": "Endwert", "field": "ende"},
            {"name": "gewinn", "label": "Gewinn", "field": "gewinn"},
            {"name": "gewinn_p", "label": "Gewinn (%)",
             "field": "gewinn_p"},
        ]
        rows = []
        for etf, prognose in vergleichsdaten:
            rows.append({
                "name": etf.name,
                "rendite": f"{prognose.effektive_rendite:.2f}",
                "anfang": f"{prognose.anlagebetrag:,.2f}",
                "ende": f"{prognose.endwert:,.2f}",
                "gewinn": f"{prognose.gewinn:+,.2f}",
                "gewinn_p": f"{prognose.gewinn_prozent:+.2f}",
            })

        ui.table(columns=spalten, rows=rows).classes("w-full")

    # === Diagramm: Wertentwicklung aller ETFs ===
    with ui.card().classes("w-full mt-4"):
        ui.label("Wertentwicklung im Vergleich") \
            .classes("text-lg font-semibold")

        jahre_labels = [f"Jahr {i}" for i in range(jahre + 1)]

        series = []
        for etf, prognose in vergleichsdaten:
            series.append({
                "name": etf.name,
                "type": "line",
                "data": [round(w, 2) for w in prognose.werte_pro_jahr],
                "smooth": True,
            })

        ui.echart({
            "tooltip": {"trigger": "axis"},
            "legend": {"data": [s["name"] for s in series], "bottom": 0},
            "xAxis": {"type": "category", "data": jahre_labels},
            "yAxis": {"type": "value", "name": "Wert", "scale": True},
            "series": series,
            "grid": {"left": 70, "right": 20, "top": 30, "bottom": 60},
        }).classes("w-full h-96")
