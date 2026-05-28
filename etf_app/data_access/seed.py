"""
seed.py - Inserts the 10 largest ETFs worldwide on first start.
"""

from sqlmodel import Session
from etf_app.domain.models import ETF


def seed_etfs(session: Session) -> None:
    """Add the 10 largest ETFs by assets under management (AUM)."""
    etfs = [
        ETF(name="Vanguard S&P 500 ETF", isin="US9229083632",
            symbol="VOO", ter=0.03, kategorie="USA Large Cap",
            aktueller_kurs=525.00, erwartete_rendite=8.50),
        ETF(name="SPDR S&P 500 ETF Trust", isin="US78462F1030",
            symbol="SPY", ter=0.09, kategorie="USA Large Cap",
            aktueller_kurs=570.00, erwartete_rendite=8.50),
        ETF(name="iShares Core S&P 500 ETF", isin="US4642872000",
            symbol="IVV", ter=0.03, kategorie="USA Large Cap",
            aktueller_kurs=572.00, erwartete_rendite=8.50),
        ETF(name="Vanguard Total Stock Market ETF",
            isin="US9229087690", symbol="VTI", ter=0.03,
            kategorie="USA Total Market", aktueller_kurs=285.00,
            erwartete_rendite=8.20),
        ETF(name="Invesco QQQ Trust", isin="US46090E1038",
            symbol="QQQ", ter=0.20, kategorie="USA Technologie",
            aktueller_kurs=490.00, erwartete_rendite=10.50),
        ETF(name="Vanguard FTSE Developed Markets ETF",
            isin="US9219438580", symbol="VEA", ter=0.06,
            kategorie="Industrieländer ex USA",
            aktueller_kurs=52.00, erwartete_rendite=6.50),
        ETF(name="iShares Core MSCI EAFE ETF", isin="US46434G7087",
            symbol="IEFA", ter=0.07,
            kategorie="Industrieländer ex USA",
            aktueller_kurs=78.00, erwartete_rendite=6.50),
        ETF(name="Vanguard FTSE Emerging Markets ETF",
            isin="US9220428588", symbol="VWO", ter=0.08,
            kategorie="Schwellenländer", aktueller_kurs=47.00,
            erwartete_rendite=7.50),
        ETF(name="Vanguard FTSE All-World UCITS ETF",
            isin="IE00B3RBWM25", symbol="VWRL", ter=0.22,
            kategorie="Welt", aktueller_kurs=130.00,
            erwartete_rendite=7.50),
        ETF(name="iShares Core MSCI World UCITS ETF",
            isin="IE00B4L5Y983", symbol="IWDA", ter=0.20,
            kategorie="Welt (Industrieländer)",
            aktueller_kurs=95.00, erwartete_rendite=7.50),
    ]
    for etf in etfs:
        session.add(etf)
