import math
from typing import Dict, Any, List
import numpy as np
from scipy.stats import poisson


# ── Helpers de forma ──────────────────────────────────────────────────────────

def analyze_form(team: Dict[str, Any]) -> float:
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
        total_weight += w
    return round(score / total_weight, 1) if total_weight > 0 else 50.0


def form_trend(team: Dict[str, Any]) -> str:
    form = team.get("form", [])
    if len(form) < 4:
        return "indefinida"
    recent_pts = sum(3 if r == "W" else 1 if r == "D" else 0 for r in form[:3])
    older_pts  = sum(3 if r == "W" else 1 if r == "D" else 0 for r in form[3:])
    if recent_pts > older_pts:
        return "ascendente"
    elif recent_pts < older_pts:
        return "declinante"
    return "estável"


def infer_style(team: Dict[str, Any]) -> str:
    ranking = team.get("ranking", 50)
    attack  = team.get("attack_rating", 70)
    defense = team.get("defense_rating", 70)
    if ranking <= 10 and attack >= 82:
        return "Alta pressão / Ofensivo"
    if ranking <= 20 and (attack + defense) / 2 >= 74:
        return "Posse de bola / Pressing"
    if attack >= defense + 8:
        return "Ofensivo / Contra-ataque"
    if defense >= attack + 8:
        return "Defensivo / Bloco baixo"
    if ranking <= 40:
        return "Equilibrado / Organizado"
    return "Contra-ataque / Reativo"


def infer_formation(team: Dict[str, Any]) -> str:
    ranking = team.get("ranking", 50)
    attack  = team.get("attack_rating", 70)
    defense = team.get("defense_rating", 70)
    if ranking <= 12:
        return "4-3-3"
    if attack >= defense + 6:
        return "4-2-3-1"
    if defense >= attack + 6:
        return "5-3-2"
    if ranking <= 35:
        return "4-4-2"
    return "4-5-1 / 5-4-1"


def style_matchup(s1: str, s2: str) -> str:
    if "Alta pressão" in s1 and "Defensivo" in s2:
        return "Equipe da casa deve dominar territorialmente contra bloco baixo — jogo pode ter poucos gols mas com boa pressão."
    if "Posse de bola" in s1 and "Contra-ataque" in s2:
        return "Disputa tática: posse vs contra-ataque. Visitante pode aproveitar espaços deixados pela equipe de casa."
    if "Ofensivo" in s1 and "Ofensivo" in s2:
        return "Jogo ofensivo esperado dos dois lados — alto potencial de gols e escanteios."
    if "Defensivo" in s1 and "Defensivo" in s2:
        return "Duelo fechado e físico — mercado de poucos gols favorecido."
    return "Confronto equilibrado — resultado aberto."


def host_advantage_note(team: Dict[str, Any]) -> str:
    host_nations = {"United States", "USA", "Canada", "Mexico"}
    if team.get("name") in host_nations:
        return f"{team['name']} joga em casa na Copa 2026 com apoio total da torcida."
    return ""


def recent_results_summary(team: Dict[str, Any]) -> str:
    results = team.get("recent_results", [])[:3]
    if not results:
        return ""
    parts = [f"{r['opponent']} ({r['result']} {r['score']})" for r in results]
    return f"Últimos 3 jogos: {', '.join(parts)}"


# ── ELO e probabilidades ──────────────────────────────────────────────────────

def calculate_elo_score(team: Dict[str, Any]) -> float:
    ranking   = team.get("ranking", 50)
    attack    = team.get("attack_rating", 70)
    defense   = team.get("defense_rating", 70)
    form_score = analyze_form(team)
    ranking_score = max(0, (100 - ranking) * 0.5)
    return attack * 0.35 + defense * 0.35 + ranking_score * 0.2 + form_score * 0.1


