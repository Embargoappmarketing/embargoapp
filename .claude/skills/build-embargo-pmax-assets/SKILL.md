---
name: build-embargo-pmax-assets
description: Buduje grupy zasobów Performance Max dla Embargo (UK i PL) — nagłówki do 30 znaków, długie nagłówki do 90, opisy do 60 i 90, briefy obrazów i wideo, sygnały odbiorców, search themes i wykluczenia marki — per segment (kawiarnie, quick service, delivery) lub produkt (lojalność, zamówienia online). Użyj przy „PMax”, „Performance Max”, „asset group”, „grupa zasobów”, „sygnały odbiorców”, „search themes”, „odśwież zasoby PMax”.
---

# Performance Max — Embargo

## Wejście
- Rynek, kampania (PMax Product lub PMax HoReCa Core), segment albo produkt grupy, landing page.
- Dostępne materiały: zdjęcia, wideo, logo; listy odbiorców (HubSpot, odwiedzający stronę).
- Opcjonalnie: raport zasobów (ocena „Low / Good / Best”) i wyniki.

## Zasady
- Jedna obietnica na grupę zasobów; segment = osobna grupa (kawiarnie, quick service, delivery).
- Limity: do 15 nagłówków (30 zn.), do 5 długich nagłówków (90), 1 krótki opis (60) + do 4 opisów (90), nazwa firmy „Embargo”.
- Obrazy: 1,91:1, 1:1 i 4:5; logo 1:1 i 4:1; zawsze własne wideo (bez niego Google generuje słabe automaty).
- Search themes: do 25 na grupę, zgodne z motywami słów kluczowych.
- Włącz wykluczenia marki, żeby PMax nie kanibalizował kampanii Brand.
- Optymalizuj pod jakość: import konwersji offline z HubSpot (MQL → SQL), kontrola spamu w formularzach.
- Bez cen, bez symboli i emoji, bez nazw konkurentów.

## Kroki
1. Przeczytaj `reference/embargo-essentials.md`.
2. Zdefiniuj grupę: segment / produkt, obietnica, dowód, landing page.
3. Napisz teksty, zapisz je do CSV (`type,text`; typy headline, long_headline, short_description, description, business_name) i uruchom `python scripts/check_ad_lengths.py assets.csv`. Popraw wszystkie ERROR.
4. Opisz obrazy i wideo do przygotowania (kadry, tekst na obrazie, formaty).
5. Zaproponuj sygnały odbiorców i search themes.

## Format odpowiedzi
1. Karta grupy: nazwa `{RYNEK}_PMax_{segment}`, obietnica, landing page.
2. Tabele: nagłówki | długie nagłówki | opisy — z liczbą znaków.
3. Lista obrazów i wideo do produkcji.
4. Sygnały odbiorców: listy klientów, odwiedzający, segmenty niestandardowe (frazy kategorii i konkurencji), zainteresowania.
5. Search themes (do 25) i wykluczenia marki.

## Przykład (UK, kawiarnie)
Długie nagłówki: „Own your regulars: loyalty, CRM and direct ordering in one app” (62) · „Know every regular by name — and bring lapsed guests back with AI” (65). Krótki opis: „Loyalty, CRM and direct ordering for independent venues.” (56).
