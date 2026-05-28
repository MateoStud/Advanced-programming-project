"""
forecast_service.py - The compound interest calculation.

Kept separate from the DAO because the DAO is for "loading and saving"
and this is for "calculating". One responsibility per class.

Formula:    final_value = amount * (1 + rate/100) ** years
With TER:   rate = expected_return - TER
"""

from dataclasses import dataclass
from typing import List

from etf_app.domain.models import ETF


@dataclass
class Forecast:
    """Holds the result of a forecast calculation."""
    anlagebetrag: float           # invested amount
    endwert: float                # final value after N years
    gewinn: float                 # endwert - anlagebetrag
    gewinn_prozent: float         # gewinn as percent of investment
    jahre: int                    # investment period
    effektive_rendite: float      # rate used in the formula
    werte_pro_jahr: List[float]   # value at year 0, 1, ..., N (chart)


class ForecastService:
    """Calculates compound interest forecasts."""

    def calculate(self, etf: ETF, anlagebetrag: float, jahre: int,
                  ter_abziehen: bool = True) -> Forecast:
        """Return a Forecast object for the given inputs."""
        # Input checks - the UI also validates, but the service must
        # be safe to call from anywhere (tests, future code).
        if anlagebetrag <= 0:
            raise ValueError("Anlagebetrag muss grösser als 0 sein.")
        if jahre < 1:
            raise ValueError("Anlagedauer muss mindestens 1 Jahr sein.")

        # Effective rate: deduct the TER if the user wants that.
        if ter_abziehen:
            rendite = etf.erwartete_rendite - etf.ter
        else:
            rendite = etf.erwartete_rendite

        # Calculate year by year so we have data for the chart.
        werte = [anlagebetrag]  # year 0 = starting amount
        for jahr in range(1, jahre + 1):
            wert = anlagebetrag * (1 + rendite / 100) ** jahr
            werte.append(wert)

        endwert = werte[-1]
        gewinn = endwert - anlagebetrag
        gewinn_prozent = gewinn / anlagebetrag * 100

        return Forecast(
            anlagebetrag=anlagebetrag,
            endwert=endwert,
            gewinn=gewinn,
            gewinn_prozent=gewinn_prozent,
            jahre=jahre,
            effektive_rendite=rendite,
            werte_pro_jahr=werte,
        )
