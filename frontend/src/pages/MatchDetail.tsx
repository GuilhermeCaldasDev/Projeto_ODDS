import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { fetchMatch } from '../api/matches'
import { Match } from '../types'
import PredictionCard from '../components/PredictionCard'
import FormIndicator from '../components/FormIndicator'
import StatsChart from '../components/StatsChart'
import ConfidenceBar from '../components/ConfidenceBar'

export default function MatchDetail() {
  const { id } = useParams<{ id: string }>()
  const [match, setMatch] = useState<Match | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!id) return
    fetchMatch(Number(id))
      .then(setMatch)
      .finally(() => setLoading(false))
  }, [id])

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
            {gp ? (
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
