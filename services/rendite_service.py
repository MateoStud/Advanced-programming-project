"""
rendite_service.py
------------------
Hier liegt die Geschaeftslogik der Anwendung: die Renditeprognose.

Wir trennen das bewusst von den DAOs, weil DAOs nur Daten holen/speichern
sollen und nicht rechnen. So bleibt der Code uebersichtlich (Single
Responsibility Principle).

Die Berechnung verwendet die Zinseszins-Formel:

    Endwert = Anlagebetrag * (1 + Rendite/100) ^ Jahre

Wir koennen optional auch die TER (jaehrliche Kosten) abziehen, dann lautet
die Formel:

    Endwert = Anlagebetrag * (1 + (Rendite - TER)/100) ^ Jahre
"""

from dataclasses import dataclass
from models import ETF


@dataclass
class Prognose:
    """Buendelt das Ergebnis einer Prognose-Berechnung.

    Eine Dataclass ist wie eine kleine Klasse, die nur Daten haelt -
    sie wurde im Unterricht als saubere Alternative zu Dictionaries
    vorgestellt.
    """
    anlagebetrag: float            # was eingezahlt wurde
    endwert: float                 # was am Ende rauskommt
    gewinn: float                  # Endwert - Anlagebetrag
    gewinn_prozent: float          # Gewinn relativ zum Anlagebetrag
    jahre: int                     # Anlagedauer
    effektive_rendite: float       # Rendite nach Abzug der TER
    werte_pro_jahr: list[float]    # Wert nach jedem Jahr (fuer Diagramm)


class RenditeService:
    """Berechnet Renditeprognosen auf Basis eines ETFs."""

    def berechne(self, etf: ETF, anlagebetrag: float,
                 jahre: int, ter_abziehen: bool = True) -> Prognose:
        """Berechnet die zu erwartende Wertentwicklung.

        Parameter:
        - etf: der ETF mit erwarteter Rendite und TER
        - anlagebetrag: einmalige Investition zu Beginn
        - jahre: Anlagedauer
        - ter_abziehen: wenn True, wird die TER von der Rendite abgezogen
        """
        # Effektive Rendite = was wirklich beim Anleger ankommt
        if ter_abziehen:
            effektive_rendite = etf.erwartete_rendite - etf.ter
        else:
            effektive_rendite = etf.erwartete_rendite

        # Zinseszinsformel angewendet auf jedes Jahr,
        # damit wir die Werte fuer das Diagramm haben
        werte = [anlagebetrag]  # Jahr 0 = Startwert
        for jahr in range(1, jahre + 1):
            wert = anlagebetrag * (1 + effektive_rendite / 100) ** jahr
            werte.append(wert)

        endwert = werte[-1]
        gewinn = endwert - anlagebetrag
        gewinn_prozent = (gewinn / anlagebetrag * 100
                          if anlagebetrag > 0 else 0.0)

        return Prognose(
            anlagebetrag=anlagebetrag,
            endwert=endwert,
            gewinn=gewinn,
            gewinn_prozent=gewinn_prozent,
            jahre=jahre,
            effektive_rendite=effektive_rendite,
            werte_pro_jahr=werte,
        )
