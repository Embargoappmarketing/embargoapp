---
name: review-embargo-ad-performance
description: Analizuje wyniki kampanii Embargo z eksportów Meta Ads, Google Ads i HubSpot (CSV, XLSX lub wklejone tabele) i podejmuje decyzje pauzuj / skaluj / czekaj według zasad konta (cel CPL ok. £60–70, pauza po 2× CPL bez leada, skalowanie +10–15% po 4–5 leadach, werdykt kreacji po ≥15 konwersjach), wykrywa problemy z placementami (Audience Network), CPM, CVR i jakością leadów (MQL → SQL) oraz pisze raport tygodniowy lub miesięczny. Użyj przy „przeanalizuj kampanie”, „raport tygodniowy PPC”, „co wyłączyć”, „dlaczego CPL rośnie”, „performance review”, „weekly report”, „kill or scale”, „podsumowanie miesiąca”.
---

# Analiza wyników i raport — Embargo

## Wejście
- Eksport z okresem (daty), poziomem (kampania / ad set / reklama), wydatkami, wyświetleniami, kliknięciami i leadami (najlepiej też placement).
- Opcjonalnie: HubSpot (MQL, SQL, źródło), Calendly (rezerwacje), poprzedni okres do porównania.
- Docelowy CPL per rynek (domyślnie £65). Jeśli brak — zapytaj albo przyjmij £65 i zapisz założenie.

## Kroki
1. Zweryfikuj dane: okres, waluta, okno atrybucji, czy ostatnie 3 dni są niepełne (lag konwersji), czy „Results” to na pewno lead / rezerwacja.
2. Uruchom `python scripts/ppc_kpi_report.py eksport.csv --target-cpl 65` (dla CSV z „;” i polskimi liczbami też działa; konto w PLN: `--currency "zł " --pause-mult 2`). XLSX najpierw zapisz jako CSV.
3. Zastosuj zasady decyzji:

| Sytuacja | Decyzja |
| --- | --- |
| Wydano 2× docelowego CPL i 0 leadów (3×, gdy cel > £75) | Pauza |
| 4–5 leadów w docelowym CPL | Skaluj +10–15% budżetu |
| ≥15 konwersji, CPL w celu | Zwycięzca — skaluj, nagraj kolejne otwarcia |
| ≥15 konwersji, CPL >30% ponad celem | Wymień kreację |
| 1–3 leady | Czekaj (lag ok. 3 dni) |

4. Zdiagnozuj przyczyny: udział Audience Network i Facebook Feed (tani ruch, słaby CVR), CPM vs CVR (tańszy CPM + wyższe CPA = gorsza jakość ruchu), wysoki CTR przy niskim CVR (hook przyciąga złych ludzi), zmęczenie kreacji, konwersja landing page’a, jakość leadów (MQL → SQL, spam).
5. Porównaj z benchmarkami z `reference/embargo-essentials.md` (sekcja 8) i z poprzednim okresem.
6. Napisz rekomendacje z priorytetem i oczekiwanym efektem.

## Format odpowiedzi (raport)
1. **TL;DR** — 3 punkty: wynik vs cel, największy problem, najważniejsza decyzja.
2. **KPI:** | Kanał / rynek | Wydatki | Leady (MQL) | CPL | SQL | Koszt SQL | CTR | CVR | CPM / CPC | Zmiana vs poprzedni okres |
3. **Decyzje:** | Pozycja | Metryka | Zasada | Decyzja | Kiedy sprawdzić ponownie |
4. **Wnioski kreatywne:** co działa, co nie (odnieś się do wzorców: klient mówiący do właścicieli, hook jako filtr).
5. **Następne testy** (maks. 3, każdy z hipotezą).
6. **Braki w danych.**

## Przypadki brzegowe
- Brak kolumny z leadami: zapytaj o zdarzenie konwersji, nie licz CPL z kliknięć.
- Mieszane waluty lub rynki: raportuj osobno UK i PL.
- Mała próba (<15 konwersji): nie ogłaszaj zwycięzcy, podaj kierunek i potrzebny budżet.
- Google Brand: niski CPL nie jest sukcesem kampanii non-brand — raportuj osobno.
