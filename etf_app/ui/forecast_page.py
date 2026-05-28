"""
forecast_page.py - The Renditerechner page.

The user picks one ETF, enters an amount and number of years, and
sees the projected value and a chart.
"""

from nicegui import ui

from etf_app.data_access.dao import ETFDAO
from etf_app.services.forecast_service import ForecastService, Forecast
from etf_app.domain.models import ETF
from etf_app.ui.common import navigation


def forecast_page(dao: ETFDAO, service: ForecastService) -> None:
    """Build the Renditerechner page."""
    ui.label("Renditerechner").classes("text-3xl font-bold mb-4")
    navigation()

    # Load all ETFs for the dropdown.
    etfs = dao.list_all()
    if not etfs:
        ui.label("Bitte zuerst auf der Startseite einen ETF anlegen.") \
            .classes("text-gray-500 italic")
        return

    options = {e.id: f"{e.name} ({e.symbol})" for e in etfs}

    # === Input form ============================================
    with ui.card().classes("w-full mb-4"):
        ui.label("Eingaben").classes("text-xl font-semibold")

        etf_select = ui.select(options=options,
                               label="ETF").classes("w-full")

        with ui.row().classes("w-full gap-4"):
            amount_input = ui.number("Anlagebetrag", value=10000,
                                     format="%.2f").classes("flex-grow")
            years_input = ui.number("Anlagedauer (Jahre)", value=10,
                                    format="%.0f", min=1,
                                    max=60).classes("flex-grow")

        ter_check = ui.checkbox("TER von der Rendite abziehen",
                                value=True)

        # Container where the result will appear.
        result_box = ui.column().classes("w-full mt-4")

        def calculate() -> None:
            """Handler for the 'calculate' button."""
            result_box.clear()

            # ETF must be picked.
            if etf_select.value is None:
                ui.notify("Bitte einen ETF auswählen.", type="warning")
                return

            # The service raises ValueError for bad numeric input.
            try:
                etf = dao.get_by_id(etf_select.value)
                forecast = service.calculate(
                    etf=etf,
                    anlagebetrag=float(amount_input.value or 0),
                    jahre=int(years_input.value or 0),
                    ter_abziehen=ter_check.value,
                )
            except ValueError as ve:
                ui.notify(str(ve), type="warning")
                return

            with result_box:
                _show_result(etf, forecast)

        ui.button("Rendite berechnen", on_click=calculate) \
            .props("color=primary").classes("mt-2")


def _show_result(etf: ETF, forecast: Forecast) -> None:
    """Render the four KPI cards and the chart."""

    # === KPI cards =============================================
    with ui.row().classes("w-full gap-4"):
        with ui.card().classes("flex-grow"):
            ui.label("Anlagebetrag").classes("text-sm text-gray-600")
            ui.label(f"{forecast.anlagebetrag:,.2f}") \
                .classes("text-2xl font-bold")
            ui.label("am Anfang").classes("text-xs text-gray-500")

        with ui.card().classes("flex-grow"):
            ui.label("Endwert").classes("text-sm text-gray-600")
            ui.label(f"{forecast.endwert:,.2f}") \
                .classes("text-2xl font-bold")
            ui.label(f"nach {forecast.jahre} Jahren") \
                .classes("text-xs text-gray-500")

        with ui.card().classes("flex-grow"):
            ui.label("Gewinn").classes("text-sm text-gray-600")
            # Green for profit, red for loss.
            colour = ("text-green-600" if forecast.gewinn >= 0
                      else "text-red-600")
            ui.label(f"{forecast.gewinn:+,.2f}") \
                .classes(f"text-2xl font-bold {colour}")
            ui.label(f"{forecast.gewinn_prozent:+.2f} %") \
                .classes("text-xs text-gray-500")

        with ui.card().classes("flex-grow"):
            ui.label("Effektive Rendite p.a.") \
                .classes("text-sm text-gray-600")
            ui.label(f"{forecast.effektive_rendite:.2f} %") \
                .classes("text-2xl font-bold")
            ui.label("nach Kosten").classes("text-xs text-gray-500")

    # === Chart ==================================================
    with ui.card().classes("w-full mt-4"):
        ui.label(f"Wertentwicklung von {etf.name}") \
            .classes("text-lg font-semibold")
        jahre_labels = [f"Jahr {i}" for i in range(forecast.jahre + 1)]
        ui.echart({
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": jahre_labels},
            "yAxis": {"type": "value", "name": "Wert", "scale": True},
            "series": [{
                "type": "line",
                "data": [round(w, 2) for w in forecast.werte_pro_jahr],
                "smooth": True,
                "areaStyle": {},
            }],
            "grid": {"left": 70, "right": 20, "top": 30, "bottom": 50},
        }).classes("w-full h-80")
