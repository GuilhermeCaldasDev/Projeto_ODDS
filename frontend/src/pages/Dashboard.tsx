import { useEffect, useState, useMemo } from 'react'
import { fetchTopPredictions } from '../api/predictions'
import { fetchMatches } from '../api/matches'
import { Prediction, Match } from '../types'
import PredictionCard from '../components/PredictionCard'
import MatchCard from '../components/MatchCard'
import clsx from 'clsx'
import { etToBRT } from '../utils/time'

export default function Dashboard() {
  const [topPredictions, setTopPredictions] = useState<Prediction[]>([])
  const [matches, setMatches] = useState<Match[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedMatch, setSelectedMatch] = useState<number | null>(null)

  useEffect(() => {
    Promise.all([fetchTopPredictions(), fetchMatches()])
      .then(([preds, matchData]) => {
        setTopPredictions(preds)
        setMatches(matchData.filter(m => m.status === 'live' || m.status === 'upcoming').slice(0, 6))
      })
      .catch(() => setError('Erro ao carregar dados. Verifique se o backend está em execução.'))
      .finally(() => setLoading(false))
  }, [])

  // Unique matches that appear in today's predictions, in kickoff order
  const matchOptions = useMemo(() => {
    const seen = new Map<number, Prediction>()
    topPredictions.forEach(p => {
      if (!seen.has(p.match_id)) seen.set(p.match_id, p)
    })
    return Array.from(seen.values()).sort((a, b) =>
      a.time.localeCompare(b.time)
    )
  }, [topPredictions])

  const visiblePredictions = useMemo(() =>
    selectedMatch === null
      ? topPredictions
      : topPredictions.filter(p => p.match_id === selectedMatch),
    [topPredictions, selectedMatch]
  )

  if (loading) return (
    <div className="flex items-center justify-center min-h-96">
      <div className="text-center">
        <div className="text-4xl mb-4 animate-bounce">⚽</div>
        <div className="text-gray-400">Carregando análises...</div>
      </div>
    </div>
  )

  if (error) return (
    <div className="flex items-center justify-center min-h-96">
      <div className="text-center bg-red-500/10 border border-red-500/30 rounded-xl p-8">
        <div className="text-4xl mb-4">⚠️</div>
        <div className="text-red-400 font-medium mb-2">Erro de Conexão</div>
        <div className="text-gray-400 text-sm">{error}</div>
        <div className="mt-4 text-xs text-gray-500">
          Execute: <code className="bg-gray-800 px-2 py-1 rounded">uvicorn app.main:app --reload</code>
        </div>
      </div>
    </div>
  )

  const avgConfidence = topPredictions.length > 0
    ? (topPredictions.reduce((a, p) => a + p.confidence, 0) / topPredictions.length).toFixed(1)
    : '0'

  return (
    <div>
      {/* Hero */}
      <div className="mb-8 text-center py-8">
        <div className="text-5xl mb-4">🏆</div>
        <h1 className="text-3xl font-bold text-white mb-2">Copa do Mundo 2026</h1>
        <p className="text-gray-400 text-lg">Análise Estatística de Apostas</p>
        <p className="text-gray-500 text-sm mt-2">Previsões baseadas em ELO, Poisson e forma recente</p>
      </div>

      {/* Stats Bar */}
      <div className="grid grid-cols-3 gap-4 mb-10">
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-4 text-center">
          <div className="text-2xl font-bold text-green-400">72</div>
          <div className="text-xs text-gray-400 mt-1">Jogos Analisados</div>
        </div>
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-4 text-center">
          <div className="text-2xl font-bold text-blue-400">{avgConfidence}%</div>
          <div className="text-xs text-gray-400 mt-1">Confiança Média</div>
        </div>
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-4 text-center">
          <div className="text-2xl font-bold text-purple-400">48</div>
          <div className="text-xs text-gray-400 mt-1">Seleções</div>
        </div>
      </div>

      {/* Top Predictions */}
      <section className="mb-10">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-xl">🎯</span>
          <h2 className="text-xl font-bold text-white">Melhores Apostas do Dia</h2>
          <span className="ml-auto text-xs text-gray-500 bg-gray-800 border border-gray-700 px-2 py-1 rounded">
            {visiblePredictions.length} apostas
          </span>
        </div>

        {/* Match filter */}
        {matchOptions.length > 1 && (
          <div className="flex flex-wrap gap-2 mb-5">
            <button
              onClick={() => setSelectedMatch(null)}
              className={clsx(
                'px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
                selectedMatch === null
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-800 text-gray-400 border border-gray-700 hover:bg-gray-700 hover:text-white'
              )}
            >
              Todos os jogos
            </button>
            {matchOptions.map(p => (
              <button
                key={p.match_id}
                onClick={() => setSelectedMatch(p.match_id)}
                className={clsx(
                  'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
                  selectedMatch === p.match_id
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-800 text-gray-400 border border-gray-700 hover:bg-gray-700 hover:text-white'
                )}
              >
                <span>{p.home_flag}</span>
                <span>{p.home_team}</span>
                <span className="text-gray-500">x</span>
                <span>{p.away_team}</span>
                <span>{p.away_flag}</span>
                <span className={clsx(
                  'ml-1 font-semibold',
                  selectedMatch === p.match_id ? 'text-white' : 'text-green-400'
                )}>
                  {etToBRT(p.time)}
                </span>
              </button>
            ))}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {visiblePredictions.map((pred, i) => (
            <PredictionCard
              key={i}
              prediction={pred}
              matchInfo={{
                home_team: pred.home_team,
                home_flag: pred.home_flag,
                away_team: pred.away_team,
                away_flag: pred.away_flag,
                date: pred.date,
                time: pred.time,
                match_id: pred.match_id,
              }}
            />
          ))}
        </div>
      </section>

      {/* Upcoming Matches */}
      <section>
        <div className="flex items-center gap-3 mb-4">
          <span className="text-xl">{matches.some(m => m.status === 'live') ? '🔴' : '📅'}</span>
          <h2 className="text-xl font-bold text-white">
            {matches.some(m => m.status === 'live') ? 'Ao Vivo & Próximos Jogos' : 'Próximos Jogos'}
          </h2>
          <a href="/matches" className="ml-auto text-xs text-green-400 hover:text-green-300">
            Ver todos →
          </a>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {matches.map((match) => (
            <MatchCard key={match.id} match={match} />
          ))}
        </div>
      </section>
    </div>
  )
}
