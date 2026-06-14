import { useEffect, useState, useMemo, useCallback, useRef } from 'react'
import { fetchMatches } from '../api/matches'
import { Match } from '../types'
import MatchCard from '../components/MatchCard'
import clsx from 'clsx'
import { matchDateBRT, todayBRT } from '../utils/time'

const GROUPS = ['Todos', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
type DateFilter = 'todos' | 'hoje' | 'amanha' | 'semana'

const POLL_INTERVAL = 30_000 // 30 seconds when live matches exist

export default function Matches() {
  const [allMatches, setAllMatches]   = useState<Match[]>([])
  const [selectedGroup, setSelectedGroup] = useState('Todos')
  const [dateFilter, setDateFilter]   = useState<DateFilter>('hoje')
  const [loading, setLoading]         = useState(true)
  const [refreshing, setRefreshing]   = useState(false)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [secondsAgo, setSecondsAgo]   = useState(0)
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const load = useCallback((isRefresh = false) => {
    if (isRefresh) setRefreshing(true)
    else setLoading(true)
    return fetchMatches()
      .then(data => {
        setAllMatches(data)
        setLastUpdated(new Date())
        setSecondsAgo(0)
      })
      .finally(() => {
        setLoading(false)
        setRefreshing(false)
      })
  }, [])

  // Initial load
  useEffect(() => { load() }, [load])

  // "X segundos atrás" counter
  useEffect(() => {
    const tick = setInterval(() => setSecondsAgo(s => s + 1), 1000)
    return () => clearInterval(tick)
  }, [])

  // Auto-polling: active only while there are live matches
  const hasLive = allMatches.some(m => m.status === 'live')
  useEffect(() => {
    if (timerRef.current) clearInterval(timerRef.current)
    if (hasLive) {
      timerRef.current = setInterval(() => load(true), POLL_INTERVAL)
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current) }
  }, [hasLive, load])

  const matches = useMemo(() => {
    let result = allMatches

    if (selectedGroup !== 'Todos') {
      result = result.filter(m => m.group === selectedGroup)
    }

    if (dateFilter === 'hoje') {
      const today = todayBRT(0)
      result = result.filter(m => matchDateBRT(m.date, m.time) === today)
    } else if (dateFilter === 'amanha') {
      const tomorrow = todayBRT(1)
      result = result.filter(m => matchDateBRT(m.date, m.time) === tomorrow)
    } else if (dateFilter === 'semana') {
      const start = todayBRT(0)
      const end   = todayBRT(6)
      result = result.filter(m => {
        const d = matchDateBRT(m.date, m.time)
        return d >= start && d <= end
      })
    }

    return result
  }, [allMatches, selectedGroup, dateFilter])

  const liveCount = matches.filter(m => m.status === 'live').length

  const dateButtons: { key: DateFilter; label: string }[] = [
    { key: 'todos', label: 'Todos os Dias' },
    { key: 'hoje',  label: 'Hoje' },
    { key: 'amanha', label: 'Amanhã' },
    { key: 'semana', label: 'Esta Semana' },
  ]

  return (
    <div>
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Jogos da Copa 2026</h1>
          <p className="text-gray-400 text-sm">Filtre por data e grupo</p>
        </div>

        {/* Refresh controls */}
        <div className="flex flex-col items-end gap-1">
          <button
            onClick={() => load(true)}
            disabled={refreshing}
            className={clsx(
              'flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors',
              refreshing
                ? 'bg-gray-700 text-gray-500 border-gray-600 cursor-not-allowed'
                : 'bg-gray-800 text-gray-300 border-gray-600 hover:bg-gray-700 hover:text-white'
            )}
          >
            <span className={clsx('text-sm', refreshing && 'animate-spin')}>↻</span>
            {refreshing ? 'Atualizando...' : 'Atualizar'}
          </button>
          {lastUpdated && (
            <span className="text-xs text-gray-600">
              {hasLive && <span className="text-red-400 mr-1">● Ao Vivo</span>}
              atualizado há {secondsAgo}s
            </span>
          )}
        </div>
      </div>

      {/* Live banner */}
      {liveCount > 0 && (
        <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 rounded-lg px-4 py-2 mb-4">
          <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
          <span className="text-red-400 text-sm font-medium">
            {liveCount} jogo{liveCount > 1 ? 's' : ''} ao vivo agora · placar atualizado automaticamente a cada 30s
          </span>
        </div>
      )}

      {/* Date Filter */}
      <div className="flex flex-wrap gap-2 mb-4">
        {dateButtons.map(({ key, label }) => (
          <button
            key={key}
            onClick={() => setDateFilter(key)}
            className={clsx(
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              dateFilter === key
                ? 'bg-blue-500 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white border border-gray-700'
            )}
          >
            {label}
            {key === 'hoje' && liveCount > 0 && (
              <span className="ml-1.5 inline-block w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse align-middle" />
            )}
          </button>
        ))}
      </div>

      {/* Group Filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        {GROUPS.map((g) => (
          <button
            key={g}
            onClick={() => setSelectedGroup(g)}
            className={clsx(
              'px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
              selectedGroup === g
                ? 'bg-green-500 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white border border-gray-700'
            )}
          >
            {g === 'Todos' ? 'Todos os Grupos' : `Grupo ${g}`}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-center py-20 text-gray-400">
          <div className="text-3xl mb-3 animate-bounce">⚽</div>
          <div>Carregando jogos...</div>
        </div>
      ) : matches.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <div className="text-3xl mb-3">📅</div>
          <div>Nenhum jogo encontrado para este filtro.</div>
        </div>
      ) : (
        <>
          <div className="text-xs text-gray-500 mb-4">
            {matches.length} jogo{matches.length !== 1 ? 's' : ''} encontrado{matches.length !== 1 ? 's' : ''}
            {refreshing && <span className="ml-2 text-blue-400">· atualizando...</span>}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {matches.map((match) => (
              <MatchCard key={match.id} match={match} />
            ))}
          </div>
        </>
      )}
    </div>
  )
}
