import { useEffect, useState, useCallback } from 'react'
import { useParams, Link } from 'react-router-dom'
import { fetchMatch } from '../api/matches'
import { Match, LiveEvent } from '../types'
import PredictionCard from '../components/PredictionCard'
import FormIndicator from '../components/FormIndicator'
import StatsChart from '../components/StatsChart'
import ConfidenceBar from '../components/ConfidenceBar'
import clsx from 'clsx'

function EventIcon({ type }: { type: LiveEvent['type'] }) {
  if (type === 'goal') return <span>⚽</span>
  if (type === 'penalty') return <span title="Pênalti">⚽</span>
  if (type === 'own_goal') return <span title="Gol Contra">↩⚽</span>
  if (type === 'yellow_card') return <span>🟨</span>
  if (type === 'red_card') return <span>🟥</span>
  return null
}

function eventLabel(type: LiveEvent['type']): string {
  if (type === 'goal') return 'Gol'
  if (type === 'penalty') return 'Pênalti (Gol)'
  if (type === 'own_goal') return 'Gol Contra'
  if (type === 'yellow_card') return 'Cartão Amarelo'
  if (type === 'red_card') return 'Cartão Vermelho'
  return type
}

function StatRow({ label, home, away }: { label: string; home: number | string; away: number | string }) {
  const h = typeof home === 'string' ? parseFloat(home) : home
  const a = typeof away === 'string' ? parseFloat(away) : away
  const total = h + a || 1
  const homePct = (h / total) * 100
  return (
    <div className="mb-3">
      <div className="flex items-center justify-between text-sm mb-1">
        <span className="font-bold text-white w-12 text-right">{home}</span>
        <span className="text-gray-400 text-xs flex-1 text-center">{label}</span>
        <span className="font-bold text-white w-12">{away}</span>
      </div>
      <div className="h-2 rounded-full bg-gray-700 overflow-hidden flex">
        <div className="bg-blue-400 h-full transition-all duration-500" style={{ width: `${homePct}%` }} />
        <div className="bg-orange-400 h-full flex-1" />
      </div>
    </div>
  )
}

