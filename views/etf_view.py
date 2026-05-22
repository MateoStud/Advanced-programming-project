"""
etf_view.py
-----------
Die Startseite der Anwendung. Hier kann der Benutzer:
- neue ETFs anlegen,
- die vorhandenen ETFs in einer Tabelle sehen,
- ETFs wieder loeschen.
"""

from nicegui import ui

from database import get_session
from dao import ETFDAO


def _zeige_etf_liste(container) -> None:
    """Baut die Tabelle mit allen ETFs neu auf."""
    container.clear()
    with container:
        with get_session() as session:
            etfs = ETFDAO(session).get_all()

        if not etfs:
            ui.label("Noch keine ETFs vorhanden. Lege oben einen an.") \
                .classes("text-gray-500 italic")
            return

        zeilen = [{
            "id": etf.id,
            "name": etf.name,
            "isin": etf.isin,
            "symbol": etf.symbol,
            "ter": f"{etf.ter:.2f}",
            "kategorie": etf.kategorie,
            "kurs": f"{etf.aktueller_kurs:.2f}",
            "rendite": f"{etf.erwartete_rendite:.2f}",
        } for etf in etfs]

        spalten = [
            {"name": "name", "label": "Name", "field": "name",
             "align": "left"},
            {"name": "isin", "label": "ISIN", "field": "isin",
             "align": "left"},
            {"name": "symbol", "label": "Symbol", "field": "symbol"},
            {"name": "ter", "label": "TER (%)", "field": "ter"},
            {"name": "kategorie", "label": "Kategorie",
             "field": "kategorie"},
            {"name": "kurs", "label": "Aktueller Kurs", "field": "kurs"},
            {"name": "rendite", "label": "Erw. Rendite p.a. (%)",
             "field": "rendite"},
        ]
        ui.table(columns=spalten, rows=zeilen, row_key="id") \
            .classes("w-full")


def etf_seite() -> None:
    """Die komplette Startseite."""
    ui.label("ETF-Vergleicher").classes("text-3xl font-bold mb-4")

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

    # === Bereich: Neuen ETF anlegen ============================
    with ui.card().classes("w-full mb-4"):
        ui.label("Neuen ETF hinzufuegen").classes("text-xl font-semibold")

        with ui.row().classes("w-full gap-2"):
            name_input = ui.input("Name").classes("flex-grow")
            isin_input = ui.input("ISIN").classes("flex-grow")
            symbol_input = ui.input("Symbol").classes("flex-grow")

        with ui.row().classes("w-full gap-2"):
            kategorie_input = ui.input("Kategorie").classes("flex-grow")
            ter_input = ui.number("TER (%)", value=0.20, format="%.2f") \
                .classes("flex-grow")

        with ui.row().classes("w-full gap-2"):
            kurs_input = ui.number("Aktueller Kurs", value=100.00,
                                   format="%.2f").classes("flex-grow")
            rendite_input = ui.number("Erwartete Rendite p.a. (%)",
                                      value=7.00, format="%.2f") \
                .classes("flex-grow")

        ui.label("Hinweis: Die erwartete Rendite ist eine Annahme - "
                 "ueblich sind 5-8% fuer breite Aktien-ETFs.") \
            .classes("text-sm text-gray-600")

        def etf_hinzufuegen():
            # Pflichtfelder pruefen
            if not all([name_input.value, isin_input.value,
                        symbol_input.value, kategorie_input.value]):
                ui.notify("Bitte alle Textfelder ausfuellen.",
                          type="warning")
                return

            if kurs_input.value is None or kurs_input.value <= 0:
                ui.notify("Aktueller Kurs muss groesser als 0 sein.",
                          type="warning")
                return

            try:
                with get_session() as session:
                    dao = ETFDAO(session)
                    if dao.get_by_isin(isin_input.value):
                        ui.notify(
                            f"ETF mit ISIN {isin_input.value} existiert bereits.",
                            type="warning")
                        return
                    dao.create(
                        name=name_input.value,
                        isin=isin_input.value,
                        symbol=symbol_input.value,
                        ter=float(ter_input.value),
                        kategorie=kategorie_input.value,
                        aktueller_kurs=float(kurs_input.value),
                        erwartete_rendite=float(rendite_input.value),
                    )
                ui.notify("ETF hinzugefuegt.", type="positive")

                # Felder leeren
                name_input.value = ""
                isin_input.value = ""
                symbol_input.value = ""
                kategorie_input.value = ""

                _zeige_etf_liste(etf_liste_container)

            except Exception as fehler:
                ui.notify(f"Fehler: {fehler}", type="negative")

        ui.button("ETF hinzufuegen", on_click=etf_hinzufuegen) \
            .props("color=primary")

    # === Bereich: Liste aller ETFs ==============================
    with ui.card().classes("w-full"):
        ui.label("Vorhandene ETFs").classes("text-xl font-semibold mb-2")
        etf_liste_container = ui.column().classes("w-full")
        _zeige_etf_liste(etf_liste_container)
