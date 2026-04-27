import axios from 'axios';
import Constants from 'expo-constants';
import { Platform } from 'react-native';

// Use localhost for web, 10.0.2.2 for Android emulator
const API_BASE_URL = Platform.OS === 'web' 
  ? 'http://localhost:8000' 
  : (Constants.expoConfig?.extra?.apiUrl || 'http://10.0.2.2:8000');

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export interface Household {
  name: string;
}

export interface User {
  username: string;
  household: string;
  points: number;
  is_admin?: boolean;
  habits_completed?: Record<string, string[]>;
  streaks?: Record<string, number>;
  bonus_claimed?: Record<string, string>;
}

export interface Habit {
  name: string;
  periodicity: string;
  points: number;
  is_bonus: boolean;
  created_at?: string;
}

export interface LeaderboardEntry {
  rank: number;
  username: string;
  points: number;
}

export const householdAPI = {
  create: async (name: string) => {
    const response = await api.post('/households', { name });
    return response.data;
  },
  getAll: async (): Promise<string[]> => {
    const response = await api.get('/households');
    return response.data.households;
  },
  verifyPassword: async (household_name: string, password: string) => {
    const response = await api.post('/households/verify', { household_name, password });
    return response.data.verified;
  },
  updatePassword: async (household_name: string, new_password: string) => {
    const response = await api.put(`/households/${household_name}/password`, null, {
      params: { new_password }
    });
    return response.data;
  },
};

export const userAPI = {
  create: async (username: string, household_name: string) => {
    const response = await api.post('/users', { username, household_name });
    return response.data;
  },
  get: async (username: string): Promise<User> => {
    const response = await api.get(`/users/${username}`);
    return response.data;
  },
  getAll: async (): Promise<User[]> => {
    const response = await api.get('/users');
    return response.data.users;
  },
};

export const habitAPI = {
  create: async (name: string, periodicity: string, points: number, is_bonus: boolean = false) => {
    const response = await api.post('/habits', { name, periodicity, points, is_bonus });
    return response.data;
  },
  getAll: async (): Promise<Habit[]> => {
    const response = await api.get('/habits');
    return response.data.habits;
  },
  complete: async (username: string, habit_name: string) => {
    const response = await api.post('/habits/complete', { username, habit_name });
    return response.data;
  },
};

export const leaderboardAPI = {
  get: async (household_name: string): Promise<LeaderboardEntry[]> => {
    const response = await api.get(`/leaderboard/${household_name}`);
    return response.data.rankings;
  },
  getPast: async (household_name: string) => {
    const response = await api.get(`/leaderboard/${household_name}/past`);
    return response.data.past_rankings;
  },
  getTopPerformers: async () => {
    const response = await api.get('/top-performers');
    return response.data.top_performers;
  },
};

export const adminAPI = {
  createHouseholdWithAdmin: async (household_name: string, admin_username: string, password?: string) => {
    const response = await api.post(`/households/${household_name}/admin`, null, {
      params: { admin_username, password }
    });
    return response.data;
  },
  addMember: async (username: string, household_name: string) => {
    const response = await api.post('/admin/members', null, {
      params: { username, household_name }
    });
    return response.data;
  },
  getMembers: async (household_name: string) => {
    const response = await api.get(`/households/${household_name}/members`);
    return response.data.members;
  },
};

export default api;
