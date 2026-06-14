"""
Fetches live and recent scores + statistics from ESPN's unofficial API.
No API key required.
"""
import httpx
from datetime import datetime, timezone, timedelta

BRT = timezone(timedelta(hours=-3))
ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"

NAME_MAP = {
    "USA": "United States",
    "United States of America": "United States",
    "US": "United States",
    "Korea Republic": "South Korea",
    "Republic of Korea": "South Korea",
    "Czech Republic": "Czechia",
    "Turkey": "Türkiye",
    "Saudi Arabia": "Saudi Arabia",
    "Côte d'Ivoire": "Ivory Coast",
    "Ivory Coast": "Ivory Coast",
}


def _normalize(name: str) -> str:
    return NAME_MAP.get(name, name)


def _stat(stats: list, name: str) -> float:
    for s in stats:
        if s.get("name") == name:
            try:
                return float(s.get("displayValue", 0))
            except (ValueError, TypeError):
                return 0.0
    return 0.0


def _parse_events(details: list, home_id: str, away_id: str) -> list:
    events = []
    for d in details:
        team_id = d.get("team", {}).get("id", "")
        team = "home" if team_id == home_id else "away"
        minute = d.get("clock", {}).get("displayValue", "")
        athlete = ""
        athletes = d.get("athletesInvolved", [])
        if athletes:
            athlete = athletes[0].get("shortName", athletes[0].get("displayName", ""))

        if d.get("yellowCard"):
            events.append({"type": "yellow_card", "minute": minute, "team": team, "player": athlete})
        elif d.get("redCard"):
            events.append({"type": "red_card", "minute": minute, "team": team, "player": athlete})
        elif d.get("scoringPlay"):
            kind = "penalty" if d.get("penaltyKick") else ("own_goal" if d.get("ownGoal") else "goal")
            events.append({"type": kind, "minute": minute, "team": team, "player": athlete})

    return sorted(events, key=lambda e: _minute_sort(e["minute"]))


def _minute_sort(minute: str) -> float:
    try:
        base = minute.replace("'", "").split("+")
        return float(base[0]) + (float(base[1]) / 100 if len(base) > 1 else 0)
    except Exception:
        return 0.0


def fetch_live_scores() -> dict[tuple[str, str], dict]:
    """
    Returns dict keyed by (home_team, away_team) with:
      home_score, away_score, state, minute,
      stats: { home: {...}, away: {...} },
      events: [{ type, minute, team, player }]
    """
    try:
        today_str = datetime.now(BRT).strftime("%Y%m%d")
        resp = httpx.get(ESPN_URL, params={"dates": today_str}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return {}

    scores: dict[tuple[str, str], dict] = {}

    for event in data.get("events", []):
        competitions = event.get("competitions", [])
        if not competitions:
            continue
        comp = competitions[0]
        competitors = comp.get("competitors", [])
        if len(competitors) < 2:
            continue

        home = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
        away = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])

        home_name = _normalize(home.get("team", {}).get("displayName", ""))
        away_name = _normalize(away.get("team", {}).get("displayName", ""))
        home_id = home.get("team", {}).get("id", "")
        away_id = away.get("team", {}).get("id", "")

        try:
            home_score = int(home.get("score", 0))
            away_score = int(away.get("score", 0))
        except (ValueError, TypeError):
            home_score = 0
            away_score = 0

        status_type = event.get("status", {}).get("type", {})
        state = status_type.get("state", "")
        minute = event.get("status", {}).get("displayClock", "").replace("'", "").strip()

        home_stats_raw = home.get("statistics", [])
        away_stats_raw = away.get("statistics", [])

        stats = {
            "home": {
                "corners": int(_stat(home_stats_raw, "wonCorners")),
                "shots": int(_stat(home_stats_raw, "totalShots")),
                "shots_on_target": int(_stat(home_stats_raw, "shotsOnTarget")),
                "fouls": int(_stat(home_stats_raw, "foulsCommitted")),
                "possession": round(_stat(home_stats_raw, "possessionPct"), 1),
            },
            "away": {
                "corners": int(_stat(away_stats_raw, "wonCorners")),
                "shots": int(_stat(away_stats_raw, "totalShots")),
                "shots_on_target": int(_stat(away_stats_raw, "shotsOnTarget")),
                "fouls": int(_stat(away_stats_raw, "foulsCommitted")),
                "possession": round(_stat(away_stats_raw, "possessionPct"), 1),
            },
        }

        details = comp.get("details", [])
        events = _parse_events(details, home_id, away_id)

        scores[(home_name, away_name)] = {
            "home_score": home_score,
            "away_score": away_score,
            "state": state,
            "minute": minute or None,
            "stats": stats,
            "events": events,
        }

    return scores
