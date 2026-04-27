import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useAuthStore } from '../stores/authStore';
import { userAPI, User } from '../services/api';

export default function ProfileScreen() {
  const { username, household, logout } = useAuthStore();
  const [userData, setUserData] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    if (!username) return;
    
    try {
      const user = await userAPI.get(username);
      setUserData(user);
    } catch (error) {
      console.error('Error loading user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      console.log('Logging out...');
      await logout();
      console.log('Logout complete, reloading...');
      // Force page reload on web to clear all state
      if (typeof window !== 'undefined') {
        window.location.reload();
      }
    } catch (error) {
      console.error('Logout error:', error);
      Alert.alert('Error', 'Failed to logout. Please refresh the page manually.');
    }
  };

  const getStreakCount = () => {
    if (!userData?.streaks) return 0;
    return Object.keys(userData.streaks).length;
  };

  const getTotalCompletions = () => {
    if (!userData?.habits_completed) return 0;
    return Object.values(userData.habits_completed).reduce(
      (total, dates) => total + dates.length,
      0
    );
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4CAF50" />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <StatusBar style="light" />
      
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>
            {username?.[0]?.toUpperCase() || '?'}
          </Text>
        </View>
        <Text style={styles.username}>{username}</Text>
        <Text style={styles.household}>{household}</Text>
      </View>

      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{userData?.points || 0}</Text>
          <Text style={styles.statLabel}>Total Points</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{getStreakCount()}</Text>
          <Text style={styles.statLabel}>Active Streaks</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{getTotalCompletions()}</Text>
          <Text style={styles.statLabel}>Completions</Text>
        </View>
      </View>

      {userData?.streaks && Object.keys(userData.streaks).length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Your Streaks 🔥</Text>
          {Object.entries(userData.streaks).map(([habit, streak]) => (
            <View key={habit} style={styles.streakCard}>
              <Text style={styles.streakHabit}>{habit}</Text>
              <Text style={styles.streakValue}>{streak} days 🔥</Text>
            </View>
          ))}
        </View>
      )}

      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Text style={styles.logoutText}>Logout</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#4CAF50',
    paddingTop: 60,
    paddingBottom: 40,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  avatar: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
  },
  avatarText: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  username: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  household: {
    fontSize: 16,
    color: '#fff',
    opacity: 0.9,
  },
  statsContainer: {
    flexDirection: 'row',
    padding: 20,
    gap: 12,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  statValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#4CAF50',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  streakCard: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 16,
    marginBottom: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  streakHabit: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
    flex: 1,
  },
  streakValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#FF5722',
  },
  logoutButton: {
    margin: 20,
    backgroundColor: '#fff',
    padding: 18,
    borderRadius: 16,
    borderWidth: 2,
    borderColor: '#f44336',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  logoutText: {
    color: '#f44336',
    fontSize: 16,
    fontWeight: '600',
  },
});