export default function MatchDetail() {
  const { id } = useParams<{ id: string }>()
  const [match, setMatch] = useState<Match | null>(null)
  const [loading, setLoading] = useState(true)

  const load = useCallback(() => {
    if (!id) return
    fetchMatch(Number(id))
      .then(setMatch)
      .finally(() => setLoading(false))
  }, [id])

  useEffect(() => { load() }, [load])

  // Auto-refresh when live
  useEffect(() => {
    if (!match || match.status !== 'live') return
    const t = setInterval(load, 30_000)
    return () => clearInterval(t)
  }, [match?.status, load])

  if (loading) return (
    <div className="flex items-center justify-center min-h-96">
      <div className="text-center">
        <div className="text-4xl mb-4 animate-bounce">⚽</div>
        <div className="text-gray-400">Analisando partida...</div>
      </div>
    </div>
  )

  if (!match) return (
    <div className="text-center py-20">
      <div className="text-4xl mb-4">❌</div>
      <div className="text-gray-400">Jogo não encontrado</div>
      <Link to="/matches" className="text-green-400 text-sm mt-2 block">← Voltar aos jogos</Link>
    </div>
  )

  const { home_team_data: ht, away_team_data: at, win_probabilities: wp, goals_prediction: gp, betting_tips: tips } = match

  return (
    <div>
      <Link to="/matches" className="text-green-400 text-sm mb-6 block hover:text-green-300">← Voltar aos jogos</Link>

      {/* Match Header */}
      <div className="bg-gray-800 rounded-2xl border border-gray-700 p-6 mb-6">
        <div className="text-center text-xs text-gray-400 mb-4">
          Grupo {match.group} · {match.date} {match.time} · {match.venue}
        </div>
        <div className="flex items-center justify-around gap-4">
          <div className="flex flex-col items-center gap-2 flex-1">
            <span className="text-6xl">{ht?.flag || '🏳️'}</span>
            <div className="text-xl font-bold text-white">{match.home_team}</div>
            {ht && <div className="text-xs text-gray-400">#{ht.ranking} FIFA</div>}
            {wp && <div className="text-2xl font-bold text-green-400">{(wp.home * 100).toFixed(0)}%</div>}
          </div>

          <div className="flex flex-col items-center gap-2">
            {(match.status === 'live' || match.status === 'finished') && match.home_score !== undefined ? (
              <div className="text-center">
                <div className={clsx('text-4xl font-bold', match.status === 'live' ? 'text-red-400' : 'text-white')}>
                  {match.home_score} – {match.away_score}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {match.status === 'finished' ? 'Final' : match.minute ? `${match.minute}'` : '● Ao Vivo'}
                </div>
                {wp && <div className="text-sm text-gray-400 mt-2">{(wp.draw * 100).toFixed(0)}% Empate</div>}
              </div>
            ) : gp ? (
              <div className="text-center">
                <div className="text-3xl font-bold text-white">{gp.predicted_score}</div>
                <div className="text-xs text-gray-500 mt-1">Placar Previsto</div>
                {wp && <div className="text-sm text-gray-400 mt-2">{(wp.draw * 100).toFixed(0)}% Empate</div>}
              </div>
            ) : (
              <span className="text-3xl font-bold text-gray-400">VS</span>
            )}
          </div>

          <div className="flex flex-col items-center gap-2 flex-1">
            <span className="text-6xl">{at?.flag || '🏳️'}</span>
            <div className="text-xl font-bold text-white">{match.away_team}</div>
            {at && <div className="text-xs text-gray-400">#{at.ranking} FIFA</div>}
            {wp && <div className="text-2xl font-bold text-green-400">{(wp.away * 100).toFixed(0)}%</div>}
          </div>
        </div>
      </div>

      {/* Live Stats + Events */}
      {match.live_stats && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Stats */}
          <div className="bg-gray-800 rounded-xl border border-gray-700 p-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-gray-400">Estatísticas do Jogo</h3>
              {match.status === 'live' && (
                <span className="flex items-center gap-1 text-xs text-red-400">
                  <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />Ao Vivo
                </span>
              )}
            </div>
            {/* Team headers */}
            <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-400 inline-block" />{match.home_team}</span>
              <span className="flex items-center gap-1">{match.away_team}<span className="w-2 h-2 rounded-full bg-orange-400 inline-block" /></span>
            </div>
            <StatRow label="Posse de Bola %" home={`${match.live_stats.home.possession}%`} away={`${match.live_stats.away.possession}%`} />
            <StatRow label="Finalizações" home={match.live_stats.home.shots} away={match.live_stats.away.shots} />
            <StatRow label="No Gol" home={match.live_stats.home.shots_on_target} away={match.live_stats.away.shots_on_target} />
            <StatRow label="Escanteios" home={match.live_stats.home.corners} away={match.live_stats.away.corners} />
            <StatRow label="Faltas" home={match.live_stats.home.fouls} away={match.live_stats.away.fouls} />
          </div>

          {/* Events timeline */}
          {match.live_events && match.live_events.length > 0 && (
            <div className="bg-gray-800 rounded-xl border border-gray-700 p-4">
              <h3 className="text-sm font-semibold text-gray-400 mb-4">Eventos da Partida</h3>
              <div className="space-y-2">
                {match.live_events.map((ev, i) => (
                  <div key={i} className={clsx(
                    'flex items-center gap-3 text-sm',
                    ev.team === 'away' ? 'flex-row-reverse' : ''
                  )}>
                    <span className="text-xs text-gray-500 w-10 shrink-0 text-center">{ev.minute}'</span>
                    <span className="text-base"><EventIcon type={ev.type} /></span>
                    <div className={clsx('flex-1', ev.team === 'away' ? 'text-right' : '')}>
                      <span className="text-white font-medium text-xs">{ev.player}</span>
                      <span className="text-gray-500 text-xs ml-1">({eventLabel(ev.type)})</span>
                    </div>
                    <span className="text-[10px] text-gray-600 shrink-0">
                      {ev.team === 'home' ? match.home_team : match.away_team}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Stats Chart */}
        {ht && at && <StatsChart team1={ht} team2={at} />}

        {/* Goals Prediction */}
        {gp && (
          <div className="bg-gray-800 rounded-xl border border-gray-700 p-4">
            <h3 className="text-sm font-semibold text-gray-400 mb-4">Previsão de Gols (Poisson)</h3>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-white">{gp.home_expected_goals}</div>
                <div className="text-xs text-gray-400 mt-1">Gols esperados ({match.home_team})</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white">{gp.away_expected_goals}</div>
                <div className="text-xs text-gray-400 mt-1">Gols esperados ({match.away_team})</div>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">Over 2.5 Gols</span>
                <span className="text-xs font-bold text-white">{(gp.over_2_5_probability * 100).toFixed(1)}%</span>
              </div>
              <ConfidenceBar confidence={gp.over_2_5_probability * 100} showLabel={false} />
              <div className="flex items-center justify-between mt-2">
                <span className="text-xs text-gray-400">Ambas Marcam (BTTS)</span>
                <span className="text-xs font-bold text-white">{(gp.btts_probability * 100).toFixed(1)}%</span>
              </div>
              <ConfidenceBar confidence={gp.btts_probability * 100} showLabel={false} />
            </div>
            {gp.top_scores && (
              <div className="mt-4">
                <div className="text-xs text-gray-400 mb-2">Placares mais prováveis</div>
                <div className="flex flex-wrap gap-2">
                  {gp.top_scores.map(([score, prob]) => (
                    <span key={score} className="bg-gray-700 text-white text-xs px-3 py-1 rounded-lg font-bold">
                      {score} <span className="text-gray-400 font-normal">{(prob * 100).toFixed(1)}%</span>
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Form Comparison */}
      {ht && at && (
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-4 mb-6">
          <h3 className="text-sm font-semibold text-gray-400 mb-4">Forma Recente</h3>
          <div className="grid grid-cols-2 gap-6">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <span>{ht.flag}</span>
                <span className="text-sm font-medium text-white">{ht.name}</span>
                {match.home_form_score !== undefined && (
                  <span className="ml-auto text-xs text-green-400 font-bold">{match.home_form_score}/100</span>
                )}
              </div>
              <FormIndicator form={ht.form} size="md" />
              <div className="mt-3 space-y-1">
                {ht.recent_results?.map((r, i) => (
                  <div key={i} className="flex items-center gap-2 text-xs">
                    <span className={`w-5 h-5 rounded-full flex items-center justify-center font-bold text-xs ${r.result === 'W' ? 'bg-green-500' : r.result === 'D' ? 'bg-yellow-500 text-gray-900' : 'bg-red-500'} text-white`}>
                      {r.result}
                    </span>
                    <span className="text-gray-400">vs {r.opponent}</span>
                    <span className="text-gray-300 ml-auto">{r.score}</span>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2 mb-3">
                <span>{at.flag}</span>
                <span className="text-sm font-medium text-white">{at.name}</span>
                {match.away_form_score !== undefined && (
                  <span className="ml-auto text-xs text-green-400 font-bold">{match.away_form_score}/100</span>
                )}
              </div>
              <FormIndicator form={at.form} size="md" />
              <div className="mt-3 space-y-1">
                {at.recent_results?.map((r, i) => (
                  <div key={i} className="flex items-center gap-2 text-xs">
                    <span className={`w-5 h-5 rounded-full flex items-center justify-center font-bold text-xs ${r.result === 'W' ? 'bg-green-500' : r.result === 'D' ? 'bg-yellow-500 text-gray-900' : 'bg-red-500'} text-white`}>
                      {r.result}
                    </span>
                    <span className="text-gray-400">vs {r.opponent}</span>
                    <span className="text-gray-300 ml-auto">{r.score}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Betting Tips */}
      {tips && tips.length > 0 && (
        <section>
          <h2 className="text-lg font-bold text-white mb-4">Análise de Apostas</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {tips.map((tip, i) => (
              <PredictionCard key={i} prediction={tip} />
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
