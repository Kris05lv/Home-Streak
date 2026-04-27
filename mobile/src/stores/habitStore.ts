import { create } from 'zustand';
import { habitAPI, Habit } from '../services/api';

interface HabitState {
  habits: Habit[];
  isLoading: boolean;
  error: string | null;
  fetchHabits: () => Promise<void>;
  completeHabit: (username: string, habitName: string) => Promise<void>;
  refreshHabits: () => Promise<void>;
}

export const useHabitStore = create<HabitState>((set, get) => ({
  habits: [],
  isLoading: false,
  error: null,

  fetchHabits: async () => {
    set({ isLoading: true, error: null });
    try {
      const habits = await habitAPI.getAll();
      set({ habits, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  completeHabit: async (username: string, habitName: string) => {
    try {
      await habitAPI.complete(username, habitName);
      await get().fetchHabits();
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    }
  },

  refreshHabits: async () => {
    await get().fetchHabits();
  },
}));
