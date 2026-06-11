import clsx from 'clsx'

interface FormIndicatorProps {
  form: ('W' | 'D' | 'L')[]
  size?: 'sm' | 'md' | 'lg'
}

export default function FormIndicator({ form, size = 'md' }: FormIndicatorProps) {
  const dotSize =
    size === 'sm' ? 'w-4 h-4 text-xs' :
    size === 'lg' ? 'w-7 h-7 text-sm' :
    'w-5 h-5 text-xs'

  return (
    <div className="flex items-center gap-1">
      {form.map((result, i) => (
        <div
          key={i}
          className={clsx(
            'rounded-full flex items-center justify-center font-bold',
            dotSize,
            result === 'W' ? 'bg-green-500 text-white' :
            result === 'D' ? 'bg-yellow-500 text-gray-900' :
            'bg-red-500 text-white'
          )}
        >
          {result}
        </div>
      ))}
    </div>
  )
}
