import math
from typing import Dict, Any, List, Tuple
from app.services.analysis import calculate_win_probabilities, predict_goals, analyze_form


def _simulate_match(team1: Dict, team2: Dict) -> Tuple[str, float, float, float]:
    """Return (winner_name, home_prob, draw_prob, away_prob)."""
    wp = calculate_win_probabilities(team1, team2)
    gp = predict_goals(team1, team2)
    home_p = (wp["home"] + gp["home_win_prob"]) / 2
    away_p = (wp["away"] + gp["away_win_prob"]) / 2
    draw_p = 1 - home_p - away_p
    if home_p >= away_p:
        winner = team1["name"]
    else:
        winner = team2["name"]
    return winner, round(home_p, 4), round(draw_p, 4), round(away_p, 4)


def simulate_group_with_results(teams: List[Dict], group_matches: List[Dict]) -> List[Dict]:
    """
    Simulate round-robin using real scores for finished matches and
    model probabilities for upcoming/live matches.
    """
    standings = {t["name"]: {"team": t, "pts": 0.0, "gf": 0.0, "ga": 0.0, "w": 0, "d": 0, "l": 0} for t in teams}
    team_map = {t["name"]: t for t in teams}

    for match in group_matches:
        t1 = team_map.get(match["home_team"])
        t2 = team_map.get(match["away_team"])
        if not t1 or not t2:
            continue

        if match.get("home_score") is not None:
            # Use real result
            hg = match["home_score"]
            ag = match["away_score"]
            standings[t1["name"]]["gf"] += hg
            standings[t1["name"]]["ga"] += ag
            standings[t2["name"]]["gf"] += ag
            standings[t2["name"]]["ga"] += hg
            if hg > ag:
                standings[t1["name"]]["pts"] += 3
                standings[t1["name"]]["w"] += 1
                standings[t2["name"]]["l"] += 1
            elif hg < ag:
                standings[t2["name"]]["pts"] += 3
                standings[t2["name"]]["w"] += 1
                standings[t1["name"]]["l"] += 1
            else:
                standings[t1["name"]]["pts"] += 1
                standings[t2["name"]]["pts"] += 1
                standings[t1["name"]]["d"] += 1
                standings[t2["name"]]["d"] += 1
        else:
            # Simulate unplayed match
            wp = calculate_win_probabilities(t1, t2)
            gp = predict_goals(t1, t2)
            home_xg = gp["home_expected_goals"]
            away_xg = gp["away_expected_goals"]
            standings[t1["name"]]["gf"] += home_xg
            standings[t1["name"]]["ga"] += away_xg
            standings[t2["name"]]["gf"] += away_xg
            standings[t2["name"]]["ga"] += home_xg
            h, d, a = wp["home"], wp["draw"], wp["away"]
            standings[t1["name"]]["pts"] += h * 3 + d * 1
            standings[t2["name"]]["pts"] += a * 3 + d * 1
            if h > a:
                standings[t1["name"]]["w"] += 1
                standings[t2["name"]]["l"] += 1
            elif a > h:
                standings[t2["name"]]["w"] += 1
                standings[t1["name"]]["l"] += 1
            else:
                standings[t1["name"]]["d"] += 1
                standings[t2["name"]]["d"] += 1

    result = []
    for name, s in standings.items():
        t = s["team"]
        result.append({
            "name": t["name"],
            "flag": t["flag"],
            "ranking": t["ranking"],
            "attack_rating": t["attack_rating"],
            "defense_rating": t["defense_rating"],
            "form_score": analyze_form(t),
            "predicted_pts": round(s["pts"], 1),
            "predicted_gf": round(s["gf"], 1),
            "predicted_ga": round(s["ga"], 1),
            "predicted_gd": round(s["gf"] - s["ga"], 1),
            "predicted_w": s["w"],
            "predicted_d": s["d"],
            "predicted_l": s["l"],
        })

    result.sort(key=lambda x: (-x["predicted_pts"], -x["predicted_gd"], -x["predicted_gf"]))
    for i, r in enumerate(result):
        r["predicted_position"] = i + 1
    return result


def simulate_all_groups(teams_by_group: Dict[str, List[Dict]], matches: List[Dict] = None) -> Dict[str, List[Dict]]:
    return {
        group: simulate_group_with_results(
            teams,
            [m for m in (matches or []) if m.get("group") == group]
        )
        for group, teams in teams_by_group.items()
    }


def get_third_place_qualifiers(group_results: Dict[str, List[Dict]], n: int = 8) -> List[Dict]:
    """Pick best n third-place teams across all groups."""
    thirds = []
    for group, standings in group_results.items():
        if len(standings) >= 3:
            third = standings[2].copy()
            third["group"] = group
            thirds.append(third)
    thirds.sort(key=lambda x: (-x["predicted_pts"], -x["predicted_gd"], -x["predicted_gf"]))
    return thirds[:n]


def simulate_ko_match(team1: Dict, team2: Dict) -> Dict:
    """Simulate a knockout match (no draws — extra time/pens handled via adjustment)."""
    wp = calculate_win_probabilities(team1, team2)
    gp = predict_goals(team1, team2)
    home_p = (wp["home"] + gp["home_win_prob"]) / 2
    away_p = (wp["away"] + gp["away_win_prob"]) / 2
    total = home_p + away_p
    home_p_adj = home_p / total
    away_p_adj = away_p / total
    winner = team1 if home_p_adj >= away_p_adj else team2
    loser = team2 if winner == team1 else team1
    return {
        "home": team1["name"],
        "home_flag": team1["flag"],
        "away": team2["name"],
        "away_flag": team2["flag"],
        "home_win_prob": round(home_p_adj, 4),
        "away_win_prob": round(away_p_adj, 4),
        "predicted_winner": winner["name"],
        "predicted_winner_flag": winner["flag"],
        "predicted_score": gp["predicted_score"],
        "home_xg": gp["home_expected_goals"],
        "away_xg": gp["away_expected_goals"],
    }
