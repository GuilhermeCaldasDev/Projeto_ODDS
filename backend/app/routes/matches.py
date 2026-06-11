from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.data.world_cup_data import MATCHES, get_match, get_team, get_matches_by_group
from app.services.analysis import (
    calculate_win_probabilities,
    predict_goals,
    get_betting_tips,
    analyze_form,
)

router = APIRouter()


@router.get("/matches")
def get_all_matches(group: Optional[str] = Query(None)):
    if group:
        matches = get_matches_by_group(group.upper())
    else:
        matches = MATCHES

    result = []
    for match in matches:
        team1 = get_team(match["home_team"])
        team2 = get_team(match["away_team"])
        if not team1 or not team2:
            continue
        win_probs = calculate_win_probabilities(team1, team2)
        goals_pred = predict_goals(team1, team2)
        tips = get_betting_tips(match, team1, team2)
        top_tip = max(tips, key=lambda t: t["confidence"])

        result.append({
            **match,
            "home_team_data": team1,
            "away_team_data": team2,
            "win_probabilities": win_probs,
            "predicted_score": goals_pred["predicted_score"],
            "top_tip": top_tip,
        })
    return result


@router.get("/matches/{match_id}")
def get_match_detail(match_id: int):
    match = get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    team1 = get_team(match["home_team"])
    team2 = get_team(match["away_team"])
    if not team1 or not team2:
        raise HTTPException(status_code=404, detail="Team data not found")

    win_probs = calculate_win_probabilities(team1, team2)
    goals_pred = predict_goals(team1, team2)
    tips = get_betting_tips(match, team1, team2)
    form1 = analyze_form(team1)
    form2 = analyze_form(team2)

    return {
        **match,
        "home_team_data": team1,
        "away_team_data": team2,
        "win_probabilities": win_probs,
        "goals_prediction": goals_pred,
        "betting_tips": tips,
        "home_form_score": form1,
        "away_form_score": form2,
    }


@router.get("/matches/{match_id}/predictions")
def get_match_predictions(match_id: int):
    match = get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    team1 = get_team(match["home_team"])
    team2 = get_team(match["away_team"])
    if not team1 or not team2:
        raise HTTPException(status_code=404, detail="Team data not found")

    win_probs = calculate_win_probabilities(team1, team2)
    goals_pred = predict_goals(team1, team2)
    tips = get_betting_tips(match, team1, team2)
    form1 = analyze_form(team1)
    form2 = analyze_form(team2)

    return {
        "match_id": match_id,
        "home_team": match["home_team"],
        "away_team": match["away_team"],
        "win_probabilities": win_probs,
        "goals_prediction": goals_pred,
        "betting_tips": sorted(tips, key=lambda t: -t["confidence"]),
        "home_form_score": form1,
        "away_form_score": form2,
        "analysis_summary": (
            f"{team1['name']} (ranked #{team1['ranking']}) vs {team2['name']} (ranked #{team2['ranking']}). "
            f"Predicted score: {goals_pred['predicted_score']}. "
            f"Home win probability: {round(win_probs['home']*100, 1)}%."
        ),
    }
