from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timezone, timedelta

BRT = timezone(timedelta(hours=-3))
from app.data.world_cup_data import MATCHES, get_team
from app.services.analysis import get_betting_tips, predict_goals, calculate_win_probabilities

router = APIRouter()


def _build_all_predictions(only_today: bool = False):
    today_str = datetime.now(BRT).date().isoformat()
    all_tips = []
    for match in MATCHES:
        if only_today and match["date"] != today_str:
            continue
        if match.get("home_score") is not None:
            continue
        team1 = get_team(match["home_team"])
        team2 = get_team(match["away_team"])
        if not team1 or not team2:
            continue
        tips = get_betting_tips(match, team1, team2)
        goals = predict_goals(team1, team2)
        win_probs = calculate_win_probabilities(team1, team2)
        for tip in tips:
            all_tips.append({
                "match_id": match["id"],
                "home_team": match["home_team"],
                "home_flag": team1["flag"],
                "away_team": match["away_team"],
                "away_flag": team2["flag"],
                "date": match["date"],
                "time": match["time"],
                "venue": match["venue"],
                "group": match["group"],
                "predicted_score": goals["predicted_score"],
                "win_probabilities": win_probs,
                **tip,
            })
    return all_tips


@router.get("/predictions/top")
def get_top_predictions():
    all_tips = _build_all_predictions(only_today=True)
    filtered = [t for t in all_tips if t["probability"] > 0.50]
    return sorted(filtered, key=lambda t: (t["date"], t["time"], -t["confidence"]))


@router.get("/predictions/all")
def get_all_predictions(market: Optional[str] = Query(None)):
    all_tips = _build_all_predictions()
    if market:
        all_tips = [t for t in all_tips if t["market"].lower().replace("/", "").replace(" ", "") == market.lower().replace("/", "").replace(" ", "")]
    return sorted(all_tips, key=lambda t: -t["confidence"])
