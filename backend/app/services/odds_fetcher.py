"""
Fetches real betting odds from The Odds API (https://the-odds-api.com).
Requires ODDS_API_KEY environment variable.
Results are cached for CACHE_TTL seconds to preserve free-tier quota (500 req/month).
"""
import os
import time
import httpx
from typing import Optional

ODDS_API_KEY = os.getenv("ODDS_API_KEY", "")
SPORT = "soccer_fifa_world_cup"
BASE_URL = "https://api.the-odds-api.com/v4"
CACHE_TTL = 600  # 10 minutes between API calls

# Preferred bookmakers ordered by reliability
PREFERRED_BOOKS = [
    "pinnacle", "betfair_ex_eu", "betfair", "bet365",
    "unibet", "williamhill", "bwin", "betway", "1xbet",
    "draftkings", "fanduel",
]

# The Odds API team names → our internal names
_NAME_MAP = {
    "United States": "United States",
    "USA": "United States",
    "US": "United States",
    "Korea Republic": "South Korea",
    "Republic of Korea": "South Korea",
    "Czech Republic": "Czechia",
    "Turkey": "Türkiye",
    "Ivory Coast": "Ivory Coast",
    "Côte d'Ivoire": "Ivory Coast",
    "Congo DR": "DR Congo",
    "Democratic Republic of the Congo": "DR Congo",
    "Bosnia": "Bosnia and Herzegovina",
    "Bosnia Herzegovina": "Bosnia and Herzegovina",
    "Cape Verde Islands": "Cape Verde",
    "Saudi Arabia": "Saudi Arabia",
    "New Zealand": "New Zealand",
}

_cache: dict = {"events": [], "ts": 0.0, "quota_remaining": None}


def _norm(name: str) -> str:
    return _NAME_MAP.get(name, name)


def _best_price_per_outcome(bookmakers: list, market_key: str) -> dict:
    """Return highest decimal price per outcome name across all bookmakers."""
    best: dict = {}
    for bk in bookmakers:
        for mkt in bk.get("markets", []):
            if mkt["key"] != market_key:
                continue
            for outcome in mkt.get("outcomes", []):
                name = outcome["name"]
                price = float(outcome.get("price", 0))
                point = outcome.get("point")
                if name not in best or price > best[name]["odds"]:
                    best[name] = {
                        "odds": round(price, 2),
                        "bookmaker": bk["title"],
                        "bookmaker_key": bk["key"],
                        "point": point,
                    }
    return best


def _parse_event(event: dict) -> dict:
    home_raw = event["home_team"]
    away_raw = event["away_team"]
    home = _norm(home_raw)
    away = _norm(away_raw)
    bookmakers_raw = event.get("bookmakers", [])

    def _priority(bk):
        try:
            return PREFERRED_BOOKS.index(bk["key"])
        except ValueError:
            return len(PREFERRED_BOOKS)

    bookmakers_raw = sorted(bookmakers_raw, key=_priority)

    parsed_books = []
    for bk in bookmakers_raw:
        entry: dict = {"name": bk["title"], "key": bk["key"]}
        for mkt in bk.get("markets", []):
            if mkt["key"] == "h2h":
                oc = {o["name"]: round(float(o["price"]), 2) for o in mkt["outcomes"]}
                entry["h2h"] = {
                    "home": oc.get(home_raw) or oc.get(home),
                    "draw": oc.get("Draw"),
                    "away": oc.get(away_raw) or oc.get(away),
                }
            elif mkt["key"] == "totals":
                for o in mkt["outcomes"]:
                    if abs(float(o.get("point", 0)) - 2.5) < 0.01:
                        entry.setdefault("totals_2_5", {})[
                            "over" if o["name"] == "Over" else "under"
                        ] = round(float(o["price"]), 2)
            elif mkt["key"] == "spreads":
                for o in mkt["outcomes"]:
                    side = "home" if o["name"] in (home_raw, home) else "away"
                    entry.setdefault("spreads", {})[side] = {
                        "point": o.get("point", 0),
                        "odds": round(float(o["price"]), 2),
                    }
        if entry.get("h2h") or entry.get("totals_2_5"):
            parsed_books.append(entry)

    best_h2h = _best_price_per_outcome(bookmakers_raw, "h2h")
    best_totals = _best_price_per_outcome(bookmakers_raw, "totals")
    best_spreads = _best_price_per_outcome(bookmakers_raw, "spreads")

    best: dict = {}
    if best_h2h:
        best["home"] = best_h2h.get(home_raw) or best_h2h.get(home)
        best["draw"] = best_h2h.get("Draw")
        best["away"] = best_h2h.get(away_raw) or best_h2h.get(away)
    for k, label in [("Over", "over_2_5"), ("Under", "under_2_5")]:
        if k in best_totals:
            best[label] = best_totals[k]
    if best_spreads:
        best["spread_home"] = best_spreads.get(home_raw) or best_spreads.get(home)
        best["spread_away"] = best_spreads.get(away_raw) or best_spreads.get(away)

    return {
        "home_team": home,
        "away_team": away,
        "commence_time": event.get("commence_time"),
        "bookmakers": parsed_books,
        "best_odds": best,
    }


