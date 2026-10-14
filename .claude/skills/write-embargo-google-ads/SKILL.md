---
name: write-embargo-google-ads
description: Tworzy Responsive Search Ads i zasoby Google Ads dla Embargo (UK i PL) — 15 nagłówków do 30 znaków, 4 opisy do 90, ścieżki, sitelinki, callouty i structured snippets — dopasowane do typu kampanii (Brand, Non-Brand Core, Business Type, konkurencja) i grupy słów kluczowych, z walidacją limitów znaków skryptem. Użyj przy prośbach „napisz RSA”, „reklamy Google Search”, „nagłówki i opisy do Google Ads”, „rozszerzenia / assets”, „Google Ads copy”, „search ads for [fraza]”, „odśwież reklamy w grupie”.
---

# Google Search Ads — Embargo

## Wejście (dopytaj, jeśli brakuje)
- Rynek (UK / PL), kampania (Brand, Non-Brand Core, Business Type, konkurencja) i grupa reklam.
- Główne frazy grupy (5–20) i landing page (URL + H1).
- Opcjonalnie: obecne reklamy i ich wyniki (CTR, konwersje, ocena zasobów).

## Zasady
- 15 nagłówków (max 30 zn.), 4 opisy (max 90 zn.), 2 ścieżki (max 15 zn.).
- Mix nagłówków: 3–4 z frazą kluczową, 3 korzyści (Own Your Regulars, Know Every Regular), 3 dowody (4.9-rated app, 3,000+ venues, live in 2–3 days), 2 problemowe (prowizje platform, anonimowi goście), 2 CTA, 1 brandowy.
- Każdy nagłówek musi mieć sens w dowolnej kombinacji — bez zdań urwanych między nagłówkami.
- Przypinaj oszczędnie; w kampanii Brand przypnij nazwę marki na pozycji 1.
- Bez gwiazdek, emoji i wykrzykników w nagłówkach (Google odrzuca symbole). Pisz „4.9-Rated App” / „ocena 4,9”.
- Bez cen i bez nazw konkurentów w tekście reklam (kampanie konkurencyjne: tylko frazy, nie copy).
- UK: British English (optimise, favourite). PL: polskie znaki liczą się jak zwykłe znaki — skracaj.
- Ton marki i claimy: `reference/embargo-essentials.md`.

## Kroki
1. Przeczytaj `reference/embargo-essentials.md` i `reference/google-examples.md`.
2. Określ intencję grupy (np. „loyalty app for cafés” = szuka narzędzia; „deliveroo alternative” = ucieka od prowizji) i dobierz główną obietnicę.
3. Napisz 15 nagłówków i 4 opisy; zadbaj o message match z H1 landing page’a.
4. Zapisz teksty do CSV (`type,text`) i uruchom `python scripts/check_ad_lengths.py ads.csv`. Popraw wszystkie ERROR i oceń WARN.
5. Dodaj ścieżki i zasoby (sitelinki, callouty, snippety).

## Format odpowiedzi
1. Kontekst: rynek, kampania, grupa, intencja, obietnica.
2. Tabela nagłówków: | # | Nagłówek | Znaki | Rola (fraza / korzyść / dowód / problem / CTA / brand) | Pin |
3. Tabela opisów: | # | Opis | Znaki |
4. Ścieżki URL, sitelinki (tytuł + 2 opisy), callouty, structured snippets.
5. Wynik walidacji skryptu i lista założeń.

## Przypadki brzegowe
- Kampania Brand: część zapytań to konsumenci aplikacji (login, download) — zasugeruj wykluczenia albo osobną ścieżkę zamiast zmiany copy.
- Słowo „embargo” ma inne znaczenia (sankcje, embargo prasowe) — przy niskim CTR sprawdź search terms (skill plan-embargo-keywords).
- Brak landing page’a dla intencji: zaproponuj sekcję hero do dopisania (skill audit-embargo-landing-page).
