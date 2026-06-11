import client from './client'

export interface GroupTeamPrediction {
  position: number
  name: string
  flag: string
  ranking: number
  predicted_pts: number
  predicted_gd: number
  attack_rating: number
  defense_rating: number
  form_score: number
  qualified: boolean
}

export interface KOMatch {
  match: number
  home: string
  home_flag: string
  away: string
  away_flag: string
  home_win_prob: number
  away_win_prob: number
  predicted_winner: string
  predicted_winner_flag: string
  predicted_score: string
  home_xg: number
  away_xg: number
  date: string
  venue: string
  slot1?: string
  slot2?: string
  wildcard?: boolean
}

export interface BracketPrediction {
  group_predictions: Record<string, GroupTeamPrediction[]>
  third_place_qualifiers: { name: string; flag: string; group: string; predicted_pts: number }[]
  round_of_32: KOMatch[]
  round_of_16: KOMatch[]
  quarterfinals: KOMatch[]
  semifinals: KOMatch[]
  final: KOMatch | null
  predicted_champion: { name: string; flag: string; ranking: number; attack_rating: number; defense_rating: number } | null
}

export const fetchBracketPrediction = async (): Promise<BracketPrediction> => {
  const res = await client.get('/api/bracket/predict')
  return res.data
}
