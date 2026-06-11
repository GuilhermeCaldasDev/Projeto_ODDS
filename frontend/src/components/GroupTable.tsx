import { GroupStanding } from '../types'

interface Props {
  group: string
  standings: GroupStanding[]
}

export default function GroupTable({ group, standings }: Props) {
  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
      <div className="bg-gray-700/50 px-4 py-2 flex items-center gap-2">
        <span className="text-green-400 font-bold text-sm">Grupo {group}</span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-gray-400 text-xs border-b border-gray-700">
              <th className="text-left px-4 py-2">#</th>
              <th className="text-left px-4 py-2">Seleção</th>
              <th className="text-center px-2 py-2">J</th>
              <th className="text-center px-2 py-2">V</th>
              <th className="text-center px-2 py-2">E</th>
              <th className="text-center px-2 py-2">D</th>
              <th className="text-center px-2 py-2">GP</th>
              <th className="text-center px-2 py-2">GC</th>
              <th className="text-center px-2 py-2">SG</th>
              <th className="text-center px-2 py-2 font-bold text-white">Pts</th>
            </tr>
          </thead>
          <tbody>
            {standings.map((s, i) => (
              <tr
                key={s.team}
                className={`border-b border-gray-700/50 ${i < 2 ? 'text-white' : 'text-gray-400'}`}
              >
                <td className="px-4 py-3">
                  <span className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold ${i < 2 ? 'bg-green-500 text-white' : 'bg-gray-700 text-gray-400'}`}>
                    {i + 1}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <span>{s.flag}</span>
                    <span className="font-medium">{s.team}</span>
                    <span className="text-xs text-gray-500">#{s.ranking}</span>
                  </div>
                </td>
                <td className="text-center px-2 py-3">{s.played}</td>
                <td className="text-center px-2 py-3">{s.won}</td>
                <td className="text-center px-2 py-3">{s.drawn}</td>
                <td className="text-center px-2 py-3">{s.lost}</td>
                <td className="text-center px-2 py-3">{s.goals_for}</td>
                <td className="text-center px-2 py-3">{s.goals_against}</td>
                <td className="text-center px-2 py-3">{s.goal_diff > 0 ? `+${s.goal_diff}` : s.goal_diff}</td>
                <td className="text-center px-2 py-3 font-bold text-white">{s.points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
