import client from './client'
import { Prediction } from '../types'

export const fetchTopPredictions = async (): Promise<Prediction[]> => {
  const res = await client.get('/api/predictions/top')
  return res.data
}

export const fetchAllPredictions = async (market?: string): Promise<Prediction[]> => {
  const params = market ? { market } : {}
  const res = await client.get('/api/predictions/all', { params })
  return res.data
}

export const fetchOddsStatus = async (): Promise<{ odds_api_configured: boolean; quota_remaining: number | null }> => {
  const res = await client.get('/api/predictions/status')
  return res.data
}
