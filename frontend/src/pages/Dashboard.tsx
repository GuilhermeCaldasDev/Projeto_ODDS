import { useEffect, useState } from 'react'
import { fetchTopPredictions } from '../api/predictions'
import { fetchMatches } from '../api/matches'
import { Prediction, Match } from '../types'
import PredictionCard from '../components/PredictionCard'
import MatchCard from '../components/MatchCard'

export default function Dashboard() {
  const [topPredictions, setTopPredictions] = useState<Prediction[]>([])
  const [matches, setMatches] = useState<Match[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([fetchTopPredictions(), fetchMatches()])
      .then(([preds, matchData]) => {
        setTopPredictions(preds)
        setMatches(matchData.slice(0, 6))
      })
      .catch(() => setError('Erro ao carregar dados. Verifique se o backend está em execução.'))
      .finally(() => setLoading(false))
  }, [])

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
          <div className="text-2xl font-bold text-green-400">{matches.length > 0 ? '48' : '0'}</div>
          <div className="text-xs text-gray-400 mt-1">Jogos Analisados</div>
        </div>
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-4 text-center">
          <div className="text-2xl font-bold text-blue-400">{avgConfidence}%</div>
          <div className="text-xs text-gray-400 mt-1">Confiança Média</div>
        </div>
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-4 text-center">
          <div className="text-2xl font-bold text-purple-400">32</div>
          <div className="text-xs text-gray-400 mt-1">Seleções</div>
        </div>
      </div>

      {/* Top Predictions */}
      <section className="mb-10">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-xl">🎯</span>
          <h2 className="text-xl font-bold text-white">Melhores Apostas do Dia</h2>
          <span className="ml-auto text-xs text-gray-500 bg-gray-800 border border-gray-700 px-2 py-1 rounded">
            Top {topPredictions.length}
          </span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {topPredictions.map((pred, i) => (
            <PredictionCard
              key={i}
              prediction={pred}
              matchInfo={{
                home_team: pred.home_team,
                home_flag: pred.home_flag,
                away_team: pred.away_team,
                away_flag: pred.away_flag,
                date: pred.date,
                match_id: pred.match_id,
              }}
            />
          ))}
        </div>
      </section>

      {/* Upcoming Matches */}
      <section>
        <div className="flex items-center gap-3 mb-4">
          <span className="text-xl">📅</span>
          <h2 className="text-xl font-bold text-white">Próximos Jogos</h2>
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
