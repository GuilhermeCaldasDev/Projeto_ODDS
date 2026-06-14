"""
Fetches real-time Copa 2026 tournament stats from ESPN.
Combines standings (W/D/L/GF/GA/Pts) with per-match stats (shots, corners, fouls).
"""
import httpx
from datetime import datetime, timezone, timedelta, date

BRT = timezone(timedelta(hours=-3))

ESPN_STANDINGS = "https://site.api.espn.com/apis/v2/sports/soccer/fifa.world/standings"
ESPN_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"

TOURNAMENT_START = date(2026, 6, 11)

NAME_MAP = {
    "USA": "United States",
    "United States of America": "United States",
    "Bosnia-Herzegovina": "Bosnia and Herzegovina",
    "Korea Republic": "South Korea",
    "Republic of Korea": "South Korea",
    "Czech Republic": "Czechia",
    "Turkey": "Türkiye",
    "Côte d'Ivoire": "Ivory Coast",
    "Congo DR": "DR Congo",
    "Curaçao": "Curaçao",
}


def _norm(name: str) -> str:
    return NAME_MAP.get(name, name)


def _safe_int(val) -> int:
    try:
        return int(float(val or 0))
    except (ValueError, TypeError):
        return 0


def fetch_tournament_stats() -> dict[str, dict]:
    """
    Returns dict keyed by normalized team name with:
      group, played, wins, draws, losses, goals_for, goals_against,
      goal_diff, points, shots, shots_on_target, corners, fouls,
      yellow_cards, red_cards
    """
    result: dict[str, dict] = {}

    # --- Standings (W/D/L/GF/GA/Pts) ---
    try:
        r = httpx.get(ESPN_STANDINGS, timeout=6)
        r.raise_for_status()
        data = r.json()
        for child in data.get("children", []):
            group = child.get("name", "").replace("Group ", "")
            for entry in child.get("standings", {}).get("entries", []):
                team_name = _norm(entry.get("team", {}).get("displayName", ""))
                stats = {s["name"]: s.get("displayValue", "0") for s in entry.get("stats", [])}
                result[team_name] = {
                    "group": group,
                    "played": _safe_int(stats.get("gamesPlayed", 0)),
                    "wins": _safe_int(stats.get("wins", 0)),
                    "draws": _safe_int(stats.get("ties", 0)),
                    "losses": _safe_int(stats.get("losses", 0)),
                    "goals_for": _safe_int(stats.get("pointsFor", 0)),
                    "goals_against": _safe_int(stats.get("pointsAgainst", 0)),
                    "goal_diff": _safe_int(stats.get("pointDifferential", 0)),
                    "points": _safe_int(stats.get("points", 0)),
                    "shots": 0,
                    "shots_on_target": 0,
                    "corners": 0,
                    "fouls": 0,
                    "yellow_cards": 0,
                    "red_cards": 0,
                }
    except Exception:
        pass

    # --- Match stats (shots, corners, fouls, cards) ---
    today = datetime.now(BRT).date()
    current = TOURNAMENT_START
    while current <= today:
        try:
            r = httpx.get(ESPN_SCOREBOARD, params={"dates": current.strftime("%Y%m%d")}, timeout=6)
            r.raise_for_status()
            events = r.json().get("events", [])
            for event in events:
                state = event.get("status", {}).get("type", {}).get("state", "")
                if state not in ("in", "post"):
                    continue
                comp = event.get("competitions", [{}])[0]

                # Count cards from details
                team_yellows: dict[str, int] = {}
                team_reds: dict[str, int] = {}
                competitors = comp.get("competitors", [])
                id_to_name = {
                    c.get("team", {}).get("id"): _norm(c.get("team", {}).get("displayName", ""))
                    for c in competitors
                }
                for detail in comp.get("details", []):
                    tid = detail.get("team", {}).get("id", "")
                    tname = id_to_name.get(tid, "")
                    if not tname:
                        continue
                    if detail.get("yellowCard"):
                        team_yellows[tname] = team_yellows.get(tname, 0) + 1
                    if detail.get("redCard"):
                        team_reds[tname] = team_reds.get(tname, 0) + 1

                for c in competitors:
                    name = _norm(c.get("team", {}).get("displayName", ""))
                    if name not in result:
                        continue
                    raw = {s["name"]: s.get("displayValue", "0") for s in c.get("statistics", [])}
                    result[name]["shots"] += _safe_int(raw.get("totalShots", 0))
                    result[name]["shots_on_target"] += _safe_int(raw.get("shotsOnTarget", 0))
                    result[name]["corners"] += _safe_int(raw.get("wonCorners", 0))
                    result[name]["fouls"] += _safe_int(raw.get("foulsCommitted", 0))
                    result[name]["yellow_cards"] += team_yellows.get(name, 0)
                    result[name]["red_cards"] += team_reds.get(name, 0)
        except Exception:
            pass
        current += timedelta(days=1)

    return result
