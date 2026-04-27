import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthState {
  username: string | null;
  household: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, household: string) => Promise<void>;
  logout: () => Promise<void>;
  loadAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  username: null,
  household: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (username: string, household: string) => {
    try {
      await AsyncStorage.setItem('@username', username);
      await AsyncStorage.setItem('@household', household);
      set({ username, household, isAuthenticated: true });
    } catch (error) {
      console.error('Error saving auth:', error);
      throw error;
    }
  },

  logout: async () => {
    try {
      await AsyncStorage.removeItem('@username');
      await AsyncStorage.removeItem('@household');
      set({ 
        username: null, 
        household: null, 
        isAuthenticated: false,
        isLoading: false 
      });
    } catch (error) {
      console.error('Error clearing auth:', error);
      // Force logout even if storage fails
      set({ 
        username: null, 
        household: null, 
        isAuthenticated: false,
        isLoading: false 
      });
    }
  },

  loadAuth: async () => {
    try {
      const username = await AsyncStorage.getItem('@username');
      const household = await AsyncStorage.getItem('@household');
      
      if (username && household) {
        set({ username, household, isAuthenticated: true, isLoading: false });
      } else {
        set({ isLoading: false });
      }
    } catch (error) {
      console.error('Error loading auth:', error);
      set({ isLoading: false });
    }
  },
}));
