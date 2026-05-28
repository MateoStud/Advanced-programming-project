"""
etf_page.py - The start page.

Lets the user view, add and delete ETFs. Calls the DAO directly,
no extra controller layer in between.
"""

from pydantic import ValidationError
from nicegui import ui

from etf_app.data_access.dao import ETFDAO, DuplicateISINError
from etf_app.domain.models import ETF
from etf_app.ui.common import navigation


def etf_page(dao: ETFDAO) -> None:
    """Build the start page."""
    ui.label("ETF-Vergleicher").classes("text-3xl font-bold mb-4")
    navigation()

    # === Card 1: form to add a new ETF =========================
    with ui.card().classes("w-full mb-4"):
        ui.label("Neuen ETF hinzufügen").classes("text-xl font-semibold")

        # Inputs in three rows.
        with ui.row().classes("w-full gap-2"):
            name_input = ui.input("Name").classes("flex-grow")
            isin_input = ui.input("ISIN").classes("flex-grow")
            symbol_input = ui.input("Symbol").classes("flex-grow")

        with ui.row().classes("w-full gap-2"):
            kategorie_input = ui.input("Kategorie").classes("flex-grow")
            ter_input = ui.number("TER (%)", value=0.20,
                                  format="%.2f").classes("flex-grow")

        with ui.row().classes("w-full gap-2"):
            kurs_input = ui.number("Aktueller Kurs", value=100.00,
                                   format="%.2f").classes("flex-grow")
            rendite_input = ui.number("Erwartete Rendite p.a. (%)",
                                      value=7.00,
                                      format="%.2f").classes("flex-grow")

        def add_etf() -> None:
            """Handler for the 'add' button. Builds an ETF and saves it."""
            try:
                # Building the ETF triggers the Field() validation.
                etf = ETF(
                    name=(name_input.value or "").strip(),
                    isin=(isin_input.value or "").strip().upper(),
                    symbol=(symbol_input.value or "").strip().upper(),
                    kategorie=(kategorie_input.value or "").strip(),
                    ter=float(ter_input.value or 0),
                    aktueller_kurs=float(kurs_input.value or 0),
                    erwartete_rendite=float(rendite_input.value or 0),
                )
                dao.create(etf)
            except ValidationError as ve:
                # Pydantic gives one error per failed rule.
                for err in ve.errors():
                    feld = err["loc"][0]
                    ui.notify(f"{feld}: {err['msg']}", type="warning")
                return
            except DuplicateISINError as de:
                ui.notify(str(de), type="warning")
                return

            ui.notify("ETF hinzugefügt.", type="positive")
            # Reset only text fields - the numbers keep their defaults.
            name_input.value = ""
            isin_input.value = ""
            symbol_input.value = ""
            kategorie_input.value = ""
            refresh_table()

        ui.button("ETF hinzufügen",
                  on_click=add_etf).props("color=primary")

    # === Card 2: table of all ETFs =============================
    with ui.card().classes("w-full"):
        ui.label("Vorhandene ETFs") \
            .classes("text-xl font-semibold mb-2")
        table_box = ui.column().classes("w-full")

        def refresh_table() -> None:
            """Rebuild the table from the current DB state."""
            table_box.clear()
            with table_box:
                _render_table(dao)

        refresh_table()


def _render_table(dao: ETFDAO) -> None:
    """Render the ETF table with a delete button in every row."""
    etfs = dao.list_all()
    if not etfs:
        ui.label("Noch keine ETFs vorhanden.") \
            .classes("text-gray-500 italic")
        return

    columns = [
        {"name": "name", "label": "Name", "field": "name", "align": "left"},
        {"name": "isin", "label": "ISIN", "field": "isin", "align": "left"},
        {"name": "symbol", "label": "Symbol", "field": "symbol"},
        {"name": "ter", "label": "TER (%)", "field": "ter"},
        {"name": "kategorie", "label": "Kategorie", "field": "kategorie"},
        {"name": "kurs", "label": "Aktueller Kurs", "field": "kurs"},
        {"name": "rendite", "label": "Erw. Rendite p.a. (%)",
         "field": "rendite"},
        {"name": "actions", "label": "", "field": "actions"},
    ]
    rows = [{
        "id": e.id,
        "name": e.name,
        "isin": e.isin,
        "symbol": e.symbol,
        "ter": f"{e.ter:.2f}",
        "kategorie": e.kategorie,
        "kurs": f"{e.aktueller_kurs:.2f}",
        "rendite": f"{e.erwartete_rendite:.2f}",
    } for e in etfs]

    table = ui.table(columns=columns, rows=rows,
                     row_key="id").classes("w-full")

    # Custom delete button per row.
    table.add_slot("body-cell-actions", r"""
        <q-td :props="props">
            <q-btn flat dense color="negative" icon="delete"
                   @click="$parent.$emit('del', props.row)" />
        </q-td>
    """)

    def on_delete(e) -> None:
        row = e.args
        dao.delete(row["id"])
        ui.notify(f"ETF '{row['name']}' gelöscht.", type="positive")
        # Reload the page so the table refreshes.
        ui.navigate.to("/")

    table.on("del", on_delete)
