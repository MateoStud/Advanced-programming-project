"""
compare_page.py - The comparison page.

The user picks several ETFs and sees a table + multi-line chart.
"""

from nicegui import ui

from etf_app.data_access.dao import ETFDAO
from etf_app.services.forecast_service import ForecastService
from etf_app.ui.common import navigation


def compare_page(dao: ETFDAO, service: ForecastService) -> None:
    """Build the comparison page."""
    ui.label("Vergleich mehrerer ETFs").classes("text-3xl font-bold mb-4")
    navigation()

    # Need at least 2 ETFs to make a comparison meaningful.
    etfs = dao.list_all()
    if len(etfs) < 2:
        ui.label("Für einen Vergleich werden mindestens 2 ETFs benötigt.") \
            .classes("text-gray-500 italic")
        return

    options = {e.id: f"{e.name} ({e.symbol})" for e in etfs}

    # === Input form ============================================
    with ui.card().classes("w-full mb-4"):
        ui.label("Eingaben").classes("text-xl font-semibold")

        # multiple=True lets the user pick more than one ETF.
        etf_select = ui.select(options=options, label="ETFs",
                               multiple=True) \
            .props("use-chips").classes("w-full")

        with ui.row().classes("w-full gap-4"):
            amount_input = ui.number("Anlagebetrag", value=10000,
                                     format="%.2f").classes("flex-grow")
            years_input = ui.number("Anlagedauer (Jahre)", value=10,
                                    format="%.0f", min=1,
                                    max=60).classes("flex-grow")

        ter_check = ui.checkbox("TER von der Rendite abziehen",
                                value=True)
        result_box = ui.column().classes("w-full mt-4")

        def compare() -> None:
            """Handler for the 'compare' button."""
            result_box.clear()
            selected = etf_select.value or []

            if len(selected) < 2:
                ui.notify("Bitte mindestens 2 ETFs auswählen.",
                          type="warning")
                return

            # Calculate a forecast for each selected ETF.
            try:
                rows = []
                for etf_id in selected:
                    etf = dao.get_by_id(etf_id)
                    forecast = service.calculate(
                        etf=etf,
                        anlagebetrag=float(amount_input.value or 0),
                        jahre=int(years_input.value or 0),
                        ter_abziehen=ter_check.value,
                    )
                    rows.append((etf, forecast))
            except ValueError as ve:
                ui.notify(str(ve), type="warning")
                return

            with result_box:
                _show_result(rows, int(years_input.value or 0))

        ui.button("Vergleichen", on_click=compare) \
            .props("color=primary").classes("mt-2")


def _show_result(rows, jahre: int) -> None:
    """Render the comparison table and the multi-line chart."""

    # === Table ==================================================
    with ui.card().classes("w-full"):
        ui.label("Prognose im Vergleich").classes("text-lg font-semibold")
        columns = [
            {"name": "name", "label": "ETF", "field": "name",
             "align": "left"},
            {"name": "rendite", "label": "Effektive Rendite p.a. (%)",
             "field": "rendite"},
            {"name": "anfang", "label": "Anlagebetrag",
             "field": "anfang"},
            {"name": "ende", "label": "Endwert", "field": "ende"},
            {"name": "gewinn", "label": "Gewinn", "field": "gewinn"},
            {"name": "gewinn_p", "label": "Gewinn (%)",
             "field": "gewinn_p"},
        ]
        table_rows = [{
            "name": etf.name,
            "rendite": f"{f.effektive_rendite:.2f}",
            "anfang": f"{f.anlagebetrag:,.2f}",
            "ende": f"{f.endwert:,.2f}",
            "gewinn": f"{f.gewinn:+,.2f}",
            "gewinn_p": f"{f.gewinn_prozent:+.2f}",
        } for etf, f in rows]
        ui.table(columns=columns, rows=table_rows).classes("w-full")

    # === Chart ==================================================
    with ui.card().classes("w-full mt-4"):
        ui.label("Wertentwicklung im Vergleich") \
            .classes("text-lg font-semibold")
        jahre_labels = [f"Jahr {i}" for i in range(jahre + 1)]
        series = [{
            "name": etf.name,
            "type": "line",
            "data": [round(w, 2) for w in f.werte_pro_jahr],
            "smooth": True,
        } for etf, f in rows]
        ui.echart({
            "tooltip": {"trigger": "axis"},
            "legend": {"data": [s["name"] for s in series], "bottom": 0},
            "xAxis": {"type": "category", "data": jahre_labels},
            "yAxis": {"type": "value", "name": "Wert", "scale": True},
            "series": series,
            "grid": {"left": 70, "right": 20, "top": 30, "bottom": 60},
        }).classes("w-full h-96")
