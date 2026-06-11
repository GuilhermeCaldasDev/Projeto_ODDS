import client from './client'
import { Match } from '../types'

export const fetchMatches = async (group?: string): Promise<Match[]> => {
  const params = group ? { group } : {}
  const res = await client.get('/api/matches', { params })
  return res.data
}

export const fetchMatch = async (id: number): Promise<Match> => {
  const res = await client.get(`/api/matches/${id}`)
  return res.data
}

export const fetchMatchPredictions = async (id: number) => {
  const res = await client.get(`/api/matches/${id}/predictions`)
  return res.data
}
