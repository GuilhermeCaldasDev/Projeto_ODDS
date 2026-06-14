import { Prediction, BettingTip } from '../types'
import ConfidenceBar from './ConfidenceBar'
import clsx from 'clsx'
import { etToBRT } from '../utils/time'

interface PredictionCardProps {
  prediction: Prediction | BettingTip
  matchInfo?: {
    home_team: string
    home_flag: string
    away_team: string
    away_flag: string
    date: string
    time?: string
    match_id: number
  }
  compact?: boolean
}

const BOOKMAKER_LOGOS: Record<string, string> = {
  bet365: '365',
  pinnacle: 'PIN',
  betfair: 'BF',
  betfair_ex_eu: 'BF',
  unibet: 'UNI',
  williamhill: 'WH',
  bwin: 'BW',
  betway: 'BTW',
  '1xbet': '1XB',
  draftkings: 'DK',
  fanduel: 'FD',
}

export default function PredictionCard({ prediction, matchInfo, compact = false }: PredictionCardProps) {
  const marketColors: Record<string, string> = {
    '1X2':                 'text-blue-400   bg-blue-500/10   border-blue-500/30',
    'Over/Under 2.5':      'text-purple-400 bg-purple-500/10 border-purple-500/30',
    'Mais/Menos 2.5':      'text-purple-400 bg-purple-500/10 border-purple-500/30',
    'BTTS':                'text-orange-400 bg-orange-500/10 border-orange-500/30',
    'Ambas Marcam':        'text-orange-400 bg-orange-500/10 border-orange-500/30',
    'Asian Handicap':      'text-cyan-400   bg-cyan-500/10   border-cyan-500/30',
    'Handicap Asiático':   'text-cyan-400   bg-cyan-500/10   border-cyan-500/30',
    'Escanteios':          'text-yellow-400 bg-yellow-500/10 border-yellow-500/30',
    'Cartões':             'text-red-400    bg-red-500/10    border-red-500/30',
    'Defesas do Goleiro':  'text-green-400  bg-green-500/10  border-green-500/30',
  }

  const marketColor = marketColors[prediction.market] || 'text-gray-400 bg-gray-500/10 border-gray-500/30'

  const confColor =
    prediction.confidence >= 70 ? 'text-green-400' :
    prediction.confidence >= 50 ? 'text-yellow-400' :
    'text-red-400'

  const hasRealOdds = prediction.real_odds?.price != null
  const realValue   = prediction.real_value
  const bookTag     = hasRealOdds
    ? (BOOKMAKER_LOGOS[prediction.real_odds!.bookmaker_key] ?? prediction.real_odds!.bookmaker.slice(0, 4).toUpperCase())
    : null

  // Use real value if available, fall back to model value
  const displayValue = realValue ?? prediction.value
  const isValue = displayValue?.has_value

  return (
    <div className={clsx(
      'bg-gray-800 rounded-xl border overflow-hidden transition-all duration-200',
      isValue ? 'border-green-600/50 hover:border-green-500' : 'border-gray-700 hover:border-gray-600',
      compact ? 'p-3' : 'p-4'
    )}>

      {/* Match Info */}
      {matchInfo && (
        <div className="flex items-center gap-2 mb-3 pb-3 border-b border-gray-700">
          <span className="text-lg">{matchInfo.home_flag}</span>
          <span className="text-sm font-medium text-white truncate">{matchInfo.home_team}</span>
          <span className="text-gray-500 text-xs shrink-0">×</span>
          <span className="text-sm font-medium text-white truncate">{matchInfo.away_team}</span>
          <span className="text-lg">{matchInfo.away_flag}</span>
          <div className="ml-auto shrink-0 text-right">
            {matchInfo.time && (
              <div className="text-xs font-semibold text-green-400">
                {etToBRT(matchInfo.time)} <span className="text-gray-600">BRT</span>
              </div>
            )}
            <div className="text-xs text-gray-500">{matchInfo.date}</div>
          </div>
        </div>
      )}

      {/* Market badge + value badge */}
      <div className="flex items-center justify-between mb-3">
        <span className={clsx('text-xs font-bold px-2 py-1 rounded border', marketColor)}>
          {prediction.market}
        </span>
        <div className="flex items-center gap-1.5">
          {isValue && (
            <span className="text-xs bg-green-500/20 text-green-400 border border-green-500/40 px-2 py-0.5 rounded font-bold">
              VALOR +{displayValue!.value_percentage.toFixed(1)}%
            </span>
          )}
        </div>
      </div>

      {/* Recommendation */}
      <div className={clsx('text-base font-bold mb-3', confColor)}>
        {prediction.description}
      </div>

      {/* Odds comparison */}
      <div className={clsx(
        'rounded-lg mb-3 overflow-hidden border',
        hasRealOdds ? 'border-gray-600' : 'border-gray-700'
      )}>
        {hasRealOdds ? (
          /* Two-column: real odds vs model */
          <div className="grid grid-cols-2 divide-x divide-gray-700">
            <div className="px-3 py-2 text-center">
              <div className="text-xs text-gray-500 mb-1">Modelo</div>
              <div className="text-sm font-bold text-gray-400">@{prediction.odds_estimate}</div>
            </div>
            <div className="px-3 py-2 text-center bg-green-900/20">
              <div className="flex items-center justify-center gap-1 mb-1">
                <div className="text-xs text-green-400">Melhor casa</div>
                <span className="text-xs bg-gray-700 text-gray-300 px-1 rounded font-mono">
                  {bookTag}
                </span>
              </div>
              <div className="text-base font-bold text-white">
                @{prediction.real_odds!.price.toFixed(2)}
              </div>
            </div>
          </div>
        ) : (
          /* Single: model-only */
          <div className="px-3 py-2 flex items-center justify-between">
            <span className="text-xs text-gray-500">Odds estimadas (modelo)</span>
            <span className="text-sm font-bold text-white">@{prediction.odds_estimate}</span>
          </div>
        )}
      </div>

      {/* Probability + edge */}
      <div className="text-xs text-gray-400 mb-3 flex flex-wrap gap-x-3 gap-y-1">
        <span>
          Prob: <span className="text-white font-medium">{(prediction.probability * 100).toFixed(1)}%</span>
        </span>
        {hasRealOdds && displayValue && (
          <span className={displayValue.edge > 0 ? 'text-green-400' : 'text-red-400'}>
            Edge: {displayValue.edge > 0 ? '+' : ''}{displayValue.edge.toFixed(1)}%
          </span>
        )}
        {hasRealOdds && (prediction.bookmakers_available ?? 0) > 0 && (
          <span className="text-gray-600">
            {prediction.bookmakers_available} casa{prediction.bookmakers_available !== 1 ? 's' : ''}
          </span>
        )}
      </div>

      {/* Confidence bar */}
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