def calculate_win_probabilities(team1: Dict[str, Any], team2: Dict[str, Any]) -> Dict[str, float]:
    elo1 = calculate_elo_score(team1)
    elo2 = calculate_elo_score(team2)
    diff = elo1 - elo2
    win1 = 1 / (1 + math.exp(-diff / 15))
    win2 = 1 / (1 + math.exp(diff / 15))
    draw_base = 0.28
    adjustment = 1 - draw_base
    win1_adj = win1 * adjustment
    win2_adj = win2 * adjustment
    total = win1_adj + draw_base + win2_adj
    return {
        "home": round(win1_adj / total, 4),
        "draw": round(draw_base / total, 4),
        "away": round(win2_adj / total, 4),
    }


def predict_goals(team1: Dict[str, Any], team2: Dict[str, Any]) -> Dict[str, Any]:
    avg_rating = 70.0
    home_attack_str = team1.get("attack_rating", 70) / avg_rating
    away_attack_str = team2.get("attack_rating", 70) / avg_rating
    home_def_str    = team1.get("defense_rating", 70) / avg_rating
    away_def_str    = team2.get("defense_rating", 70) / avg_rating
    base_goals = 1.2
    home_advantage = 1.08
    home_lambda = base_goals * home_attack_str * (1.0 / away_def_str) * home_advantage
    away_lambda = base_goals * away_attack_str * (1.0 / home_def_str)
    home_lambda = max(0.3, min(4.0, home_lambda))
    away_lambda = max(0.3, min(4.0, away_lambda))
    max_goals = 8
    score_probs = {}
    over_2_5 = 0.0
    btts = 0.0
    home_win_prob = 0.0
    draw_prob = 0.0
    away_win_prob = 0.0
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob = float(poisson.pmf(i, home_lambda) * poisson.pmf(j, away_lambda))
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
    if prob <= 0:
        return 99.0
    return round(1 / prob, 2)


def calculate_value_bet(probability: float, implied_odds: float) -> Dict[str, Any]:
    implied_prob = 1 / implied_odds if implied_odds > 0 else 1
    value = probability * implied_odds - 1
    has_value = bool(value > 0.05)
    return {
        "has_value": has_value,
        "value_percentage": round(float(value) * 100, 1),
        "edge": round(float(probability - implied_prob) * 100, 1),
    }


# ── Estimativas de mercados adicionais ───────────────────────────────────────

def estimate_corners(team: Dict[str, Any]) -> float:
    attack = team.get("attack_rating", 70)
    goals  = team.get("goals_scored_avg", 1.2)
    return round(3.5 + (attack / 100) * 4.5 + goals * 0.25, 1)


def estimate_cards(team: Dict[str, Any]) -> float:
    defense = team.get("defense_rating", 70)
    ranking = team.get("ranking", 50)
    base = 1.8 + (ranking / 120) * 1.0 - (defense / 100) * 0.6
    return round(max(0.6, min(3.2, base)), 1)


def estimate_saves(team: Dict[str, Any]) -> float:
    defense      = team.get("defense_rating", 70)
    goals_conc   = team.get("goals_conceded_avg", 1.2)
    # weaker defense = more shots faced = more saves
    return round(1.5 + goals_conc * 1.4 + (1 - defense / 100) * 2.5, 1)


# ── Função principal de tips ──────────────────────────────────────────────────

