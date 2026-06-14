from fastapi import APIRouter
from app.data.world_cup_data import TEAMS, MATCHES, KNOCKOUT_BRACKET, GROUPS, get_teams_by_group
from app.services.bracket import simulate_all_groups, get_third_place_qualifiers, simulate_ko_match

router = APIRouter()


@router.get("/bracket/predict")
def predict_bracket():
    # Step 1 — simulate all 12 groups (using real results for finished matches)
    teams_by_group = {g: get_teams_by_group(g) for g in GROUPS}
    group_results = simulate_all_groups(teams_by_group, MATCHES)

    # Step 2 — extract qualifiers
    qualifiers = {}  # slot -> team dict
    for group, standings in group_results.items():
        qualifiers[f"1{group}"] = next(t for t in TEAMS if t["name"] == standings[0]["name"])
        qualifiers[f"2{group}"] = next(t for t in TEAMS if t["name"] == standings[1]["name"])

    third_places = get_third_place_qualifiers(group_results, n=8)
    for i, t in enumerate(third_places):
        team_data = next(tt for tt in TEAMS if tt["name"] == t["name"])
        qualifiers[f"3rd_{i+1}"] = team_data

    # Step 3 — simulate Round of 32 (only the 12 fixed matchups)
    r32_results = []
    r32_winners = {}  # match_num -> team dict

    fixed_r32 = [m for m in KNOCKOUT_BRACKET["round_of_32"] if not m.get("wildcard")]
    for match in fixed_r32:
        t1 = qualifiers.get(match["slot1"])
        t2 = qualifiers.get(match["slot2"])
        if t1 and t2:
            result = simulate_ko_match(t1, t2)
            result["match"] = match["match"]
            result["date"] = match["date"]
            result["venue"] = match["venue"]
            result["slot1"] = match["slot1"]
            result["slot2"] = match["slot2"]
            r32_results.append(result)
            winner_name = result["predicted_winner"]
            r32_winners[match["match"]] = next(tt for tt in TEAMS if tt["name"] == winner_name)

    # Wildcard R32 — simulate best 3rd vs weakest group winners
    wildcard_r32 = [m for m in KNOCKOUT_BRACKET["round_of_32"] if m.get("wildcard")]
    sorted_group_winners = sorted(
        [{"slot": f"1{g}", "team": qualifiers[f"1{g}"]} for g in GROUPS],
        key=lambda x: x["team"]["ranking"]
    )
    for i, match in enumerate(wildcard_r32):
        third = qualifiers.get(f"3rd_{i+1}")
        opp_slot = sorted_group_winners[-(i + 1)] if i < len(sorted_group_winners) else None
        if third and opp_slot:
            opp = opp_slot["team"]
            result = simulate_ko_match(opp, third)
            result["match"] = match["match"]
            result["date"] = match["date"]
            result["venue"] = match["venue"]
            result["slot1"] = f"3rd_{i+1}"
            result["slot2"] = opp_slot["slot"]
            result["wildcard"] = True
            r32_results.append(result)
            winner_name = result["predicted_winner"]
            r32_winners[match["match"]] = next(tt for tt in TEAMS if tt["name"] == winner_name)

    r32_results.sort(key=lambda x: x["match"])

    # Step 4 — simulate Round of 16
    r16_results = []
    r16_winners = {}
    for match in KNOCKOUT_BRACKET["round_of_16"]:
        m1, m2 = match["feeds_from"]
        t1 = r32_winners.get(m1)
        t2 = r32_winners.get(m2)
        if t1 and t2:
            result = simulate_ko_match(t1, t2)
            result["match"] = match["match"]
            result["date"] = match["date"]
            result["venue"] = match["venue"]
            r16_results.append(result)
            winner_name = result["predicted_winner"]
            r16_winners[match["match"]] = next(tt for tt in TEAMS if tt["name"] == winner_name)

    # Step 5 — simulate Quarterfinals
    qf_results = []
    qf_winners = {}
    for match in KNOCKOUT_BRACKET["quarterfinals"]:
        m1, m2 = match["feeds_from"]
        t1 = r16_winners.get(m1)
        t2 = r16_winners.get(m2)
        if t1 and t2:
            result = simulate_ko_match(t1, t2)
            result["match"] = match["match"]
            result["date"] = match["date"]
            result["venue"] = match["venue"]
            qf_results.append(result)
            winner_name = result["predicted_winner"]
            qf_winners[match["match"]] = next(tt for tt in TEAMS if tt["name"] == winner_name)

    # Step 6 — simulate Semifinals
    sf_results = []
    sf_winners = {}
    sf_losers = {}
    for match in KNOCKOUT_BRACKET["semifinals"]:
        m1, m2 = match["feeds_from"]
        t1 = qf_winners.get(m1)
        t2 = qf_winners.get(m2)
        if t1 and t2:
            result = simulate_ko_match(t1, t2)
            result["match"] = match["match"]
            result["date"] = match["date"]
            result["venue"] = match["venue"]
            sf_results.append(result)
            winner_name = result["predicted_winner"]
            winner = next(tt for tt in TEAMS if tt["name"] == winner_name)
            loser_name = t2["name"] if winner_name == t1["name"] else t1["name"]
            loser = next(tt for tt in TEAMS if tt["name"] == loser_name)
            sf_winners[match["match"]] = winner
            sf_losers[match["match"]] = loser

    # Step 7 — Final
    sf_match_nums = [m["match"] for m in KNOCKOUT_BRACKET["semifinals"]]
    finalist1 = sf_winners.get(sf_match_nums[0]) if len(sf_match_nums) > 0 else None
    finalist2 = sf_winners.get(sf_match_nums[1]) if len(sf_match_nums) > 1 else None
    final_result = None
    champion = None
    if finalist1 and finalist2:
        final = KNOCKOUT_BRACKET["final"]
        final_result = simulate_ko_match(finalist1, finalist2)
        final_result["match"] = final["match"]
        final_result["date"] = final["date"]
        final_result["venue"] = final["venue"]
        champion_name = final_result["predicted_winner"]
        champion = next(tt for tt in TEAMS if tt["name"] == champion_name)

    return {
        "group_predictions": {
            g: [
                {
                    "position": s["predicted_position"],
                    "name": s["name"],
                    "flag": s["flag"],
                    "ranking": s["ranking"],
                    "predicted_pts": s["predicted_pts"],
                    "predicted_gd": s["predicted_gd"],
                    "attack_rating": s["attack_rating"],
                    "defense_rating": s["defense_rating"],
                    "form_score": s["form_score"],
                    "qualified": s["predicted_position"] <= 2,
                }
                for s in standings
            ]
            for g, standings in group_results.items()
        },
        "third_place_qualifiers": [
            {"name": t["name"], "flag": t["flag"], "group": t["group"], "predicted_pts": t["predicted_pts"]}
            for t in third_places
        ],
        "round_of_32": r32_results,
        "round_of_16": r16_results,
        "quarterfinals": qf_results,
        "semifinals": sf_results,
        "final": final_result,
        "predicted_champion": {
            "name": champion["name"],
            "flag": champion["flag"],
            "ranking": champion["ranking"],
            "attack_rating": champion["attack_rating"],
            "defense_rating": champion["defense_rating"],
        } if champion else None,
    }
