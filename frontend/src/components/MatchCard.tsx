import { Link } from 'react-router-dom'
import { Match } from '../types'
import ConfidenceBar from './ConfidenceBar'
import clsx from 'clsx'

interface MatchCardProps {
  match: Match
}

export default function MatchCard({ match }: MatchCardProps) {
  const { home_team_data, away_team_data, win_probabilities, predicted_score, top_tip } = match

  const statusColor =
    match.status === 'live' ? 'bg-red-500 animate-pulse' :
    match.status === 'finished' ? 'bg-gray-500' :
    'bg-green-500'

  return (
    <Link to={`/matches/${match.id}`} className="block">
      <div className="bg-gray-800 rounded-xl border border-gray-700 hover:border-green-500/50 transition-all duration-200 hover:shadow-lg hover:shadow-green-500/10 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-2 bg-gray-700/50">
          <span className="text-xs text-gray-400 font-medium">Grupo {match.group}</span>
          <div className="flex items-center gap-2">
            <div className={clsx('w-2 h-2 rounded-full', statusColor)} />
            <span className="text-xs text-gray-400">{match.date} · {match.time}</span>
          </div>
        </div>

        {/* Teams */}
        <div className="px-4 py-4">
          <div className="flex items-center justify-between gap-2">
            {/* Home Team */}
            <div className="flex flex-col items-center gap-1 flex-1">
              <span className="text-4xl">{home_team_data?.flag || '🏳️'}</span>
              <span className="text-sm font-semibold text-white text-center leading-tight">{match.home_team}</span>
              {win_probabilities && (
                <span className="text-xs text-green-400 font-bold">{(win_probabilities.home * 100).toFixed(0)}%</span>
              )}
            </div>

            {/* Score/VS */}
            <div className="flex flex-col items-center gap-1">
              {predicted_score ? (
                <div className="text-center">
                  <div className="text-xl font-bold text-white">{predicted_score}</div>
                  <div className="text-xs text-gray-500">Previsto</div>
                </div>
              ) : (
                <span className="text-xl font-bold text-gray-400">VS</span>
              )}
              {win_probabilities && (
                <span className="text-xs text-gray-400">{(win_probabilities.draw * 100).toFixed(0)}% X</span>
              )}
            </div>

            {/* Away Team */}
            <div className="flex flex-col items-center gap-1 flex-1">
              <span className="text-4xl">{away_team_data?.flag || '🏳️'}</span>
              <span className="text-sm font-semibold text-white text-center leading-tight">{match.away_team}</span>
              {win_probabilities && (
                <span className="text-xs text-green-400 font-bold">{(win_probabilities.away * 100).toFixed(0)}%</span>
              )}
            </div>
          </div>
        </div>

        {/* Top Tip */}
        {top_tip && (
          <div className="px-4 pb-4">
            <div className="bg-gray-700/50 rounded-lg p-3">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs text-gray-400 font-medium">{top_tip.market}</span>
                <span className="text-xs font-bold text-white bg-gray-600 px-2 py-0.5 rounded">
                  @{top_tip.odds_estimate}
                </span>
              </div>
              <div className="text-sm font-semibold text-green-400 mb-2">{top_tip.description}</div>
              <ConfidenceBar confidence={top_tip.confidence} size="sm" />
            </div>
          </div>
        )}

        {/* Venue */}
        <div className="px-4 py-2 border-t border-gray-700/50">
          <span className="text-xs text-gray-500">{match.venue}</span>
        </div>
      </div>
    </Link>
  )
}
