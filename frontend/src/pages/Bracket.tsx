import { useEffect, useState } from 'react'
import { fetchBracketPrediction, BracketPrediction, KOMatch, GroupTeamPrediction } from '../api/bracket'
import clsx from 'clsx'

function GroupCard({ group, standings }: { group: string; standings: GroupTeamPrediction[] }) {
  return (
    <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
      <h3 className="text-green-400 font-bold text-sm mb-3 uppercase tracking-wider">Grupo {group}</h3>
      <div className="space-y-1">
        {standings.map((team) => (
          <div
            key={team.name}
            className={clsx(
              'flex items-center gap-2 px-2 py-1.5 rounded-lg text-sm',
              team.position <= 2 ? 'bg-green-900/30 border border-green-800/40' : 'border border-transparent'
            )}
          >
            <span className="w-5 text-center font-bold text-gray-500 text-xs">{team.position}</span>
            <span className="text-lg leading-none">{team.flag}</span>
            <span className={clsx('flex-1 font-medium truncate', team.position <= 2 ? 'text-white' : 'text-gray-400')}>
              {team.name}
            </span>
            <span className="text-xs text-gray-400 w-8 text-right">{team.predicted_pts.toFixed(1)}pts</span>
            {team.position <= 2 && (
              <span className="text-green-400 text-xs font-bold ml-1">✓</span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function KOMatchCard({ match, round }: { match: KOMatch; round: string }) {
  const homeWin = match.home_win_prob > match.away_win_prob

  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
      <div className="px-3 py-1.5 bg-gray-750 border-b border-gray-700 flex items-center justify-between">
        <span className="text-xs text-gray-500">{round} · Jogo {match.match}</span>
        {match.date && <span className="text-xs text-gray-600">{match.date}</span>}
      </div>
      <div className="p-3 space-y-2">
        <div className={clsx('flex items-center gap-2', homeWin ? 'opacity-100' : 'opacity-60')}>
          <span className="text-xl">{match.home_flag}</span>
          <span className={clsx('flex-1 text-sm font-medium', homeWin ? 'text-white' : 'text-gray-400')}>
            {match.home || match.slot1 || '?'}
          </span>
          <span className="text-xs text-gray-400">{(match.home_win_prob * 100).toFixed(0)}%</span>
          {homeWin && <span className="text-yellow-400 text-xs">★</span>}
        </div>
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <div className="flex-1 h-px bg-gray-700" />
          <span className="px-2">VS</span>
          <div className="flex-1 h-px bg-gray-700" />
        </div>
        <div className={clsx('flex items-center gap-2', !homeWin ? 'opacity-100' : 'opacity-60')}>
          <span className="text-xl">{match.away_flag}</span>
          <span className={clsx('flex-1 text-sm font-medium', !homeWin ? 'text-white' : 'text-gray-400')}>
            {match.away || match.slot2 || '?'}
          </span>
          <span className="text-xs text-gray-400">{(match.away_win_prob * 100).toFixed(0)}%</span>
          {!homeWin && <span className="text-yellow-400 text-xs">★</span>}
        </div>
      </div>
      {match.predicted_score && (
        <div className="px-3 pb-3">
          <div className="bg-gray-900 rounded-lg px-3 py-1.5 text-center">
            <span className="text-white font-bold text-sm">{match.predicted_score}</span>
            <span className="text-gray-500 text-xs ml-2">placar previsto</span>
          </div>
        </div>
      )}
    </div>
  )
}

type Tab = 'groups' | 'r32' | 'r16' | 'qf' | 'sf' | 'final'

export default function Bracket() {
  const [data, setData] = useState<BracketPrediction | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [tab, setTab] = useState<Tab>('groups')

  useEffect(() => {
    fetchBracketPrediction()
      .then(setData)
      .catch(() => setError('Erro ao carregar previsões do chaveamento.'))
      .finally(() => setLoading(false))
  }, [])

  const tabs: { id: Tab; label: string }[] = [
    { id: 'groups', label: 'Grupos' },
    { id: 'r32', label: 'Oitavas (R32)' },
    { id: 'r16', label: 'Décimas (R16)' },
    { id: 'qf', label: 'Quartas' },
    { id: 'sf', label: 'Semis' },
    { id: 'final', label: 'Final' },
  ]

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white mb-1">Chaveamento Copa 2026</h1>
        <p className="text-gray-400 text-sm">Previsão completa baseada em análise estatística · 48 seleções</p>
      </div>

      {loading && (
        <div className="text-center py-20 text-gray-400">
          <div className="text-3xl mb-3 animate-bounce">🏆</div>
          <div>Simulando chaveamento...</div>
        </div>
      )}

      {error && (
        <div className="text-center py-20 text-red-400">{error}</div>
      )}

      {data && (
        <>
          {/* Champion Banner */}
          {data.predicted_champion && (
            <div className="mb-6 bg-gradient-to-r from-yellow-900/40 via-yellow-800/20 to-yellow-900/40 border border-yellow-700/50 rounded-2xl p-5 flex items-center gap-4">
              <span className="text-5xl">{data.predicted_champion.flag}</span>
              <div>
                <div className="text-xs text-yellow-400 font-semibold uppercase tracking-wider mb-1">Campeão Previsto</div>
                <div className="text-2xl font-bold text-white">{data.predicted_champion.name}</div>
                <div className="text-sm text-gray-400 mt-0.5">
                  Ranking FIFA #{data.predicted_champion.ranking} ·
                  Ataque {data.predicted_champion.attack_rating} ·
                  Defesa {data.predicted_champion.defense_rating}
                </div>
              </div>
              <div className="ml-auto text-4xl">🏆</div>
            </div>
          )}

          {/* Third-place wildcards summary */}
          <div className="mb-6 bg-gray-800 rounded-xl border border-gray-700 p-4">
            <h2 className="text-sm font-semibold text-gray-300 mb-3">
              Melhores 3os lugares classificados (wildcards para R32)
            </h2>
            <div className="flex flex-wrap gap-2">
              {data.third_place_qualifiers.map((t) => (
                <div key={t.name} className="flex items-center gap-1.5 bg-blue-900/30 border border-blue-700/40 rounded-lg px-2.5 py-1">
                  <span>{t.flag}</span>
                  <span className="text-xs text-blue-300 font-medium">{t.name}</span>
                  <span className="text-xs text-gray-500">Gr.{t.group}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Tabs */}
          <div className="flex flex-wrap gap-2 mb-6">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={clsx(
                  'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  tab === t.id
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white border border-gray-700'
                )}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* Groups Tab */}
          {tab === 'groups' && (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {Object.entries(data.group_predictions).map(([group, standings]) => (
                <GroupCard key={group} group={group} standings={standings} />
              ))}
            </div>
          )}

          {/* Round of 32 */}
          {tab === 'r32' && (
            <>
              <p className="text-xs text-gray-500 mb-4">
                32 times: Top 2 de cada grupo (24) + 8 melhores 3os lugares
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
                {data.round_of_32.map((m) => (
                  <KOMatchCard key={m.match} match={m} round="R32" />
                ))}
              </div>
            </>
          )}

          {/* Round of 16 */}
          {tab === 'r16' && (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
              {data.round_of_16.map((m) => (
                <KOMatchCard key={m.match} match={m} round="R16" />
              ))}
            </div>
          )}

          {/* Quarterfinals */}
          {tab === 'qf' && (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
              {data.quarterfinals.map((m) => (
                <KOMatchCard key={m.match} match={m} round="Quartas" />
              ))}
            </div>
          )}

          {/* Semifinals */}
          {tab === 'sf' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl">
              {data.semifinals.map((m) => (
                <KOMatchCard key={m.match} match={m} round="Semifinal" />
              ))}
            </div>
          )}

          {/* Final */}
          {tab === 'final' && data.final && (
            <div className="max-w-sm">
              <div className="text-center mb-4">
                <span className="text-3xl">🏆</span>
                <h2 className="text-xl font-bold text-yellow-400 mt-1">Grande Final</h2>
                {data.final.date && <p className="text-gray-500 text-sm">{data.final.date} · {data.final.venue}</p>}
              </div>
              <KOMatchCard match={data.final} round="Final" />
            </div>
          )}
        </>
      )}
    </div>
  )
}
