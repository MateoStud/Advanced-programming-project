# 🧪 Manual GUI Test Cases

**Project:** ETF-Vergleicher (NiceGUI Browser App)
**Test environment:** Web browser at `http://localhost:8080`, `etf_app.db` pre-seeded with the 10 largest ETFs.
**Tester:** _your name_
**Date:** _yyyy-mm-dd_
**Result:** All 15 test cases passed.

## How to use this document

1. Start the application with `python main.py`.
2. Execute every test case in the order given.
3. Compare what you see in the browser with the **Expected Result**.
4. Record the observed behaviour in **Actual Result** and set the **Status**.

---

## Section 1 – Start Page (ETF Management)

### TC_001 – Display the seeded ETF list on first launch

| Field | Value |
|---|---|
| **Preconditions** | Application has just been started. `etf_app.db` contains the 10 seeded ETFs. |
| **Steps** | 1. Open `http://localhost:8080`<br>2. Stay on the start page<br>3. Scroll to "Vorhandene ETFs" |
| **Test Data** | – |
| **Expected Result** | Table contains exactly 10 rows. Columns: Name, ISIN, Symbol, TER (%), Kategorie, Aktueller Kurs, Erw. Rendite p.a. (%). VOO, SPY, IVV, VTI, QQQ, VEA, IEFA, VWO, VWRL, IWDA all appear. |
| **Actual Result** | Table displayed exactly 10 rows. All expected ETFs (VOO, SPY, IVV, VTI, QQQ, VEA, IEFA, VWO, VWRL, IWDA) present, all columns correctly filled. |
| **Status** | Pass |

---

### TC_002 – Add a valid new ETF

| Field | Value |
|---|---|
| **Preconditions** | Start page is open. |
| **Steps** | 1. Fill in all fields of "Neuen ETF hinzufügen"<br>2. Click "ETF hinzufügen" |
| **Test Data** | Name: `MSCI Europe ETF`<br>ISIN: `IE00B1YZSC51`<br>Symbol: `CEU`<br>Kategorie: `Europa`<br>TER: `0.12`<br>Kurs: `65.00`<br>Rendite: `6.50` |
| **Expected Result** | Green notification "ETF hinzugefügt." Text fields are cleared. Table now shows 11 rows. |
| **Actual Result** | Green notification "ETF hinzugefügt." appeared. Text fields were cleared. Table then showed 11 rows including the new MSCI Europe ETF. |
| **Status** | Pass |

---

### TC_003 – Reject an empty text field on submit

| Field | Value |
|---|---|
| **Preconditions** | Start page is open. |
| **Steps** | 1. Leave the field "Name" empty<br>2. Fill all other fields with valid data<br>3. Click "ETF hinzufügen" |
| **Test Data** | Name: (empty)<br>ISIN: `TEST00000001`<br>Symbol: `TST`<br>Kategorie: `Test`<br>Defaults for numbers |
| **Expected Result** | Orange warning notification mentioning "name". No ETF added; row count unchanged. |
| **Actual Result** | Orange warning referencing "name" was shown. No ETF added, row count unchanged. |
| **Status** | Pass |

---

### TC_004 – Reject a current price of zero or below

| Field | Value |
|---|---|
| **Preconditions** | Start page is open. |
| **Steps** | 1. Fill all text fields with valid values<br>2. Set "Aktueller Kurs" to `0`<br>3. Click "ETF hinzufügen" |
| **Test Data** | Name: `ZeroPrice Test`<br>ISIN: `TEST00000002`<br>Symbol: `ZPT`<br>Kategorie: `Test`<br>Aktueller Kurs: `0` |
| **Expected Result** | Orange warning notification about `aktueller_kurs`. ETF not added; table unchanged. |
| **Actual Result** | Orange warning about "aktueller_kurs" appeared. ETF not saved, table unchanged. |
| **Status** | Pass |

---

### TC_005 – Reject a duplicate ISIN

| Field | Value |
|---|---|
| **Preconditions** | Start page is open. An ETF with ISIN `US9229083632` (Vanguard S&P 500 ETF) already exists. |
| **Steps** | 1. Fill all fields with the duplicate ISIN<br>2. Click "ETF hinzufügen" |
| **Test Data** | Name: `Duplicate Test`<br>ISIN: `US9229083632`<br>Symbol: `DUP`<br>Kategorie: `Test`<br>Kurs: `100`, Rendite: `5.00` |
| **Expected Result** | Orange notification: "Ein ETF mit ISIN US9229083632 existiert bereits." Table unchanged. |
| **Actual Result** | Orange notification "Ein ETF mit ISIN US9229083632 existiert bereits." was displayed. No new entry, table unchanged. |
| **Status** | Pass |

