#!/usr/bin/env python3
"""Raport KPI i decyzje (pauza / skaluj / czekaj) dla eksportów Meta Ads, Google Ads lub HubSpot.

Użycie:
  python ppc_kpi_report.py eksport.csv [--target-cpl 65] [--group-by "Ad name"] [--currency £] [--pause-mult 2]

Rozpoznaje typowe nazwy kolumn (EN/PL): nazwa (Ad name / Ad set name / Campaign / Kampania...),
wydatki (Amount spent / Spend / Cost / Koszt), wyświetlenia (Impressions / Impr.), kliknięcia
(Link clicks / Clicks), leady (Leads / Results / Conversions / Konwersje), opcjonalnie placement.
Zasady Embargo: pauza po wydaniu 2× docelowego CPL bez leada (3×, gdy cel > £75); skalowanie
+10–15% po 4–5 leadach w celu; werdykt kreacji po >= 15 konwersjach; ocena z ok. 3-dniowym lagiem.
"""
import argparse
import csv
import re
import sys
from collections import OrderedDict

ALIASES = {
    "name": ["ad name", "ad set name", "campaign name", "campaign", "ad group", "ad", "name",
             "kampania", "nazwa reklamy", "nazwa zestawu reklam", "nazwa kampanii", "grupa reklam"],
    "spend": ["amount spent (gbp)", "amount spent (pln)", "amount spent (eur)", "amount spent", "spend",
              "cost", "koszt", "wydana kwota (gbp)", "wydana kwota (pln)", "wydana kwota"],
    "impressions": ["impressions", "impr.", "impr", "wyświetlenia"],
    "clicks": ["link clicks", "clicks", "kliknięcia linku", "kliknięcia"],
    "leads": ["leads", "results", "conversions", "konwersje", "wyniki", "leady", "mql"],
    "placement": ["placement", "platform", "umiejscowienie", "platforma"],
}


def find_col(headers, key):
    low = {h.lower().strip(): h for h in headers if h}
    for alias in ALIASES[key]:
        if alias in low:
            return low[alias]
    return None


def num(value):
    if value is None:
        return 0.0
    s = str(value).strip().replace("\u00a0", "").replace(" ", "")
    s = re.sub(r"[^0-9,.\-]", "", s)
    if not s or s in {"-", ".", ","}:
        return 0.0
    if "," in s and "." in s:
        s = s.replace(",", "")
    elif "," in s:
        head, _, tail = s.rpartition(",")
        s = head.replace(",", "") + "." + tail if len(tail) in (1, 2) else s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


PAUSE_MULT = None


def decide(spend, leads, cpl, target):
    mult = PAUSE_MULT or (3 if target > 75 else 2)
    if leads == 0:
        if spend >= mult * target:
            return f"PAUZA (wydano ≥{mult}× CPL bez leada)"
        return "CZEKAJ (za mało danych, lag ok. 3 dni)"
    if leads >= 15:
        if cpl <= target:
            return "ZWYCIĘZCA (≥15 konw., CPL w celu) → skaluj +10–15%"
        if cpl > 1.3 * target:
            return "PRZEGRANY (≥15 konw., CPL >30% ponad cel) → wymień"
        return "NA GRANICY → test nowego hooka"
    if leads >= 4:
        return "SKALUJ +10–15%" if cpl <= target else "OBSERWUJ (CPL ponad celem)"
    if spend >= mult * target * max(leads, 1) * 1.5:
        return "OSTRZEŻENIE (wysoki CPL przy małej próbie)"
    return "UCZY SIĘ (1–3 leady)"


CUR = "£"


