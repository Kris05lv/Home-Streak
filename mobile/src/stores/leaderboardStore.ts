import { create } from 'zustand';
import { leaderboardAPI, LeaderboardEntry } from '../services/api';

interface LeaderboardState {
  rankings: LeaderboardEntry[];
  isLoading: boolean;
  error: string | null;
  fetchLeaderboard: (household: string) => Promise<void>;
  refreshLeaderboard: (household: string) => Promise<void>;
}

export const useLeaderboardStore = create<LeaderboardState>((set, get) => ({
  rankings: [],
  isLoading: false,
  error: null,

  fetchLeaderboard: async (household: string) => {
    set({ isLoading: true, error: null });
    try {
      const rankings = await leaderboardAPI.get(household);
      set({ rankings, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  refreshLeaderboard: async (household: string) => {
    await get().fetchLeaderboard(household);
  },
}));
