#!/usr/bin/env python3
"""Walidacja tekstów reklam Embargo (Google Ads, PMax, Meta) — limity znaków i zasady marki.

Użycie:
  python check_ad_lengths.py plik.csv
CSV z nagłówkiem: type,text  (opcjonalnie kolumna id).
Typy: headline, long_headline, description, short_description, path, callout,
      sitelink, sitelink_description, snippet, business_name,
      meta_headline, meta_description, meta_hook
Kod wyjścia 1, jeśli jest choć jeden błąd (ERROR).
"""
import csv
import re
import sys
import unicodedata

LIMITS = {
    "headline": 30, "long_headline": 90, "description": 90, "short_description": 60,
    "path": 15, "callout": 25, "sitelink": 25, "sitelink_description": 35,
    "snippet": 25, "business_name": 25,
    "meta_headline": 40, "meta_description": 30, "meta_hook": 125,
}
GOOGLE_TYPES = {"headline", "long_headline", "description", "short_description", "path",
                "callout", "sitelink", "sitelink_description", "snippet", "business_name"}
BANNED_WORDS = ["synergy", "optimisation", "optimization", "holistic", "seamless", "best-in-class",
                "solution", "leverage", "api", "database", "saas", "users", "clients",
                "guaranteed", "gwarantujemy", "rozwiązanie"]
PRICE_RE = re.compile(r"(£|€|\$|zł|pln|gbp|eur)\s?\d|\d\s?(£|€|zł|pln|gbp|eur)|per month|/month|miesięcznie za", re.I)


def has_emoji_or_symbol(text):
    for ch in text:
        cat = unicodedata.category(ch)
        if ch in "★☆✓✔✅❌→←•●" or cat == "So" or ord(ch) > 0x1F000:
            return True
    return False


def check(row_type, text):
    issues = []
    t = row_type.strip().lower()
    limit = LIMITS.get(t)
    n = len(text)
    if limit is None:
        issues.append(("ERROR", f"nieznany typ '{row_type}'"))
    elif n > limit:
        issues.append(("ERROR", f"{n}/{limit} znaków (za długie o {n - limit})"))
    if t in GOOGLE_TYPES:
        if has_emoji_or_symbol(text):
            issues.append(("ERROR", "symbol/emoji — Google odrzuci (np. ★)"))
        if t in {"headline", "long_headline", "callout", "sitelink", "path", "snippet"} and "!" in text:
            issues.append(("ERROR", "wykrzyknik niedozwolony w tym elemencie"))
        if text.count("!") > 1:
            issues.append(("ERROR", "więcej niż jeden wykrzyknik"))
        letters = [c for c in text if c.isalpha()]
        if len(letters) > 4 and sum(c.isupper() for c in letters) / len(letters) > 0.6:
            issues.append(("WARN", "nadmiar wielkich liter"))
    low = text.lower()
    for w in BANNED_WORDS:
        if re.search(r"\b" + re.escape(w) + r"\b", low):
            issues.append(("WARN", f"słowo spoza ToV: '{w}'"))
    if PRICE_RE.search(text):
        issues.append(("WARN", "wygląda na cenę — w reklamach Embargo nie podajemy cen"))
    return n, limit, issues


def main(path):
    errors = 0
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    print("| # | Typ | Tekst | Znaki | Status |")
    print("| --- | --- | --- | --- | --- |")
    for i, row in enumerate(rows, 1):
        rid = row.get("id") or i
        extra = row.get(None) or []  # niecytowane przecinki w tekście
        text = ",".join([row.get("text") or ""] + list(extra)).strip()
        n, limit, issues = check(row.get("type", ""), text)
        status = "OK" if not issues else "; ".join(f"{lvl}: {msg}" for lvl, msg in issues)
        errors += sum(1 for lvl, _ in issues if lvl == "ERROR")
        print(f"| {rid} | {row.get('type','')} | {text.replace('|', '/')} | {n}/{limit if limit else '?'} | {status} |")
    print(f"\nBłędy: {errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
