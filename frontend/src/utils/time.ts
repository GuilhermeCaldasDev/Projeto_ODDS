// Match times in data are stored in ET (EDT = UTC-4, used in June).
// BRT (Brasília) = UTC-3, so BRT = ET + 1 hour.

export function etToBRT(time: string): string {
  const [h, m] = time.split(':').map(Number)
  const brt = (h + 1) % 24
  return `${String(brt).padStart(2, '0')}:${String(m).padStart(2, '0')}`
}

/**
 * Returns today's date in BRT (UTC-3) as "YYYY-MM-DD",
 * regardless of the browser's local timezone.
 */
export function todayBRT(offsetDays = 0): string {
  const now = new Date()
  // Shift UTC time by -3h to get BRT
  const brt = new Date(now.getTime() - 3 * 60 * 60 * 1000)
  brt.setUTCDate(brt.getUTCDate() + offsetDays)
  const y = brt.getUTCFullYear()
  const m = String(brt.getUTCMonth() + 1).padStart(2, '0')
  const d = String(brt.getUTCDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

/**
 * Returns the match date in BRT, bumping +1 day when a 23:00 ET kickoff
 * crosses midnight (becomes 00:00 BRT next day).
 */
export function matchDateBRT(date: string, time: string): string {
  const [h] = time.split(':').map(Number)
  if (h !== 23) return date
  // Add 1 day
  const d = new Date(date + 'T12:00:00Z')
  d.setUTCDate(d.getUTCDate() + 1)
  const y = d.getUTCFullYear()
  const m = String(d.getUTCMonth() + 1).padStart(2, '0')
  const day = String(d.getUTCDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}
