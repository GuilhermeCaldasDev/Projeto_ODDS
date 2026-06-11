import { useEffect, useState } from 'react'
import { fetchMatches } from '../api/matches'
import { Match } from '../types'
import MatchCard from '../components/MatchCard'
import clsx from 'clsx'

const GROUPS = ['Todos', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

export default function Matches() {
  const [matches, setMatches] = useState<Match[]>([])
  const [selectedGroup, setSelectedGroup] = useState('Todos')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const group = selectedGroup === 'Todos' ? undefined : selectedGroup
    setLoading(true)
    fetchMatches(group)
      .then(setMatches)
      .finally(() => setLoading(false))
  }, [selectedGroup])

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white mb-1">Jogos da Copa 2026</h1>
        <p className="text-gray-400 text-sm">Selecione um grupo para filtrar</p>
      </div>

      {/* Group Tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        {GROUPS.map((g) => (
          <button
            key={g}
            onClick={() => setSelectedGroup(g)}
            className={clsx(
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              selectedGroup === g
                ? 'bg-green-500 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white border border-gray-700'
            )}
          >
            {g === 'Todos' ? 'Todos os Jogos' : `Grupo ${g}`}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-center py-20 text-gray-400">
          <div className="text-3xl mb-3 animate-bounce">⚽</div>
          <div>Carregando jogos...</div>
        </div>
      ) : (
        <>
          <div className="text-xs text-gray-500 mb-4">{matches.length} jogos encontrados</div>
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
