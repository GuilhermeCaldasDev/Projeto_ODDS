import { useEffect, useState } from 'react'
import { fetchGroups, fetchTeams } from '../api/teams'
import { Team, GroupStanding } from '../types'
import TeamCard from '../components/TeamCard'
import GroupTable from '../components/GroupTable'
import clsx from 'clsx'

type ViewMode = 'grid' | 'standings'

export default function Teams() {
  const [teams, setTeams] = useState<Team[]>([])
  const [groups, setGroups] = useState<Record<string, GroupStanding[]>>({})
  const [viewMode, setViewMode] = useState<ViewMode>('standings')
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([fetchTeams(), fetchGroups()])
      .then(([teamsData, groupsData]) => {
        setTeams(teamsData)
        setGroups(groupsData)
      })
      .finally(() => setLoading(false))
  }, [])

  const filteredTeams = teams.filter(t =>
    t.name.toLowerCase().includes(search.toLowerCase()) ||
    t.confederation.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Seleções</h1>
          <p className="text-gray-400 text-sm">48 seleções qualificadas para a Copa 2026</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('standings')}
            className={clsx('px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              viewMode === 'standings' ? 'bg-green-500 text-white' : 'bg-gray-800 text-gray-400 border border-gray-700 hover:bg-gray-700'
            )}
          >
            Grupos
          </button>
          <button
            onClick={() => setViewMode('grid')}
            className={clsx('px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              viewMode === 'grid' ? 'bg-green-500 text-white' : 'bg-gray-800 text-gray-400 border border-gray-700 hover:bg-gray-700'
            )}
          >
            Cards
          </button>
        </div>
      </div>

      {viewMode === 'grid' && (
        <input
          type="text"
          placeholder="Buscar seleção..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 mb-6 focus:outline-none focus:border-green-500"
        />
      )}

      {loading ? (
        <div className="text-center py-20 text-gray-400">
          <div className="text-3xl mb-3 animate-bounce">⚽</div>
          <div>Carregando seleções...</div>
        </div>
      ) : viewMode === 'standings' ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {Object.entries(groups).map(([group, standings]) => (
            <GroupTable key={group} group={group} standings={standings} />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredTeams.map(team => (
            <TeamCard key={team.name} team={team} />
          ))}
        </div>
      )}
    </div>
  )
}
