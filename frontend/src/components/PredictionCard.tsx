import { Prediction, BettingTip } from '../types'
import ConfidenceBar from './ConfidenceBar'
import clsx from 'clsx'

interface PredictionCardProps {
  prediction: Prediction | BettingTip
  matchInfo?: {
    home_team: string
    home_flag: string
    away_team: string
    away_flag: string
    date: string
    match_id: number
  }
  compact?: boolean
}

export default function PredictionCard({ prediction, matchInfo, compact = false }: PredictionCardProps) {
  const marketColors: Record<string, string> = {
    '1X2': 'text-blue-400 bg-blue-500/10 border-blue-500/30',
    'Over/Under 2.5': 'text-purple-400 bg-purple-500/10 border-purple-500/30',
    'BTTS': 'text-orange-400 bg-orange-500/10 border-orange-500/30',
    'Asian Handicap': 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30',
  }

  const marketColor = marketColors[prediction.market] || 'text-gray-400 bg-gray-500/10 border-gray-500/30'
  const confColor =
    prediction.confidence >= 70 ? 'text-green-400' :
    prediction.confidence >= 50 ? 'text-yellow-400' :
    'text-red-400'

  return (
    <div className={clsx(
      'bg-gray-800 rounded-xl border border-gray-700 overflow-hidden',
      'hover:border-gray-600 transition-all duration-200',
      compact ? 'p-3' : 'p-4'
    )}>
      {/* Match Info */}
      {matchInfo && (
        <div className="flex items-center gap-2 mb-3 pb-3 border-b border-gray-700">
          <span className="text-lg">{matchInfo.home_flag}</span>
          <span className="text-sm font-medium text-white">{matchInfo.home_team}</span>
          <span className="text-gray-500 text-xs">vs</span>
          <span className="text-sm font-medium text-white">{matchInfo.away_team}</span>
          <span className="text-lg">{matchInfo.away_flag}</span>
          <span className="ml-auto text-xs text-gray-500">{matchInfo.date}</span>
        </div>
      )}

      {/* Market Badge + Odds */}
      <div className="flex items-center justify-between mb-2">
        <span className={clsx('text-xs font-bold px-2 py-1 rounded border', marketColor)}>
          {prediction.market}
        </span>
        <div className="flex items-center gap-2">
          {prediction.value.has_value && (
            <span className="text-xs bg-green-500/20 text-green-400 border border-green-500/30 px-2 py-0.5 rounded font-bold">
              VALUE BET
            </span>
          )}
          <span className="text-sm font-bold text-white bg-gray-700 px-3 py-1 rounded-lg">
            @{prediction.odds_estimate}
          </span>
        </div>
      </div>

      {/* Recommendation */}
      <div className={clsx('text-lg font-bold mb-1', confColor)}>
        {prediction.description}
      </div>

      {/* Probability */}
      <div className="text-xs text-gray-400 mb-3">
        Probabilidade: <span className="text-white font-medium">{(prediction.probability * 100).toFixed(1)}%</span>
        {prediction.value.has_value && (
          <span className="ml-2 text-green-400">
            · Edge: +{prediction.value.edge.toFixed(1)}%
          </span>
        )}
      </div>

      {/* Confidence Bar */}
      <ConfidenceBar confidence={prediction.confidence} size="sm" />

      {/* Reasoning */}
      {!compact && (
        <div className="mt-3 pt-3 border-t border-gray-700">
          <p className="text-xs text-gray-400 leading-relaxed">{prediction.reasoning}</p>
        </div>
      )}
    </div>
  )
}
