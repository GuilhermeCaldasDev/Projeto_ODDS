import math
from typing import Dict, Any, List
import numpy as np
from scipy.stats import poisson


def analyze_form(team: Dict[str, Any]) -> float:
    """Return form score 0-100 based on recent results."""
    form = team.get("form", [])
    if not form:
        return 50.0
    score = 0.0
    weights = [1.0, 0.9, 0.8, 0.7, 0.6]
    total_weight = 0.0
    for i, result in enumerate(form):
        w = weights[i] if i < len(weights) else 0.5
        if result == "W":
            score += 100 * w
        elif result == "D":
            score += 50 * w
        else:
            score += 0 * w
        total_weight += w
    return round(score / total_weight, 1) if total_weight > 0 else 50.0


def calculate_elo_score(team: Dict[str, Any]) -> float:
    """Derive an ELO-style score from ranking, attack, defense, and form."""
    ranking = team.get("ranking", 50)
    attack = team.get("attack_rating", 70)
    defense = team.get("defense_rating", 70)
    form_score = analyze_form(team)

    # ELO-like base score: lower ranking = stronger team
    ranking_score = max(0, (100 - ranking) * 0.5)
    base = (attack * 0.35 + defense * 0.35 + ranking_score * 0.2 + form_score * 0.1)
    return base


def calculate_win_probabilities(team1: Dict[str, Any], team2: Dict[str, Any]) -> Dict[str, float]:
    """Calculate 1X2 win probabilities using ELO-style calculation."""
    elo1 = calculate_elo_score(team1)
    elo2 = calculate_elo_score(team2)

    diff = elo1 - elo2
    # Sigmoid transformation
    win1 = 1 / (1 + math.exp(-diff / 15))
    win2 = 1 / (1 + math.exp(diff / 15))

    # Introduce draw probability
    draw_base = 0.28
    adjustment = 1 - draw_base
    win1_adj = win1 * adjustment
    win2_adj = win2 * adjustment

    # Normalize
    total = win1_adj + draw_base + win2_adj
    return {
        "home": round(win1_adj / total, 4),
        "draw": round(draw_base / total, 4),
        "away": round(win2_adj / total, 4),
    }


def predict_goals(team1: Dict[str, Any], team2: Dict[str, Any]) -> Dict[str, Any]:
    """Use Poisson distribution to predict expected goals and score probabilities."""
    avg_rating = 70.0  # baseline average team rating

    # Attack strength relative to average
    home_attack_str = team1.get("attack_rating", 70) / avg_rating
    away_attack_str = team2.get("attack_rating", 70) / avg_rating

    # Defense weakness: higher defense = harder to score against (lower multiplier)
    home_def_str = team1.get("defense_rating", 70) / avg_rating
    away_def_str = team2.get("defense_rating", 70) / avg_rating

    # Base expected goals for an average team in World Cup = 1.2 goals/game
    base_goals = 1.2
    home_advantage = 1.08

    # Home team lambda: home attack vs away defense
    home_lambda = base_goals * home_attack_str * (1.0 / away_def_str) * home_advantage
    # Away team lambda: away attack vs home defense
    away_lambda = base_goals * away_attack_str * (1.0 / home_def_str)

    home_lambda = max(0.3, min(4.0, home_lambda))
    away_lambda = max(0.3, min(4.0, away_lambda))

    # Compute probability matrix
    max_goals = 8
    score_probs = {}
    over_2_5 = 0.0
    btts = 0.0
    home_win_prob = 0.0
    draw_prob = 0.0
    away_win_prob = 0.0

    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob = poisson.pmf(i, home_lambda) * poisson.pmf(j, away_lambda)
            score_probs[f"{i}-{j}"] = round(prob, 4)
            if i + j > 2.5:
                over_2_5 += prob
            if i > 0 and j > 0:
                btts += prob
            if i > j:
                home_win_prob += prob
            elif i == j:
                draw_prob += prob
            else:
                away_win_prob += prob

    # Most likely score
    best_score = max(score_probs, key=score_probs.get)

    return {
        "home_expected_goals": round(home_lambda, 2),
        "away_expected_goals": round(away_lambda, 2),
        "predicted_score": best_score,
        "over_2_5_probability": round(over_2_5, 4),
        "btts_probability": round(btts, 4),
        "top_scores": sorted(score_probs.items(), key=lambda x: -x[1])[:5],
        "home_win_prob": round(home_win_prob, 4),
        "draw_prob": round(draw_prob, 4),
        "away_win_prob": round(away_win_prob, 4),
    }


def prob_to_odds(prob: float) -> float:
    """Convert probability to decimal odds."""
    if prob <= 0:
        return 99.0
    return round(1 / prob, 2)


def calculate_value_bet(probability: float, implied_odds: float) -> Dict[str, Any]:
    """Identify value bets: value = prob * odds - 1."""
    implied_prob = 1 / implied_odds if implied_odds > 0 else 1
    value = probability * implied_odds - 1
    has_value = value > 0.05
    return {
        "has_value": has_value,
        "value_percentage": round(value * 100, 1),
        "edge": round((probability - implied_prob) * 100, 1),
    }


