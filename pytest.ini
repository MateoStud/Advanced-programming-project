"""
test_unit.py - Unit tests for the ForecastService.

These tests do NOT touch the database. They pass an ETF object
directly into the service, so they are fast and isolated.
"""

import pytest

from etf_app.domain.models import ETF
from etf_app.services.forecast_service import ForecastService, Forecast


# Test 1: forecast WITH TER deduction
def test_compound_interest_with_ter(sample_etf):
    """7% return - 0.2% TER = 6.8% effective over 10 years.
    Expected: 10'000 * (1.068)^10 ≈ 19'306.90
    """
    result = ForecastService().calculate(
        etf=sample_etf, anlagebetrag=10000, jahre=10, ter_abziehen=True
    )
    assert result.endwert == pytest.approx(19306.90, abs=0.01)
    assert result.effektive_rendite == pytest.approx(6.80, abs=0.001)


# Test 2: forecast WITHOUT TER deduction
def test_compound_interest_without_ter(sample_etf):
    """Full 7% used. Expected: 10'000 * (1.07)^10 ≈ 19'671.51"""
    result = ForecastService().calculate(
        etf=sample_etf, anlagebetrag=10000, jahre=10, ter_abziehen=False
    )
    assert result.endwert == pytest.approx(19671.51, abs=0.01)


# Test 3: 0% return = no profit
def test_zero_return_no_profit():
    etf = ETF(name="Cash ETF", isin="CH0000000099", symbol="ZERO",
              ter=0.0, kategorie="Cash", aktueller_kurs=100,
              erwartete_rendite=0.0)
    result = ForecastService().calculate(
        etf=etf, anlagebetrag=5000, jahre=10
    )
    assert result.endwert == pytest.approx(5000.00, abs=0.01)
    assert result.gewinn == pytest.approx(0.0, abs=0.01)


# Test 4: Forecast object has all the expected fields
def test_forecast_has_all_fields(sample_etf):
    result = ForecastService().calculate(
        etf=sample_etf, anlagebetrag=1000, jahre=5
    )
    assert isinstance(result, Forecast)
    # 5 years -> year 0 plus years 1..5 = 6 values for the chart
    assert len(result.werte_pro_jahr) == 6
    assert result.werte_pro_jahr[0] == 1000


# Test 5: negative effective rate -> loss
def test_negative_effective_rate():
    """TER (2%) > return (1%) -> -1% effective. Loss over 5 years.
    Expected: 10'000 * (0.99)^5 ≈ 9'509.90
    """
    etf = ETF(name="Teurer ETF", isin="CH0000000098", symbol="EXPN",
              ter=2.0, kategorie="Test", aktueller_kurs=100,
              erwartete_rendite=1.0)
    result = ForecastService().calculate(
        etf=etf, anlagebetrag=10000, jahre=5
    )
    assert result.endwert == pytest.approx(9509.90, abs=0.01)
    assert result.gewinn < 0


# Test 6: invalid inputs are rejected
def test_invalid_input_raises(sample_etf):
    service = ForecastService()
    with pytest.raises(ValueError):
        service.calculate(etf=sample_etf, anlagebetrag=0, jahre=10)
    with pytest.raises(ValueError):
        service.calculate(etf=sample_etf, anlagebetrag=1000, jahre=0)
