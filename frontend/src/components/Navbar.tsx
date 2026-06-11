import { Link, useLocation } from 'react-router-dom'
import clsx from 'clsx'

const navLinks = [
  { path: '/', label: 'Dashboard' },
  { path: '/matches', label: 'Jogos' },
  { path: '/teams', label: 'Seleções' },
  { path: '/predictions', label: 'Apostas' },
]

export default function Navbar() {
  const location = useLocation()

  return (
    <nav className="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-3">
            <span className="text-2xl">🏆</span>
            <div>
              <span className="text-white font-bold text-lg leading-none block">Copa do Mundo</span>
              <span className="text-green-400 text-xs font-semibold">2026 · Análise de Apostas</span>
            </div>
          </Link>

          <div className="flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={clsx(
                  'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  location.pathname === link.path
                    ? 'bg-green-500 text-white'
                    : 'text-gray-300 hover:text-white hover:bg-gray-700'
                )}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}
