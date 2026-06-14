import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { fetchTeam } from '../api/teams'
import { fetchMatches } from '../api/matches'
import { Team, Match, TournamentStats } from '../types'
import FormIndicator from '../components/FormIndicator'
import ConfidenceBar from '../components/ConfidenceBar'

function StatTile({ label, value, sub, color = 'text-white' }: { label: string; value: string | number; sub?: string; color?: string }) {
  return (
    <div className="bg-gray-700/50 rounded-lg p-3 text-center">
      <div className={`text-2xl font-bold ${color}`}>{value}</div>
      {sub && <div className="text-[10px] text-gray-500">{sub}</div>}
      <div className="text-xs text-gray-400 mt-1">{label}</div>
    </div>
  )
}

function TournamentStatsBlock({ ts }: { ts: TournamentStats }) {
  const perGame = (n: number) => ts.played ? (n / ts.played).toFixed(1) : '0'
  return (
    <div className="bg-gray-800 rounded-xl border border-green-500/30 p-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-green-400">Copa 2026 — Dados Reais</h2>
        <span className="text-xs text-gray-500">{ts.played} jogo{ts.played !== 1 ? 's' : ''} disputado{ts.played !== 1 ? 's' : ''}</span>
      </div>

      {/* Resultado */}
      <div className="grid grid-cols-4 gap-2 mb-3">
        <StatTile label="Pontos" value={ts.points} color="text-yellow-400" />
        <StatTile label="Vitórias" value={ts.wins} color="text-green-400" />
        <StatTile label="Empates" value={ts.draws} color="text-yellow-300" />
        <StatTile label="Derrotas" value={ts.losses} color="text-red-400" />
      </div>

      {/* Gols */}
      <div className="grid grid-cols-3 gap-2 mb-3">
        <StatTile label="Gols Marcados" value={ts.goals_for} sub={`${perGame(ts.goals_for)}/jogo`} color="text-green-400" />
        <StatTile label="Gols Sofridos" value={ts.goals_against} sub={`${perGame(ts.goals_against)}/jogo`} color="text-red-400" />
        <StatTile label="Saldo" value={ts.goal_diff >= 0 ? `+${ts.goal_diff}` : `${ts.goal_diff}`} color={ts.goal_diff >= 0 ? 'text-green-400' : 'text-red-400'} />
      </div>

      {/* Stats de jogo */}
      <div className="grid grid-cols-3 gap-2 mb-3">
        <StatTile label="Finalizações" value={ts.shots} sub={`${perGame(ts.shots)}/jogo`} color="text-blue-400" />
        <StatTile label="No Gol" value={ts.shots_on_target} sub={`${perGame(ts.shots_on_target)}/jogo`} color="text-blue-300" />
        <StatTile label="Escanteios" value={ts.corners} sub={`${perGame(ts.corners)}/jogo`} color="text-purple-400" />
      </div>

      {/* Disciplina */}
      <div className="grid grid-cols-3 gap-2">
        <StatTile label="Faltas" value={ts.fouls} sub={`${perGame(ts.fouls)}/jogo`} color="text-orange-400" />
        <StatTile label="Cartões Amarelos" value={ts.yellow_cards} color="text-yellow-400" />
        <StatTile label="Cartões Vermelhos" value={ts.red_cards} color="text-red-500" />
      </div>
    </div>
  )
}