def get_betting_tips(match: Dict[str, Any], team1: Dict[str, Any], team2: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return structured betting tips with confidence levels for various markets."""
    win_probs = calculate_win_probabilities(team1, team2)
    goals_pred = predict_goals(team1, team2)
    form1 = analyze_form(team1)
    form2 = analyze_form(team2)

    tips = []

    # 1X2 tip
    home_p = win_probs["home"]
    draw_p = win_probs["draw"]
    away_p = win_probs["away"]

    best_1x2 = max([(home_p, "1", team1["name"]), (draw_p, "X", "Draw"), (away_p, "2", team2["name"])], key=lambda x: x[0])
    conf_1x2 = round(best_1x2[0] * 100, 1)
    odds_1x2 = prob_to_odds(best_1x2[0])
    value_1x2 = calculate_value_bet(best_1x2[0], odds_1x2)

    tips.append({
        "market": "1X2",
        "recommendation": best_1x2[1],
        "description": f"{best_1x2[2]} to win" if best_1x2[1] != "X" else "Match ends in a Draw",
        "probability": best_1x2[0],
        "confidence": conf_1x2,
        "odds_estimate": odds_1x2,
        "reasoning": (
            f"{team1['name']} has form score {form1}/100 vs {team2['name']} with {form2}/100. "
            f"ELO-based probability: Home {round(home_p*100,1)}%, Draw {round(draw_p*100,1)}%, Away {round(away_p*100,1)}%."
        ),
        "value": value_1x2,
    })

    # Over/Under 2.5 goals
    over_p = goals_pred["over_2_5_probability"]
    under_p = 1 - over_p
    ou_rec = "Over 2.5" if over_p > under_p else "Under 2.5"
    ou_prob = over_p if over_p > under_p else under_p
    conf_ou = round(ou_prob * 100, 1)
    odds_ou = prob_to_odds(ou_prob)
    value_ou = calculate_value_bet(ou_prob, odds_ou)

    tips.append({
        "market": "Over/Under 2.5",
        "recommendation": ou_rec,
        "description": f"Total goals {ou_rec}",
        "probability": round(ou_prob, 4),
        "confidence": conf_ou,
        "odds_estimate": odds_ou,
        "reasoning": (
            f"Expected goals: {team1['name']} {goals_pred['home_expected_goals']} + "
            f"{team2['name']} {goals_pred['away_expected_goals']} = "
            f"{round(goals_pred['home_expected_goals'] + goals_pred['away_expected_goals'], 2)} total. "
            f"Over 2.5 probability: {round(over_p*100,1)}%."
        ),
        "value": value_ou,
    })

    # BTTS
    btts_p = goals_pred["btts_probability"]
    no_btts_p = 1 - btts_p
    btts_rec = "Yes" if btts_p > no_btts_p else "No"
    btts_prob = btts_p if btts_p > no_btts_p else no_btts_p
    conf_btts = round(btts_prob * 100, 1)
    odds_btts = prob_to_odds(btts_prob)
    value_btts = calculate_value_bet(btts_prob, odds_btts)

    tips.append({
        "market": "BTTS",
        "recommendation": btts_rec,
        "description": f"Both Teams to Score: {btts_rec}",
        "probability": round(btts_prob, 4),
        "confidence": conf_btts,
        "odds_estimate": odds_btts,
        "reasoning": (
            f"Attack: {team1['name']} avg {team1['goals_scored_avg']} goals/game, "
            f"{team2['name']} avg {team2['goals_scored_avg']} goals/game. "
            f"BTTS probability: {round(btts_p*100,1)}%."
        ),
        "value": value_btts,
    })

    # Asian Handicap
    elo1 = calculate_elo_score(team1)
    elo2 = calculate_elo_score(team2)
    diff = elo1 - elo2
    if abs(diff) < 5:
        handicap_val = 0
    elif diff > 0:
        handicap_val = -round(diff / 10 * 0.5, 1)
    else:
        handicap_val = round(abs(diff) / 10 * 0.5, 1)

    ah_prob = 0.5 + (diff / 200)
    ah_prob = max(0.35, min(0.75, ah_prob))
    conf_ah = round(ah_prob * 100, 1)
    odds_ah = prob_to_odds(ah_prob)
    ah_team = team1["name"] if diff >= 0 else team2["name"]
    ah_direction = handicap_val if diff >= 0 else -handicap_val
    value_ah = calculate_value_bet(ah_prob, odds_ah)

    tips.append({
        "market": "Asian Handicap",
        "recommendation": f"{ah_team} {ah_direction:+.1f}",
        "description": f"{ah_team} with {ah_direction:+.1f} Asian handicap",
        "probability": round(ah_prob, 4),
        "confidence": conf_ah,
        "odds_estimate": odds_ah,
        "reasoning": (
            f"ELO difference: {round(diff, 1)}. "
            f"{ah_team} is the stronger side based on rankings and ratings. "
            f"Recommended handicap: {ah_direction:+.1f} goals."
        ),
        "value": value_ah,
    })

    return tips
