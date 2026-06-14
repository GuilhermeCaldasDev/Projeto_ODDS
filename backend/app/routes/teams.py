from fastapi import APIRouter, HTTPException
from app.data.world_cup_data import TEAMS, get_team, get_teams_by_group
from app.services.analysis import analyze_form
from app.services.tournament_stats import fetch_tournament_stats

router = APIRouter()

GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]


@router.get("/teams")
def get_all_teams():
    result = []
    for team in TEAMS:
        form_score = analyze_form(team)
        result.append({**team, "form_score": form_score})
    return result


@router.get("/teams/tournament-stats")
def get_tournament_stats():
    return fetch_tournament_stats()


@router.get("/teams/{team_name}")
def get_team_detail(team_name: str):
    team = get_team(team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    form_score = analyze_form(team)

    # Fetch real tournament stats for this team
    all_stats = fetch_tournament_stats()
    tournament = all_stats.get(team["name"])

    return {**team, "form_score": form_score, "tournament_stats": tournament}


@router.get("/groups")
def get_groups():
    # Use real ESPN standings when available, fallback to simulation
    espn_stats = fetch_tournament_stats()
    result = {}

    for group in GROUPS:
        teams = get_teams_by_group(group)
        standings = []
        for team in teams:
            form_score = analyze_form(team)
            real = espn_stats.get(team["name"])

            if real and real.get("played", 0) > 0:
                standings.append({
                    "team": team["name"],
                    "flag": team["flag"],
                    "ranking": team["ranking"],
                    "played": real["played"],
                    "won": real["wins"],
                    "drawn": real["draws"],
                    "lost": real["losses"],
                    "goals_for": real["goals_for"],
                    "goals_against": real["goals_against"],
                    "goal_diff": real["goal_diff"],
                    "points": real["points"],
                    "form_score": form_score,
                })
            else:
                standings.append({
                    "team": team["name"],
                    "flag": team["flag"],
                    "ranking": team["ranking"],
                    "played": 0,
                    "won": 0,
                    "drawn": 0,
                    "lost": 0,
                    "goals_for": 0,
                    "goals_against": 0,
                    "goal_diff": 0,
                    "points": 0,
                    "form_score": form_score,
                })

        standings.sort(key=lambda x: (-x["points"], -x["goal_diff"], -x["goals_for"]))
        result[group] = standings

    return result
