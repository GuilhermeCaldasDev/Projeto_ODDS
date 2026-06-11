import { useEffect, useState } from 'react'
import { fetchAllPredictions } from '../api/predictions'
import { Prediction } from '../types'
import PredictionCard from '../components/PredictionCard'
import clsx from 'clsx'

const MARKETS = ['Todos', '1X2', 'Over/Under 2.5', 'BTTS', 'Asian Handicap']

export default function Predictions() {
  const [predictions, setPredictions] = useState<Prediction[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedMarket, setSelectedMarket] = useState('Todos')

  useEffect(() => {
    const market = selectedMarket === 'Todos' ? undefined : selectedMarket
    setLoading(true)
    fetchAllPredictions(market)
      .then((data) => {
        setPredictions(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [selectedMarket])

  const valueBets = predictions.filter((p) => p.value.has_value)
  const highConf = predictions.filter((p) => p.confidence >= 70)

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white mb-1">Top Apostas</h1>
        <p className="text-gray-400 text-sm">Todas as previsões ordenadas por confiança</p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-3 text-center">
          <div className="text-xl font-bold text-green-400">{predictions.length}</div>
          <div className="text-xs text-gray-400">Total Apostas</div>
        </div>
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-3 text-center">
          <div className="text-xl font-bold text-yellow-400">{valueBets.length}</div>
          <div className="text-xs text-gray-400">Value Bets</div>
        </div>
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-3 text-center">
          <div className="text-xl font-bold text-blue-400">{highConf.length}</div>
          <div className="text-xs text-gray-400">Alta Confiança (+70%)</div>
        </div>
      </div>

      {/* Market Filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        {MARKETS.map((m) => (
          <button
            key={m}
            onClick={() => setSelectedMarket(m)}
            className={clsx(
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              selectedMarket === m
                ? 'bg-green-500 text-white'
                : 'bg-gray-800 text-gray-400 border border-gray-700 hover:border-green-500/50 hover:text-white'
            )}
          >
            {m}
          </button>
        ))}
      </div>

      {/* Predictions Grid */}
      {loading ? (
        <div className="text-center py-20 text-gray-400">
          <div className="text-3xl mb-3 animate-bounce">⚽</div>
          <div>Calculando previsões...</div>
        </div>
      ) : (
        <>
          {predictions.length > 0 && (
            <div className="text-xs text-gray-500 mb-4">{predictions.length} previsões encontradas</div>
          )}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {predictions.map((pred, idx) => (
              <PredictionCard
                key={idx}
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
            {predictions.length === 0 && (
              <div className="col-span-3 text-center py-16 text-gray-500">
                Nenhuma previsão encontrada
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}
