import client from './client'
import { Team, GroupStanding } from '../types'

export const fetchTeams = async (): Promise<Team[]> => {
  const res = await client.get('/api/teams')
  return res.data
}

export const fetchTeam = async (name: string): Promise<Team> => {
  const res = await client.get(`/api/teams/${name}`)
  return res.data
}

export const fetchGroups = async (): Promise<Record<string, GroupStanding[]>> => {
  const res = await client.get('/api/groups')
  return res.data
}
