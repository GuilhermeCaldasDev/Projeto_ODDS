from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime, timezone, timedelta, date

BRT = timezone(timedelta(hours=-3))

from app.data.world_cup_data import MATCHES, get_match, get_team, get_matches_by_group
from app.services.analysis import (
    calculate_win_probabilities,
    predict_goals,
    get_betting_tips,
    analyze_form,
)
from app.services.live_scores import fetch_live_scores
from app.services.odds_fetcher import enrich_tips_with_real_odds, is_configured as odds_configured

router = APIRouter()

# Match duration in minutes (90 min + up to 20 min stoppage/extra time)
MATCH_DURATION_MINUTES = 110


def compute_status(match: dict) -> str:
    if match.get("home_score") is not None:
        return "finished"

    now_brt = datetime.now(BRT)
    today = now_brt.date()
    match_date = date.fromisoformat(match["date"])

    if match_date < today:
        return "finished"
    if match_date > today:
        return "upcoming"

    # Same day — compare current BRT time with match kickoff (stored in ET = BRT-1h)
    match_time_str = match.get("time", "00:00")
    h, m = map(int, match_time_str.split(":"))
    kickoff_brt_minutes = ((h + 1) % 24) * 60 + m  # ET → BRT (+1h)
    now_minutes = now_brt.hour * 60 + now_brt.minute

    if now_minutes < kickoff_brt_minutes:
        return "upcoming"
    if now_minutes <= kickoff_brt_minutes + MATCH_DURATION_MINUTES:
        return "live"
    return "finished"


@router.get("/matches")
def get_all_matches(group: Optional[str] = Query(None)):
    if group:
        matches = get_matches_by_group(group.upper())
    else:
        matches = MATCHES

    # Fetch live scores once for all matches
    live_scores = fetch_live_scores()

    result = []
    for match in matches:
        team1 = get_team(match["home_team"])
        team2 = get_team(match["away_team"])
        if not team1 or not team2:
            continue
        win_probs = calculate_win_probabilities(team1, team2)
        goals_pred = predict_goals(team1, team2)
        tips = get_betting_tips(match, team1, team2)
        tips = enrich_tips_with_real_odds(tips, match["home_team"], match["away_team"])
        top_tip = max(tips, key=lambda t: t["confidence"])

        # Try to get real-time score/stats from ESPN
        live = live_scores.get((match["home_team"], match["away_team"]))
        if live:
            home_score = live["home_score"]
            away_score = live["away_score"]
            espn_state = live["state"]
            minute = live.get("minute")
            live_stats = live.get("stats")
            live_events = live.get("events", [])
            if espn_state == "post":
                status = "finished"
            elif espn_state == "in":
                status = "live"
            else:
                status = compute_status(match)
        else:
            home_score = match.get("home_score")
            away_score = match.get("away_score")
            status = compute_status(match)
            minute = None
            live_stats = None
            live_events = []

        result.append({
            **match,
            "status": status,
            "home_score": home_score,
            "away_score": away_score,
            "minute": minute,
            "live_stats": live_stats,
            "live_events": live_events,
            "home_team_data": team1,
            "away_team_data": team2,
            "win_probabilities": win_probs,
            "predicted_score": goals_pred["predicted_score"],
            "top_tip": top_tip,
        })
    result.sort(key=lambda m: (m["date"], m["time"]))
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
    tips = enrich_tips_with_real_odds(tips, match["home_team"], match["away_team"])
    form1 = analyze_form(team1)
    form2 = analyze_form(team2)

    live_scores = fetch_live_scores()
    live = live_scores.get((match["home_team"], match["away_team"]))
    if live:
        home_score = live["home_score"]
        away_score = live["away_score"]
        espn_state = live["state"]
        minute = live.get("minute")
        live_stats = live.get("stats")
        live_events = live.get("events", [])
        if espn_state == "post":
            status = "finished"
        elif espn_state == "in":
            status = "live"
        else:
            status = compute_status(match)
    else:
        home_score = match.get("home_score")
        away_score = match.get("away_score")
        status = compute_status(match)
        minute = None
        live_stats = None
        live_events = []

    return {
        **match,
        "status": status,
        "home_score": home_score,
        "away_score": away_score,
        "minute": minute,
        "live_stats": live_stats,
        "live_events": live_events,
        "home_team_data": team1,
        "away_team_data": team2,
        "win_probabilities": win_probs,
        "goals_prediction": goals_pred,
        "betting_tips": tips,
        "home_form_score": form1,
        "away_form_score": form2,
        "odds_api_configured": odds_configured(),
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