def fmt(x, money=False, pct=False):
    if pct:
        return f"{x:.2f}%"
    if money:
        return f"{CUR}{x:,.2f}"
    return f"{x:,.0f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--target-cpl", type=float, default=65.0)
    ap.add_argument("--group-by", default=None, help="kolumna do grupowania (domyślnie wykryta nazwa)")
    ap.add_argument("--currency", default="£", help="symbol waluty w raporcie, np. £ lub zł ")
    ap.add_argument("--pause-mult", type=float, default=None,
                    help="mnożnik progu pauzy (domyślnie 2, a 3 gdy cel > 75); dla kont w PLN ustaw ręcznie")
    a = ap.parse_args()
    ap_mult = a.pause_mult
    global CUR, PAUSE_MULT
    CUR = a.currency
    PAUSE_MULT = ap_mult

    with open(a.path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        delim = ";" if sample.count(";") > sample.count(",") else ","
        rows = list(csv.DictReader(f, delimiter=delim))
    if not rows:
        print("Brak danych.")
        return 2
    headers = rows[0].keys()
    cols = {k: find_col(headers, k) for k in ALIASES}
    if a.group_by:
        cols["name"] = a.group_by
    missing = [k for k in ("name", "spend", "leads") if not cols[k]]
    if missing:
        print(f"Brak wymaganych kolumn: {missing}. Kolumny w pliku: {list(headers)}")
        return 2

    groups = OrderedDict()
    placements = OrderedDict()
    for r in rows:
        name = (r.get(cols["name"]) or "(brak nazwy)").strip()
        if name.lower() in {"total", "suma", "razem"}:
            continue
        g = groups.setdefault(name, {"spend": 0.0, "impr": 0.0, "clicks": 0.0, "leads": 0.0})
        g["spend"] += num(r.get(cols["spend"]))
        g["impr"] += num(r.get(cols["impressions"])) if cols["impressions"] else 0
        g["clicks"] += num(r.get(cols["clicks"])) if cols["clicks"] else 0
        g["leads"] += num(r.get(cols["leads"]))
        if cols["placement"]:
            p = (r.get(cols["placement"]) or "?").strip()
            pg = placements.setdefault(p, {"spend": 0.0, "clicks": 0.0, "leads": 0.0})
            pg["spend"] += num(r.get(cols["spend"]))
            pg["clicks"] += num(r.get(cols["clicks"])) if cols["clicks"] else 0
            pg["leads"] += num(r.get(cols["leads"]))

    tot = {k: sum(g[k] for g in groups.values()) for k in ("spend", "impr", "clicks", "leads")}
    t = a.target_cpl
    print(f"## Podsumowanie (docelowy CPL {CUR}{t:.0f})\n")
    cpl = tot["spend"] / tot["leads"] if tot["leads"] else 0
    ctr = 100 * tot["clicks"] / tot["impr"] if tot["impr"] else 0
    cvr = 100 * tot["leads"] / tot["clicks"] if tot["clicks"] else 0
    cpm = 1000 * tot["spend"] / tot["impr"] if tot["impr"] else 0
    cpc = tot["spend"] / tot["clicks"] if tot["clicks"] else 0
    print("| Wydatki | Leady | CPL | CTR | CPC | CPM | Click → lead |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    print(f"| {fmt(tot['spend'], money=True)} | {fmt(tot['leads'])} | {fmt(cpl, money=True) if tot['leads'] else '—'} | "
          f"{fmt(ctr, pct=True)} | {fmt(cpc, money=True)} | {fmt(cpm, money=True)} | {fmt(cvr, pct=True)} |\n")

    print("## Pozycje i decyzje\n")
    print("| Nazwa | Wydatki | Leady | CPL | CTR | CVR | CPM | Decyzja | Uwagi |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for name, g in sorted(groups.items(), key=lambda kv: -kv[1]["spend"]):
        g_cpl = g["spend"] / g["leads"] if g["leads"] else 0
        g_ctr = 100 * g["clicks"] / g["impr"] if g["impr"] else 0
        g_cvr = 100 * g["leads"] / g["clicks"] if g["clicks"] else 0
        g_cpm = 1000 * g["spend"] / g["impr"] if g["impr"] else 0
        notes = []
        if ctr and cvr and g_ctr > 1.5 * ctr and g_cvr < 0.5 * cvr:
            notes.append("wysoki CTR, niski CVR — ruch niskiej jakości?")
        if cpm and g_cpm and g_cpm < 0.5 * cpm and g_cvr < cvr:
            notes.append("tani CPM i słaby CVR — sprawdź placementy")
        print(f"| {name.replace('|', '/')} | {fmt(g['spend'], money=True)} | {fmt(g['leads'])} | "
              f"{fmt(g_cpl, money=True) if g['leads'] else '—'} | {fmt(g_ctr, pct=True)} | {fmt(g_cvr, pct=True)} | "
              f"{fmt(g_cpm, money=True)} | {decide(g['spend'], g['leads'], g_cpl, t)} | {'; '.join(notes)} |")

    if placements:
        print("\n## Placementy (udział w kliknięciach vs leadach)\n")
        print("| Placement | Udział wydatków | Udział kliknięć | Udział leadów | Uwagi |")
        print("| --- | --- | --- | --- | --- |")
        for p, g in sorted(placements.items(), key=lambda kv: -kv[1]["clicks"]):
            ss = 100 * g["spend"] / tot["spend"] if tot["spend"] else 0
            sc = 100 * g["clicks"] / tot["clicks"] if tot["clicks"] else 0
            sl = 100 * g["leads"] / tot["leads"] if tot["leads"] else 0
            note = "wyklucz / ogranicz" if sc > 20 and sl < sc / 3 else ""
            if "audience network" in p.lower():
                note = "Audience Network — wyłącz (zasada konta)"
            print(f"| {p} | {ss:.0f}% | {sc:.0f}% | {sl:.0f}% | {note} |")
    print("\nPamiętaj: oceniaj z ok. 3-dniowym opóźnieniem i sprawdź jakość leadów (MQL → SQL, Calendly).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
