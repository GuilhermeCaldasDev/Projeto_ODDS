import { Link } from 'react-router-dom'
import { Match, LiveEvent } from '../types'
import ConfidenceBar from './ConfidenceBar'
import clsx from 'clsx'
import { etToBRT } from '../utils/time'

interface MatchCardProps {
  match: Match
}

function EventIcon({ type }: { type: LiveEvent['type'] }) {
  if (type === 'goal') return <span title="Gol">⚽</span>
  if (type === 'penalty') return <span title="Pênalti">⚽🥅</span>
  if (type === 'own_goal') return <span title="Gol Contra">⚽↩</span>
  if (type === 'yellow_card') return <span title="Cartão Amarelo">🟨</span>
  if (type === 'red_card') return <span title="Cartão Vermelho">🟥</span>
  return null
}

function StatBar({ label, home, away, highlight }: { label: string; home: number; away: number; highlight?: boolean }) {
  const total = home + away || 1
  const homePct = (home / total) * 100
  return (
    <div className="mb-2">
      <div className="flex items-center justify-between text-xs mb-1">
        <span className={clsx('font-semibold', highlight ? 'text-white' : 'text-gray-300')}>{home}</span>
        <span className="text-gray-500 text-[10px]">{label}</span>
        <span className={clsx('font-semibold', highlight ? 'text-white' : 'text-gray-300')}>{away}</span>
      </div>
      <div className="h-1 rounded-full bg-gray-700 overflow-hidden flex">
        <div className="bg-blue-400 h-full rounded-l-full" style={{ width: `${homePct}%` }} />
        <div className="bg-orange-400 h-full rounded-r-full flex-1" />
      </div>
    </div>
  )
}

export default function MatchCard({ match }: MatchCardProps) {
  const { home_team_data, away_team_data, win_probabilities, predicted_score, top_tip } = match
  const hasLiveData = (match.status === 'live' || match.status === 'finished') && match.live_stats

  const statusColor =
    match.status === 'live' ? 'bg-red-500 animate-pulse' :
    match.status === 'finished' ? 'bg-gray-500' :
    'bg-green-500'

  const statusLabel =
    match.status === 'live' ? 'Ao Vivo' :
    match.status === 'finished' ? 'Finalizado' :
    'A Começar'

  // Split events by team
  const homeEvents = match.live_events?.filter(e => e.team === 'home') ?? []
  const awayEvents = match.live_events?.filter(e => e.team === 'away') ?? []

  return (
    <Link to={`/matches/${match.id}`} className="block">
      <div className="bg-gray-800 rounded-xl border border-gray-700 hover:border-green-500/50 transition-all duration-200 hover:shadow-lg hover:shadow-green-500/10 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-2 bg-gray-700/50">
          <span className="text-xs text-gray-400 font-medium">Grupo {match.group}</span>
          <div className="flex items-center gap-2">
            <div className={clsx('w-2 h-2 rounded-full', statusColor)} />
            <span className={clsx(
              'text-xs font-medium',
              match.status === 'live' ? 'text-red-400' :
              match.status === 'finished' ? 'text-gray-500' :
              'text-green-400'
            )}>{statusLabel}</span>
            <span className="text-xs text-gray-500">{match.date} · {etToBRT(match.time)} <span className="text-gray-600">BRT</span></span>
          </div>
        </div>

        {/* Teams + Score */}
        <div className="px-4 py-4">
          <div className="flex items-center justify-between gap-2">
            {/* Home Team */}
            <div className="flex flex-col items-center gap-1 flex-1">
              <span className="text-4xl">{home_team_data?.flag || '🏳️'}</span>
              <span className="text-sm font-semibold text-white text-center leading-tight">{match.home_team}</span>
              {win_probabilities && (
                <span className="text-xs text-green-400 font-bold">{(win_probabilities.home * 100).toFixed(0)}%</span>
              )}
              {homeEvents.length > 0 && (
                <div className="flex flex-wrap justify-center gap-0.5 mt-1">
                  {homeEvents.map((e, i) => (
                    <span key={i} className="text-xs leading-none">{<EventIcon type={e.type} />} <span className="text-gray-500 text-[10px]">{e.minute}'</span></span>
                  ))}
                </div>
              )}
            </div>

            {/* Score/VS */}
            <div className="flex flex-col items-center gap-1">
              {(match.status === 'finished' || match.status === 'live') && match.home_score !== undefined ? (
                <div className="text-center">
                  <div className={clsx(
                    'text-2xl font-bold',
                    match.status === 'live' ? 'text-red-400' : 'text-white'
                  )}>
                    {match.home_score} – {match.away_score}
                  </div>
                  <div className="text-xs text-gray-500">
                    {match.status === 'finished' ? 'Final' : match.minute ? `${match.minute}'` : '● Ao Vivo'}
                  </div>
                </div>
              ) : match.status === 'upcoming' && predicted_score ? (
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
              {awayEvents.length > 0 && (
                <div className="flex flex-wrap justify-center gap-0.5 mt-1">
                  {awayEvents.map((e, i) => (
                    <span key={i} className="text-xs leading-none">{<EventIcon type={e.type} />} <span className="text-gray-500 text-[10px]">{e.minute}'</span></span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Live Stats */}
        {hasLiveData && match.live_stats && (
          <div className="px-4 pb-3 border-t border-gray-700/50 pt-3">
            <div className="text-[10px] text-gray-600 uppercase tracking-widest mb-2 text-center">Estatísticas</div>
            <StatBar label="Posse %" home={match.live_stats.home.possession} away={match.live_stats.away.possession} highlight />
            <StatBar label="Finalizações" home={match.live_stats.home.shots} away={match.live_stats.away.shots} />
            <StatBar label="No Gol" home={match.live_stats.home.shots_on_target} away={match.live_stats.away.shots_on_target} />
            <StatBar label="Escanteios" home={match.live_stats.home.corners} away={match.live_stats.away.corners} />
            <StatBar label="Faltas" home={match.live_stats.home.fouls} away={match.live_stats.away.fouls} />
          </div>
        )}

        {/* Top Tip — only for upcoming */}
        {top_tip && match.status === 'upcoming' && (
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