export default function TeamDetail() {
  const { name } = useParams<{ name: string }>()
  const [team, setTeam] = useState<Team | null>(null)
  const [nextMatch, setNextMatch] = useState<Match | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!name) return
    Promise.all([fetchTeam(name), fetchMatches()])
      .then(([teamData, allMatches]) => {
        setTeam(teamData)
        const next = allMatches.find(
          (m) =>
            (m.home_team.toLowerCase() === name.toLowerCase() ||
              m.away_team.toLowerCase() === name.toLowerCase()) &&
            m.status === 'upcoming'
        )
        setNextMatch(next || null)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [name])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-4xl animate-spin">⚽</div>
      </div>
    )
  }

  if (!team) {
    return (
      <div className="text-center py-16">
        <div className="text-4xl mb-4">❌</div>
        <p className="text-gray-400">Seleção não encontrada</p>
        <Link to="/teams" className="text-green-400 hover:text-green-300 mt-2 inline-block">
          Voltar às Seleções
        </Link>
      </div>
    )
  }

  const formScore = team.form_score || 50

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm text-gray-500">
        <Link to="/" className="hover:text-gray-300">Dashboard</Link>
        <span>›</span>
        <Link to="/teams" className="hover:text-gray-300">Seleções</Link>
        <span>›</span>
        <span className="text-gray-300">{team.name}</span>
      </div>

      {/* Team Header */}
      <div className="bg-gray-800 rounded-2xl border border-gray-700 p-6">
        <div className="flex items-center gap-6">
          <span className="text-8xl">{team.flag}</span>
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-white mb-1">{team.name}</h1>
            <div className="flex items-center gap-4 text-sm text-gray-400">
              <span>{team.confederation}</span>
              <span>·</span>
              <span>Grupo {team.group}</span>
              <span>·</span>
              <span className="text-yellow-400 font-semibold">#{team.ranking} FIFA</span>
            </div>
            <div className="mt-3">
              <FormIndicator form={team.form} size="lg" />
            </div>
          </div>
        </div>
      </div>

      {/* Copa 2026 Tournament Stats */}
      {team.tournament_stats && team.tournament_stats.played > 0 ? (
        <TournamentStatsBlock ts={team.tournament_stats} />
      ) : (
        <div className="bg-gray-800/50 rounded-xl border border-gray-700/50 p-4 text-center text-gray-500 text-sm">
          Ainda não jogou na Copa 2026
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-4 text-center">
          <div className="text-xs text-gray-400 mb-2">Ataque</div>
          <div className="text-3xl font-bold text-orange-400 mb-2">{team.attack_rating}</div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div
              className="bg-orange-500 h-2 rounded-full"
              style={{ width: `${team.attack_rating}%` }}
            />
          </div>
        </div>
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-4 text-center">
          <div className="text-xs text-gray-400 mb-2">Defesa</div>
          <div className="text-3xl font-bold text-blue-400 mb-2">{team.defense_rating}</div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full"
              style={{ width: `${team.defense_rating}%` }}
            />
          </div>
        </div>
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-4 text-center">
          <div className="text-xs text-gray-400 mb-2">Média Gols Marcados</div>
          <div className="text-3xl font-bold text-green-400">{team.goals_scored_avg}</div>
          <div className="text-xs text-gray-500">por jogo</div>
        </div>
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-4 text-center">
          <div className="text-xs text-gray-400 mb-2">Média Gols Sofridos</div>
          <div className="text-3xl font-bold text-red-400">{team.goals_conceded_avg}</div>
          <div className="text-xs text-gray-500">por jogo</div>
        </div>
      </div>

      {/* Form Score */}
      <div className="bg-gray-800 rounded-xl border border-gray-700 p-4">
        <h2 className="text-sm font-semibold text-gray-400 mb-3">Índice de Forma</h2>
        <ConfidenceBar confidence={formScore} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Recent Results */}
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-4">
          <h2 className="text-sm font-semibold text-white mb-4">Resultados Recentes</h2>
          <div className="space-y-2">
            {team.recent_results.map((result, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between py-2 border-b border-gray-700/50 last:border-0"
              >
                <div className="flex items-center gap-3">
                  <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                    result.result === 'W' ? 'bg-green-500 text-white' :
                    result.result === 'D' ? 'bg-yellow-500 text-gray-900' :
                    'bg-red-500 text-white'
                  }`}>
                    {result.result}
                  </span>
                  <span className="text-sm text-gray-300">vs {result.opponent}</span>
                </div>
                <span className="text-sm font-semibold text-white">{result.score}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Key Players + Next Match */}
        <div className="space-y-4">
          {/* Key Players */}
          <div className="bg-gray-800 rounded-xl border border-gray-700 p-4">
            <h2 className="text-sm font-semibold text-white mb-4">Jogadores-Chave</h2>
            <div className="space-y-2">
              {team.key_players.map((player, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-3 py-2 border-b border-gray-700/50 last:border-0"
                >
                  <div className="w-7 h-7 bg-gray-700 rounded-full flex items-center justify-center text-xs font-bold text-green-400">
                    {idx + 1}
                  </div>
                  <span className="text-sm text-white">{player}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Next Match */}
          {nextMatch && (
            <div className="bg-gray-800 rounded-xl border border-green-500/30 p-4">
              <h2 className="text-sm font-semibold text-green-400 mb-3">Próximo Jogo</h2>
              <Link to={`/matches/${nextMatch.id}`} className="block hover:opacity-80 transition-opacity">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">{nextMatch.home_team_data?.flag}</span>
                    <span className="text-sm font-medium text-white">{nextMatch.home_team}</span>
                  </div>
                  <span className="text-gray-400 text-sm font-medium">VS</span>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-white">{nextMatch.away_team}</span>
                    <span className="text-2xl">{nextMatch.away_team_data?.flag}</span>
                  </div>
                </div>
                <div className="mt-2 text-xs text-gray-500">
                  {nextMatch.date} · {nextMatch.time}
                </div>
                <div className="text-xs text-gray-500">{nextMatch.venue}</div>
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