def _fetch_raw() -> tuple[list, Optional[int]]:
    if not ODDS_API_KEY:
        return [], None
    try:
        resp = httpx.get(
            f"{BASE_URL}/sports/{SPORT}/odds/",
            params={
                "apiKey": ODDS_API_KEY,
                "regions": "eu,uk",
                "markets": "h2h,totals,spreads",
                "oddsFormat": "decimal",
                "dateFormat": "iso",
            },
            timeout=8,
        )
        if resp.status_code in (401, 422):
            return [], None
        resp.raise_for_status()
        quota = resp.headers.get("x-requests-remaining")
        return resp.json(), int(quota) if quota else None
    except Exception:
        return [], None


def _refresh_cache() -> None:
    raw, quota = _fetch_raw()
    _cache["events"] = [_parse_event(e) for e in raw]
    _cache["ts"] = time.monotonic()
    if quota is not None:
        _cache["quota_remaining"] = quota


def get_all_odds() -> list:
    if time.monotonic() - _cache["ts"] > CACHE_TTL:
        _refresh_cache()
    return _cache["events"]


def get_match_odds(home_team: str, away_team: str) -> Optional[dict]:
    """Return odds for a match, or None if no API key / match not found."""
    if not ODDS_API_KEY:
        return None
    events = get_all_odds()
    h, a = _norm(home_team), _norm(away_team)
    for ev in events:
        if ev["home_team"] == h and ev["away_team"] == a:
            return ev
        if ev["home_team"] == a and ev["away_team"] == h:
            # Flip home/away so caller always gets home=requested home
            swapped = dict(ev)
            swapped["home_team"], swapped["away_team"] = h, a
            best = dict(swapped.get("best_odds", {}))
            best["home"], best["away"] = best.get("away"), best.get("home")
            best["spread_home"], best["spread_away"] = best.get("spread_away"), best.get("spread_home")
            swapped["best_odds"] = best
            return swapped
    return None


def enrich_tips_with_real_odds(tips: list, home_team: str, away_team: str) -> list:
    """
    For each tip, add real_odds (best bookmaker price) and recalculate value
    against actual market odds instead of model-derived odds.
    """
    match_odds = get_match_odds(home_team, away_team)
    if not match_odds:
        # No key or match not found — attach empty real_odds block
        return [{**t, "real_odds": None} for t in tips]

    best = match_odds["best_odds"]
    bookmakers = match_odds["bookmakers"]

    def _real_value(prob: float, real_price: Optional[float]) -> Optional[dict]:
        if not real_price or real_price <= 1:
            return None
        v = prob * real_price - 1
        implied = 1 / real_price
        return {
            "has_value": v > 0.05,
            "value_percentage": round(v * 100, 1),
            "edge": round((prob - implied) * 100, 1),
        }

    def _pick(best_key: str) -> Optional[dict]:
        return best.get(best_key)

    enriched = []
    for tip in tips:
        market = tip["market"]
        rec = tip["recommendation"]
        prob = tip["probability"]

        real_entry: Optional[dict] = None

        if market == "1X2":
            if rec == "1":
                real_entry = _pick("home")
            elif rec == "X":
                real_entry = _pick("draw")
            elif rec == "2":
                real_entry = _pick("away")

        elif market in ("Over/Under 2.5", "Mais/Menos 2.5"):
            if "Over" in rec or "Mais" in rec:
                real_entry = _pick("over_2_5")
            else:
                real_entry = _pick("under_2_5")

        elif market in ("BTTS", "Ambas Marcam"):
            # The Odds API doesn't always have BTTS; skip
            real_entry = None

        elif market in ("Asian Handicap", "Handicap Asiático"):
            if home_team in rec or rec.startswith(home_team[:4]):
                real_entry = _pick("spread_home")
            else:
                real_entry = _pick("spread_away")

        real_val = _real_value(prob, real_entry["odds"] if real_entry else None)

        enriched.append({
            **tip,
            "real_odds": {
                "price": real_entry["odds"] if real_entry else None,
                "bookmaker": real_entry["bookmaker"] if real_entry else None,
                "bookmaker_key": real_entry.get("bookmaker_key") if real_entry else None,
            } if real_entry else None,
            "real_value": real_val,
            "bookmakers_available": len(bookmakers),
        })

    return enriched


def is_configured() -> bool:
    return bool(ODDS_API_KEY)


def quota_remaining() -> Optional[int]:
    return _cache.get("quota_remaining")
