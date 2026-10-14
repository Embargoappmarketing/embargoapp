---
name: write-embargo-meta-ads
description: Tworzy gotowe do wgrania teksty reklam Meta (Facebook, Instagram) dla Embargo w UK i PL — primary text, headline, description, CTA i tekst na kreację — w wariantach per kąt (Ghost Guest, Aggregator Tax, ponowne pozyskanie, cichy odpływ, złożoność, historia klienta), persona i etap lejka, z hipotezą testu i nazewnictwem. Użyj przy prośbach „napisz reklamy na Metę”, „copy do statyk”, „warianty primary text”, „nowe kąty reklamowe”, „Meta ad copy”, „Facebook ads”, „Instagram ads”, „ad set problem-focused” oraz gdy trzeba przenieść zwycięską reklamę na innego klienta lub rynek.
---

# Reklamy Meta — Embargo

## Wejście (dopytaj, jeśli brakuje)
- Rynek: UK lub PL (ES tylko po potwierdzeniu briefu).
- Etap lejka (TOF / MOF / BOF) i zdarzenie konwersji (lead, rezerwacja demo).
- Kąt lub hipoteza; persona (domyślnie A: 1–4 lokale).
- Dowód: klient, osoba, liczby — wyłącznie z proof banku.
- Format (statyka, wideo, karuzela) i liczba wariantów (domyślnie 3–5).

## Zasady, które wygrywają na koncie Embargo
- Klient mówiący do innych właścicieli wygrywa z founderem i prezenterem. Dowód = konkretny lokal + liczba.
- Hook to filtr, nie magnes: wołaj właściwą osobę („If you run a café…”, „Prowadzisz kawiarnię?”). Nie optymalizuj pod CTR — przy Advantage+ klikalny hook przyciąga złych ludzi.
- Pierwsze ok. 125 znaków primary text musi działać samodzielnie.
- Jedno CTA. Przycisk: UK Book Now lub Learn More, PL Zarezerwuj lub Dowiedz się więcej. Na kreacji: „Book a demo” / „Umów demo”.
- Bez „Free Trial” w prospectingu, bez cen, bez obietnic kwotowych.
- Statyka: jeden klient, jedna liczba, jedna linijka.

## Kroki
1. Przeczytaj `reference/embargo-essentials.md` i `reference/meta-angles.md`.
2. Zapisz hipotezę: „Jeśli [persona] zobaczy [kąt + dowód], to [akcja], bo [insight]”.
3. Napisz warianty, zmieniając jedną rzecz naraz (hook, dowód albo CTA), żeby test był czysty.
4. Policz znaki: headline do 40 (najlepiej do 27), description do 30, hook do 125. Przy wielu wariantach zapisz je do CSV (`type,text`; typy meta_hook, meta_headline, meta_description) i uruchom `python scripts/check_ad_lengths.py warianty.csv`.
5. Sprawdź tekst checklistą z `reference/embargo-essentials.md` (sekcje 4 i 6).
6. Dodaj nazewnictwo reklam i UTM.

## Format odpowiedzi
Tabela: | ID | Rynek | Persona | Etap | Kąt | Hook (pierwsze 125 zn.) | Primary text | Headline (zn.) | Description (zn.) | CTA | Tekst na kreacji | Hipoteza |

Pod tabelą:
- rekomendowany zestaw do testu (maks. 3 kreacje na ad set) i co mierzyć (CPA/CPL i CVR; CPM jako wczesne ostrzeżenie; werdykt po ≥15 konwersjach),
- nazwy: `{RYNEK}_{ETAP}_{KĄT}_{KLIENT}_v{n}`, np. `UK_TOF_GhostGuest_ALMA_v1`,
- UTM: `utm_source=meta&utm_medium=paid_social&utm_campaign={rynek}_{etap}_{kąt}&utm_content={ID}`.

## Przykład (UK, TOF, Ghost Guest)
- Hook: „It’s 2PM on a slow Tuesday. Your regulars are nearby. You just can’t reach them.”
- Ciąg dalszy: „Embargo shows you who they are — and brings them back with one push. 3,000+ independents already do it.”
- Headline: „Fill Quiet Hours With Regulars” (30) · CTA: Book Now · Kreacja: „Know every regular. Book a demo.”

## Przypadki brzegowe
- Brak zatwierdzonego dowodu dla klienta: użyj liczb Embargo (3,000+ venues, 4.9★) albo wersji bez liczby z oznaczeniem „[DODAJ DOWÓD]”.
- PL: nie tłumacz UK 1:1 — zastosuj zasady z sekcji 4 i 7 essentials (albo skill localize-embargo-ads).
- Persona C (sieci 10+) słabo konwertuje w zimnym ruchu Meta — zaproponuj LinkedIn lub remarketing BOF.
- Prośba o ofertę cenową: odmów w reklamie i zaproponuj CTA do rozmowy.