def get_betting_tips(match: Dict[str, Any], team1: Dict[str, Any], team2: Dict[str, Any]) -> List[Dict[str, Any]]:
    win_probs  = calculate_win_probabilities(team1, team2)
    goals_pred = predict_goals(team1, team2)
    form1      = analyze_form(team1)
    form2      = analyze_form(team2)
    trend1     = form_trend(team1)
    trend2     = form_trend(team2)
    style1     = infer_style(team1)
    style2     = infer_style(team2)
    form1_str  = form1
    formation1 = infer_formation(team1)
    formation2 = infer_formation(team2)
    matchup    = style_matchup(style1, style2)
    host1      = host_advantage_note(team1)
    recent1    = recent_results_summary(team1)
    recent2    = recent_results_summary(team2)
    elo1       = calculate_elo_score(team1)
    elo2       = calculate_elo_score(team2)
    elo_diff   = elo1 - elo2

    home_p = win_probs["home"]
    draw_p = win_probs["draw"]
    away_p = win_probs["away"]

    tips = []

    # ── 1X2 ──────────────────────────────────────────────────────────────────
    best_1x2 = max(
        [(home_p, "1", team1["name"]), (draw_p, "X", "Empate"), (away_p, "2", team2["name"])],
        key=lambda x: x[0]
    )
    conf_1x2  = round(best_1x2[0] * 100, 1)
    odds_1x2  = prob_to_odds(best_1x2[0])
    value_1x2 = calculate_value_bet(best_1x2[0], odds_1x2)

    reasoning_1x2 = (
        f"Estilo: {team1['name']} ({style1}, {formation1}) vs {team2['name']} ({style2}, {formation2}). "
        f"{matchup} "
        f"Forma: {team1['name']} {form1}/100 (tendência {trend1}) vs {team2['name']} {form2}/100 (tendência {trend2}). "
        f"Diferença ELO: {round(elo_diff, 1)}. "
        f"Probabilidades — Casa: {round(home_p*100,1)}%, Empate: {round(draw_p*100,1)}%, Fora: {round(away_p*100,1)}%. "
        f"{recent1}. "
        + (f"{host1}" if host1 else "")
    )

    tips.append({
        "market": "1X2",
        "recommendation": best_1x2[1],
        "description": f"{best_1x2[2]} para vencer" if best_1x2[1] != "X" else "Empate",
        "probability": best_1x2[0],
        "confidence": conf_1x2,
        "odds_estimate": odds_1x2,
        "reasoning": reasoning_1x2,
        "value": value_1x2,
    })

    # ── Mais/Menos 2.5 ───────────────────────────────────────────────────────
    over_p   = goals_pred["over_2_5_probability"]
    under_p  = 1 - over_p
    ou_rec   = "Mais de 2.5" if over_p >= under_p else "Menos de 2.5"
    ou_prob  = over_p if over_p >= under_p else under_p
    conf_ou  = round(ou_prob * 100, 1)
    odds_ou  = prob_to_odds(ou_prob)
    value_ou = calculate_value_bet(ou_prob, odds_ou)

    xg_total = round(goals_pred["home_expected_goals"] + goals_pred["away_expected_goals"], 2)
    reasoning_ou = (
        f"Gols esperados (xG): {team1['name']} {goals_pred['home_expected_goals']} + "
        f"{team2['name']} {goals_pred['away_expected_goals']} = {xg_total} no total. "
        f"Média de gols marcados: {team1['name']} {team1.get('goals_scored_avg', '?')}/jogo, "
        f"{team2['name']} {team2.get('goals_scored_avg', '?')}/jogo. "
        f"Média de gols sofridos: {team1['name']} {team1.get('goals_conceded_avg', '?')}, "
        f"{team2['name']} {team2.get('goals_conceded_avg', '?')}. "
        f"Probabilidade de mais de 2.5: {round(over_p*100,1)}%. "
        f"Contexto: {matchup}"
    )

    tips.append({
        "market": "Mais/Menos 2.5",
        "recommendation": ou_rec,
        "description": f"Total de gols: {ou_rec}",
        "probability": round(ou_prob, 4),
        "confidence": conf_ou,
        "odds_estimate": odds_ou,
        "reasoning": reasoning_ou,
        "value": value_ou,
    })

    # ── Ambas Marcam ─────────────────────────────────────────────────────────
    btts_p    = goals_pred["btts_probability"]
    no_btts_p = 1 - btts_p
    btts_rec  = "Sim" if btts_p >= no_btts_p else "Não"
    btts_prob = btts_p if btts_p >= no_btts_p else no_btts_p
    conf_btts  = round(btts_prob * 100, 1)
    odds_btts  = prob_to_odds(btts_prob)
    value_btts = calculate_value_bet(btts_prob, odds_btts)

    reasoning_btts = (
        f"Poder ofensivo: {team1['name']} marca em média {team1.get('goals_scored_avg','?')} gols/jogo "
        f"(estilo: {style1}), {team2['name']} marca {team2.get('goals_scored_avg','?')} gols/jogo "
        f"(estilo: {style2}). "
        f"Defesas: {team1['name']} sofre {team1.get('goals_conceded_avg','?')}, "
        f"{team2['name']} sofre {team2.get('goals_conceded_avg','?')} gols/jogo. "
        f"Probabilidade de ambas marcarem: {round(btts_p*100,1)}%. "
        f"{recent2}"
    )

    tips.append({
        "market": "Ambas Marcam",
        "recommendation": btts_rec,
        "description": f"Ambas as seleções marcam: {btts_rec}",
        "probability": round(btts_prob, 4),
        "confidence": conf_btts,
        "odds_estimate": odds_btts,
        "reasoning": reasoning_btts,
        "value": value_btts,
    })

    # ── Handicap Asiático ─────────────────────────────────────────────────────
    diff = elo_diff
    if abs(diff) < 5:
        handicap_val = 0
    elif diff > 0:
        handicap_val = -round(diff / 10 * 0.5, 1)
    else:
        handicap_val = round(abs(diff) / 10 * 0.5, 1)

    ah_prob = max(0.35, min(0.75, 0.5 + (diff / 200)))
    conf_ah  = round(ah_prob * 100, 1)
    odds_ah  = prob_to_odds(ah_prob)
    ah_team  = team1["name"] if diff >= 0 else team2["name"]
    ah_dir   = handicap_val if diff >= 0 else -handicap_val
    value_ah = calculate_value_bet(ah_prob, odds_ah)

    reasoning_ah = (
        f"Diferença ELO: {round(diff, 1)} em favor de {ah_team} (ranking #{team1['ranking'] if diff >= 0 else team2['ranking']}). "
        f"Formação provável: {formation1 if diff >= 0 else formation2}. "
        f"Forma recente ({trend1 if diff >= 0 else trend2}): "
        f"{recent1 if diff >= 0 else recent2}. "
        f"Handicap recomendado: {ah_dir:+.1f} gols. "
        + (f"{host1}" if host1 and diff >= 0 else "")
    )

    tips.append({
        "market": "Handicap Asiático",
        "recommendation": f"{ah_team} {ah_dir:+.1f}",
        "description": f"{ah_team} com handicap {ah_dir:+.1f}",
        "probability": round(ah_prob, 4),
        "confidence": conf_ah,
        "odds_estimate": odds_ah,
        "reasoning": reasoning_ah,
        "value": value_ah,
    })

    # ── Escanteios ────────────────────────────────────────────────────────────
    corners1 = estimate_corners(team1)
    corners2 = estimate_corners(team2)
    total_corners = corners1 + corners2
    # Linha dinâmica baseada na expectativa total
    corner_line = 9.5 if total_corners >= 9.0 else 8.5
    diff_c = total_corners - corner_line
    over_c_prob = max(0.30, min(0.72, 0.5 + diff_c * 0.045))
    under_c_prob = 1 - over_c_prob
    corner_rec  = f"Mais de {corner_line}" if over_c_prob >= under_c_prob else f"Menos de {corner_line}"
    corner_prob = over_c_prob if over_c_prob >= under_c_prob else under_c_prob
    conf_c  = round(corner_prob * 100, 1)
    odds_c  = prob_to_odds(corner_prob)
    value_c = calculate_value_bet(corner_prob, odds_c)

    reasoning_c = (
        f"Escanteios estimados: {team1['name']} ~{corners1} + {team2['name']} ~{corners2} = {total_corners:.1f} no total. "
        f"Times ofensivos e de alta pressão tendem a criar mais escanteios. "
        f"Estilo {team1['name']}: {style1} ({formation1}). "
        f"Estilo {team2['name']}: {style2} ({formation2}). "
        f"{matchup} Linha fixada em {corner_line}."
    )

    tips.append({
        "market": "Escanteios",
        "recommendation": corner_rec,
        "description": f"Total de escanteios: {corner_rec}",
        "probability": round(corner_prob, 4),
        "confidence": conf_c,
        "odds_estimate": odds_c,
        "reasoning": reasoning_c,
        "value": value_c,
    })

    # ── Cartões ───────────────────────────────────────────────────────────────
    cards1 = estimate_cards(team1)
    cards2 = estimate_cards(team2)
    total_cards = cards1 + cards2
    card_line = 3.5 if total_cards >= 3.2 else 2.5
    diff_k = total_cards - card_line
    over_k_prob = max(0.30, min(0.72, 0.5 + diff_k * 0.06))
    under_k_prob = 1 - over_k_prob
    card_rec  = f"Mais de {card_line}" if over_k_prob >= under_k_prob else f"Menos de {card_line}"
    card_prob = over_k_prob if over_k_prob >= under_k_prob else under_k_prob
    conf_k  = round(card_prob * 100, 1)
    odds_k  = prob_to_odds(card_prob)
    value_k = calculate_value_bet(card_prob, odds_k)

    intensity_note = "Disputas acirradas em fase de grupos costumam ter arbitragem rígida." \
        if abs(elo_diff) < 15 else \
        "Grande diferença de nível — favorito pode ter cartões por falta de motivação defensiva."

    reasoning_k = (
        f"Tendência de cartões: {team1['name']} ~{cards1} + {team2['name']} ~{cards2} = {total_cards:.1f} estimados. "
        f"Ranking e estilo de jogo influenciam a agressividade: "
        f"{team1['name']} (#{team1['ranking']}, {style1}), "
        f"{team2['name']} (#{team2['ranking']}, {style2}). "
        f"{intensity_note} Linha em {card_line}."
    )

    tips.append({
        "market": "Cartões",
        "recommendation": card_rec,
        "description": f"Total de cartões: {card_rec}",
        "probability": round(card_prob, 4),
        "confidence": conf_k,
        "odds_estimate": odds_k,
        "reasoning": reasoning_k,
        "value": value_k,
    })

    # ── Defesas do Goleiro ────────────────────────────────────────────────────
    # Defesas do goleiro de team1 = proporcional ao ataque de team2
    saves1 = round(estimate_saves(team1) * (team2.get("attack_rating", 70) / 70), 1)
    # Defesas do goleiro de team2 = proporcional ao ataque de team1
    saves2 = round(estimate_saves(team2) * (team1.get("attack_rating", 70) / 70), 1)
    total_saves = saves1 + saves2
    save_line = 5.5 if total_saves >= 5.0 else 4.5
    diff_s = total_saves - save_line
    over_s_prob = max(0.30, min(0.72, 0.5 + diff_s * 0.04))
    under_s_prob = 1 - over_s_prob
    save_rec  = f"Mais de {save_line}" if over_s_prob >= under_s_prob else f"Menos de {save_line}"
    save_prob = over_s_prob if over_s_prob >= under_s_prob else under_s_prob
    conf_s  = round(save_prob * 100, 1)
    odds_s  = prob_to_odds(save_prob)
    value_s = calculate_value_bet(save_prob, odds_s)

    reasoning_s = (
        f"Defesas estimadas: goleiro de {team1['name']} ~{saves1} (enfrenta ataque {team2['name']} "
        f"rated {team2.get('attack_rating','?')}/100) + "
        f"goleiro de {team2['name']} ~{saves2} (enfrenta ataque {team1['name']} "
        f"rated {team1.get('attack_rating','?')}/100) = {total_saves:.1f} no total. "
        f"Defesa {team1['name']}: {team1.get('defense_rating','?')}/100 (sofre {team1.get('goals_conceded_avg','?')} gols/jogo). "
        f"Defesa {team2['name']}: {team2.get('defense_rating','?')}/100 (sofre {team2.get('goals_conceded_avg','?')} gols/jogo). "
        f"Linha em {save_line}."
    )

    tips.append({
        "market": "Defesas do Goleiro",
        "recommendation": save_rec,
        "description": f"Total de defesas: {save_rec}",
        "probability": round(save_prob, 4),
        "confidence": conf_s,
        "odds_estimate": odds_s,
        "reasoning": reasoning_s,
        "value": value_s,
    })

    return tips
