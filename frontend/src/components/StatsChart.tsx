import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, Legend } from 'recharts'
import { Team } from '../types'

interface Props {
  team1: Team
  team2: Team
}

export default function StatsChart({ team1, team2 }: Props) {
  const form1 = team1.form_score ?? team1.form.reduce((a, r) => a + (r === 'W' ? 100 : r === 'D' ? 50 : 0), 0) / team1.form.length
  const form2 = team2.form_score ?? team2.form.reduce((a, r) => a + (r === 'W' ? 100 : r === 'D' ? 50 : 0), 0) / team2.form.length
  const rank1 = Math.max(0, 100 - team1.ranking)
  const rank2 = Math.max(0, 100 - team2.ranking)

  const data = [
    { stat: 'Ataque', [team1.name]: team1.attack_rating, [team2.name]: team2.attack_rating },
    { stat: 'Defesa', [team1.name]: team1.defense_rating, [team2.name]: team2.defense_rating },
    { stat: 'Forma', [team1.name]: Math.round(form1), [team2.name]: Math.round(form2) },
    { stat: 'Ranking', [team1.name]: Math.round(rank1), [team2.name]: Math.round(rank2) },
    { stat: 'Gols/Jogo', [team1.name]: Math.round(team1.goals_scored_avg * 33), [team2.name]: Math.round(team2.goals_scored_avg * 33) },
  ]

  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700 p-4">
      <h3 className="text-sm font-semibold text-gray-400 mb-4 text-center">Comparação de Estatísticas</h3>
      <ResponsiveContainer width="100%" height={280}>
        <RadarChart data={data}>
          <PolarGrid stroke="#374151" />
          <PolarAngleAxis dataKey="stat" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
          <Radar name={team1.name} dataKey={team1.name} stroke="#22c55e" fill="#22c55e" fillOpacity={0.2} strokeWidth={2} />
          <Radar name={team2.name} dataKey={team2.name} stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.2} strokeWidth={2} />
          <Legend
            wrapperStyle={{ color: '#9CA3AF', fontSize: '12px' }}
            formatter={(value) => <span style={{ color: '#e5e7eb' }}>{value}</span>}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}
