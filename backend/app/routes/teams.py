from fastapi import APIRouter, HTTPException
from app.data.world_cup_data import TEAMS, get_team, get_teams_by_group
from app.services.analysis import analyze_form

router = APIRouter()

GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H"]


@router.get("/teams")
def get_all_teams():
    result = []
    for team in TEAMS:
        form_score = analyze_form(team)
        result.append({**team, "form_score": form_score})
    return result


@router.get("/teams/{team_name}")
def get_team_detail(team_name: str):
    team = get_team(team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    form_score = analyze_form(team)
    return {**team, "form_score": form_score}


@router.get("/groups")
def get_groups():
    result = {}
    for group in GROUPS:
        teams = get_teams_by_group(group)
        standings = []
        for team in teams:
            form_score = analyze_form(team)
            # Simulated standings based on form and ratings
            won = sum(1 for r in team["form"] if r == "W")
            drawn = sum(1 for r in team["form"] if r == "D")
            lost = sum(1 for r in team["form"] if r == "L")
            # Use last 3 results for group simulations
            last3 = team["form"][:3]
            pts = sum(3 if r == "W" else (1 if r == "D" else 0) for r in last3)
            gf = round(team["goals_scored_avg"] * 3)
            ga = round(team["goals_conceded_avg"] * 3)
            standings.append({
                "team": team["name"],
                "flag": team["flag"],
                "ranking": team["ranking"],
                "played": 3,
                "won": last3.count("W"),
                "drawn": last3.count("D"),
                "lost": last3.count("L"),
                "goals_for": gf,
                "goals_against": ga,
                "goal_diff": gf - ga,
                "points": pts,
                "form_score": form_score,
            })
        standings.sort(key=lambda x: (-x["points"], -x["goal_diff"], -x["goals_for"]))
        result[group] = standings
    return result
