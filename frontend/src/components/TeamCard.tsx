import { Link } from 'react-router-dom'
import { Team } from '../types'
import FormIndicator from './FormIndicator'

interface Props {
  team: Team
}

export default function TeamCard({ team }: Props) {
  return (
    <Link to={`/teams/${encodeURIComponent(team.name)}`} className="block">
      <div className="bg-gray-800 rounded-xl border border-gray-700 p-4 hover:border-green-500/50 transition-all duration-200 hover:shadow-lg hover:shadow-green-500/10">
        <div className="flex items-center gap-3 mb-3">
          <span className="text-4xl">{team.flag}</span>
          <div>
            <div className="font-bold text-white">{team.name}</div>
            <div className="text-xs text-gray-400">{team.confederation} · Grupo {team.group}</div>
          </div>
          <div className="ml-auto text-right">
            <div className="text-xs text-gray-500">Ranking FIFA</div>
            <div className="text-lg font-bold text-green-400">#{team.ranking}</div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-2 mb-3">
          <div className="bg-gray-700/50 rounded-lg p-2 text-center">
            <div className="text-xs text-gray-400 mb-1">Ataque</div>
            <div className="text-sm font-bold text-orange-400">{team.attack_rating}</div>
            <div className="w-full bg-gray-600 rounded-full h-1 mt-1">
              <div className="bg-orange-500 h-1 rounded-full" style={{ width: `${team.attack_rating}%` }} />
            </div>
          </div>
          <div className="bg-gray-700/50 rounded-lg p-2 text-center">
            <div className="text-xs text-gray-400 mb-1">Defesa</div>
            <div className="text-sm font-bold text-blue-400">{team.defense_rating}</div>
            <div className="w-full bg-gray-600 rounded-full h-1 mt-1">
              <div className="bg-blue-500 h-1 rounded-full" style={{ width: `${team.defense_rating}%` }} />
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-400">Forma recente</span>
          <FormIndicator form={team.form} size="sm" />
        </div>
      </div>
    </Link>
  )
}