---

## Section 2 – Renditerechner

### TC_006 – Calculate a forecast with TER deduction

| Field | Value |
|---|---|
| **Preconditions** | At least one ETF exists. Navigated to "Renditerechner". |
| **Steps** | 1. Select "Vanguard S&P 500 ETF (VOO)"<br>2. Anlagebetrag = `10000`, Anlagedauer = `10`<br>3. TER checkbox enabled<br>4. Click "Rendite berechnen" |
| **Test Data** | VOO (8.5% return, 0.03% TER), 10'000, 10 years, TER on |
| **Expected Result** | Four KPI cards appear:<br>• Anlagebetrag = 10'000.00<br>• Endwert ≈ 22'547<br>• Gewinn ≈ +12'547 (green), ≈ +125 %<br>• Effektive Rendite = 8.47 %<br>Line chart with 11 data points (Jahr 0 – Jahr 10). |
| **Actual Result** | Four KPI cards appeared: Anlagebetrag 10'000.00, Endwert 22'547.05, Gewinn +12'547.05 (green) / +125.47 %, effective return 8.47 %. Line chart with 11 points (year 0–10) rendered correctly. |
| **Status** | Pass |

---

### TC_007 – Same ETF without TER deduction produces a higher Endwert

| Field | Value |
|---|---|
| **Preconditions** | Renditerechner page is open. |
| **Steps** | 1. Select "Vanguard S&P 500 ETF (VOO)"<br>2. Anlagebetrag = `10000`, Anlagedauer = `10`<br>3. **Uncheck** TER checkbox<br>4. Click "Rendite berechnen" |
| **Test Data** | VOO, 10'000, 10 years, TER off |
| **Expected Result** | Effektive Rendite = 8.50 % (full return).<br>Endwert ≈ 22'609. Higher than TC_006 → proves the TER toggle works. |
| **Actual Result** | Effective return showed 8.50 %, Endwert 22'609.04 – higher than TC_006. TER toggle works as expected. |
| **Status** | Pass |

---

### TC_008 – Block calculation when no ETF is selected

| Field | Value |
|---|---|
| **Preconditions** | Renditerechner page is open. |
| **Steps** | 1. Do not select anything in the ETF dropdown<br>2. Click "Rendite berechnen" |
| **Test Data** | No ETF selected |
| **Expected Result** | Orange warning: "Bitte einen ETF auswählen." No KPI cards or chart rendered. |
| **Actual Result** | Orange warning "Bitte einen ETF auswählen." appeared. No KPI cards or chart rendered. |
| **Status** | Pass |

---

### TC_009 – Block calculation when Anlagebetrag is 0

| Field | Value |
|---|---|
| **Preconditions** | Renditerechner page is open. |
| **Steps** | 1. Select any ETF<br>2. Anlagebetrag = `0`, Anlagedauer = `10`<br>3. Click "Rendite berechnen" |
| **Test Data** | Anlagebetrag: 0 |
| **Expected Result** | Orange warning: "Anlagebetrag muss grösser als 0 sein." No KPI cards or chart. |
| **Actual Result** | Orange warning "Anlagebetrag muss grösser als 0 sein." was shown. No results rendered. |
| **Status** | Pass |

---

### TC_010 – Long-term forecast: 30 years on a world ETF

| Field | Value |
|---|---|
| **Preconditions** | Renditerechner page is open. |
| **Steps** | 1. Select "iShares Core MSCI World UCITS ETF (IWDA)"<br>2. Anlagebetrag = `25000`, Anlagedauer = `30`<br>3. TER checkbox enabled<br>4. Click "Rendite berechnen" |
| **Test Data** | IWDA (7.5% return, 0.20% TER), 25'000, 30 years, TER on |
| **Expected Result** | Effektive Rendite = 7.30 %.<br>Endwert ≈ 206'982.<br>Gewinn ≈ +181'982 (green).<br>Chart shows clearly exponential curve over 31 data points. |
| **Actual Result** | Effective return 7.30 %, Endwert 206'981.79, Gewinn +181'981.79 (green). Chart shows a clearly exponential curve across 31 points. |
| **Status** | Pass |

---

## Section 3 – Vergleich

### TC_011 – Compare exactly two ETFs

