import clsx from 'clsx'

interface ConfidenceBarProps {
  confidence: number
  showLabel?: boolean
  size?: 'sm' | 'md'
}

export default function ConfidenceBar({ confidence, showLabel = true, size = 'md' }: ConfidenceBarProps) {
  const color =
    confidence >= 70 ? 'bg-green-500' :
    confidence >= 50 ? 'bg-yellow-500' :
    'bg-red-500'

  const badgeColor =
    confidence >= 70 ? 'bg-green-500/20 text-green-400 border-green-500/30' :
    confidence >= 50 ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30' :
    'bg-red-500/20 text-red-400 border-red-500/30'

  const height = size === 'sm' ? 'h-1.5' : 'h-2'

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs text-gray-400">Confiança</span>
          <span className={clsx('text-xs font-bold px-2 py-0.5 rounded border', badgeColor)}>
            {confidence.toFixed(1)}%
          </span>
        </div>
      )}
      <div className={clsx('w-full bg-gray-700 rounded-full overflow-hidden', height)}>
        <div
          className={clsx('h-full rounded-full transition-all duration-500', color)}
          style={{ width: `${Math.min(100, confidence)}%` }}
        />
      </div>
    </div>
  )
}
