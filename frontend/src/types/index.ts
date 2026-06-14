export interface RecentResult {
  opponent: string
  result: 'W' | 'D' | 'L'
  score: string
}

export interface TournamentStats {
  group: string
  played: number
  wins: number
  draws: number
  losses: number
  goals_for: number
  goals_against: number
  goal_diff: number
  points: number
  shots: number
  shots_on_target: number
  corners: number
  fouls: number
  yellow_cards: number
  red_cards: number
}

export interface Team {
  name: string
  flag: string
  group: string
  confederation: string
  ranking: number
  attack_rating: number
  defense_rating: number
  form: ('W' | 'D' | 'L')[]
  goals_scored_avg: number
  goals_conceded_avg: number
  key_players: string[]
  recent_results: RecentResult[]
  form_score?: number
  tournament_stats?: TournamentStats
}

export interface WinProbabilities {
  home: number
  draw: number
  away: number
}

export interface GoalsPrediction {
  home_expected_goals: number
  away_expected_goals: number
  predicted_score: string
  over_2_5_probability: number
  btts_probability: number
  top_scores: [string, number][]
  home_win_prob: number
  draw_prob: number
  away_win_prob: number
}

export interface ValueBet {
  has_value: boolean
  value_percentage: number
  edge: number
}

export interface RealOdds {
  price: number
  bookmaker: string
  bookmaker_key: string
}

export interface RealValue {
  has_value: boolean
  value_percentage: number
  edge: number
}

export interface BettingTip {
  market: string
  recommendation: string
  description: string
  probability: number
  confidence: number
  odds_estimate: number
  reasoning: string
  value: ValueBet
  real_odds?: RealOdds | null
  real_value?: RealValue | null
  bookmakers_available?: number
}

export interface LiveTeamStats {
  corners: number
  shots: number
  shots_on_target: number
  fouls: number
  possession: number
}

export interface LiveStats {
  home: LiveTeamStats
  away: LiveTeamStats
}

export interface LiveEvent {
  type: 'goal' | 'penalty' | 'own_goal' | 'yellow_card' | 'red_card'
  minute: string
  team: 'home' | 'away'
  player: string
}

export interface Match {
  id: number
  home_team: string
  away_team: string
  group: string
  date: string
  time: string
  venue: string
  status: 'upcoming' | 'live' | 'finished'
  home_score?: number
  away_score?: number
  minute?: string
  live_stats?: LiveStats
  live_events?: LiveEvent[]
  home_team_data?: Team
  away_team_data?: Team
  win_probabilities?: WinProbabilities
  predicted_score?: string
  top_tip?: BettingTip
  goals_prediction?: GoalsPrediction
  betting_tips?: BettingTip[]
  home_form_score?: number
  away_form_score?: number
}

export interface Prediction extends BettingTip {
  match_id: number
  home_team: string
  home_flag: string
  away_team: string
  away_flag: string
  date: string
  time: string
  venue: string
  group: string
  predicted_score: string
  win_probabilities: WinProbabilities
}

export interface GroupStanding {
  team: string
  flag: string
  ranking: number
  played: number
  won: number
  drawn: number
  lost: number
  goals_for: number
  goals_against: number
  goal_diff: number
  points: number
  form_score: number
}