| Field | Value |
|---|---|
| **Preconditions** | "Vergleich" page is open. |
| **Steps** | 1. Select VOO and IWDA (two chips)<br>2. Anlagebetrag = `10000`, Anlagedauer = `15`<br>3. TER checkbox enabled<br>4. Click "Vergleichen" |
| **Test Data** | VOO + IWDA, 10'000, 15 years |
| **Expected Result** | Table "Prognose im Vergleich" with 2 rows:<br>• VOO: Effektive Rendite 8.47 %, Endwert ≈ 33'857<br>• IWDA: Effektive Rendite 7.30 %, Endwert ≈ 28'774<br>Chart "Wertentwicklung im Vergleich" with 2 lines and legend at bottom. |
| **Actual Result** | Table "Prognose im Vergleich" with 2 rows: VOO (8.47 %, Endwert 33'857.07) and IWDA (7.30 %, Endwert 28'773.78). Chart with 2 lines and legend at the bottom displayed correctly. |
| **Status** | Pass |

---

### TC_012 – Reject a comparison with less than 2 ETFs

| Field | Value |
|---|---|
| **Preconditions** | Vergleich page is open. |
| **Steps** | 1. Select only ONE ETF (e.g. VOO)<br>2. Click "Vergleichen" |
| **Test Data** | Only 1 ETF selected |
| **Expected Result** | Orange warning: "Bitte mindestens 2 ETFs auswählen." No table or chart rendered. |
| **Actual Result** | Orange warning "Bitte mindestens 2 ETFs auswählen." appeared. No table or chart rendered. |
| **Status** | Pass |

---

### TC_013 – Compare four ETFs simultaneously

| Field | Value |
|---|---|
| **Preconditions** | Vergleich page is open. |
| **Steps** | 1. Select VOO, QQQ, VWO and IWDA<br>2. Anlagebetrag = `20000`, Anlagedauer = `20`<br>3. TER checkbox enabled<br>4. Click "Vergleichen" |
| **Test Data** | 4 ETFs, 20'000, 20 years |
| **Expected Result** | Comparison table has exactly 4 rows.<br>QQQ: highest Endwert ≈ 142'082<br>VOO ≈ 101'677<br>VWO ≈ 83'701<br>IWDA ≈ 81'851<br>Order: QQQ > VOO > VWO > IWDA.<br>Chart: 4 differently coloured lines + 4 legend entries. |
| **Actual Result** | Comparison table with exactly 4 rows. Order by Endwert: QQQ (142'081.83) > VOO (101'676.65) > VWO (83'700.81) > IWDA (81'850.55). Chart with 4 coloured lines and 4 legend entries. |
| **Status** | Pass |

---

### TC_014 – Reject Anlagedauer below 1 year

| Field | Value |
|---|---|
| **Preconditions** | Vergleich page is open. |
| **Steps** | 1. Select two ETFs (e.g. VOO and IWDA)<br>2. Anlagebetrag = `10000`<br>3. Try to set Anlagedauer = `0`<br>4. Click "Vergleichen" |
| **Test Data** | 2 ETFs, Anlagedauer 0 |
| **Expected Result** | Either: the input clamps to min=1 and the user cannot enter 0,<br>OR: warning notification "Anlagedauer muss mindestens 1 Jahr sein."<br>No results rendered with Anlagedauer = 0. |
| **Actual Result** | The Anlagedauer field could not be set below 1 (min=1 enforced); calculating with 0 years was not possible. No results produced with an invalid duration. |
| **Status** | Pass |

---

### TC_015 – Navigation works consistently from every page

| Field | Value |
|---|---|
| **Preconditions** | Application is running. |
| **Steps** | 1. Open `http://localhost:8080`<br>2. Click "Renditerechner" in the navigation<br>3. Click "Vergleich"<br>4. Click "Startseite"<br>5. Check the heading and URL on each page |
| **Test Data** | – |
| **Expected Result** | Start page: heading "ETF-Vergleicher", URL `/`<br>Renditerechner: heading "Renditerechner", URL `/renditerechner`<br>Vergleich: heading "Vergleich mehrerer ETFs", URL `/vergleich`<br>All three buttons present on every page. |
| **Actual Result** | Navigation works from every page: Startseite (heading "ETF-Vergleicher", URL `/`), Renditerechner (URL `/renditerechner`), Vergleich (heading "Vergleich mehrerer ETFs", URL `/vergleich`). All three buttons present on every page. |
| **Status** | Pass |

---

## Summary

| Section | Test Cases | Passed | Failed |
|---|---|---|---|
| Start Page (ETF Management) | TC_001 – TC_005 | 5 / 5 | 0 / 5 |
| Renditerechner | TC_006 – TC_010 | 5 / 5 | 0 / 5 |
| Vergleich | TC_011 – TC_015 | 5 / 5 | 0 / 5 |
| **Total** | **15** | **15 / 15** | **0 / 15** |

**Tester:** Janis Giolo
**Date:** 21.05.2026
