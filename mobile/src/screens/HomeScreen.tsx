import React, { useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  RefreshControl,
  Alert,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useAuthStore } from '../stores/authStore';
import { useHabitStore } from '../stores/habitStore';
import { Habit } from '../services/api';

export default function HomeScreen() {
  const username = useAuthStore((state) => state.username);
  const household = useAuthStore((state) => state.household);
  const { habits, isLoading, fetchHabits, completeHabit } = useHabitStore();

  useEffect(() => {
    fetchHabits();
  }, []);

  const onRefresh = useCallback(async () => {
    await fetchHabits();
  }, [fetchHabits]);

  const handleCompleteHabit = async (habitName: string) => {
    if (!username) return;
    
    try {
      await completeHabit(username, habitName);
      Alert.alert('Success', `Habit '${habitName}' completed! 🎉`);
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to complete habit');
    }
  };

  const renderHabit = ({ item }: { item: Habit }) => (
    <TouchableOpacity
      style={[styles.habitCard, item.is_bonus && styles.bonusHabitCard]}
      onPress={() => handleCompleteHabit(item.name)}
      activeOpacity={0.7}
    >
      <View style={styles.habitHeader}>
        <Text style={styles.habitName}>{item.name}</Text>
        {item.is_bonus && (
          <View style={styles.bonusTag}>
            <Text style={styles.bonusTagText}>⭐ BONUS</Text>
          </View>
        )}
      </View>
      <View style={styles.habitDetails}>
        <Text style={styles.habitPeriodicity}>
          {item.periodicity === 'daily' ? '📅 Daily' : '📆 Weekly'}
        </Text>
        <Text style={styles.habitPoints}>{item.points} pts</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      
      <View style={styles.header}>
        <Text style={styles.greeting}>Hello, {username}! 👋</Text>
        <Text style={styles.household}>{household}</Text>
      </View>

      <View style={styles.content}>
        <Text style={styles.sectionTitle}>Today's Habits</Text>

        <FlatList
          data={habits}
          renderItem={renderHabit}
          keyExtractor={(item) => item.name}
          contentContainerStyle={styles.listContainer}
          refreshControl={
            <RefreshControl
              refreshing={isLoading}
              onRefresh={onRefresh}
              tintColor="#4CAF50"
            />
          }
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyIcon}>📝</Text>
              <Text style={styles.emptyText}>No habits yet!</Text>
              <Text style={styles.emptySubtext}>
                Ask your household admin to add some habits
              </Text>
            </View>
          }
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#4CAF50',
    paddingTop: 60,
    paddingBottom: 30,
    paddingHorizontal: 20,
  },
  greeting: {
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
  content: {
    flex: 1,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: '600',
    color: '#333',
    padding: 20,
    paddingBottom: 10,
  },
  listContainer: {
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  habitCard: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  bonusHabitCard: {
    borderWidth: 2,
    borderColor: '#FFD700',
    backgroundColor: '#FFFEF0',
  },
  habitHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  habitName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    flex: 1,
  },
  bonusTag: {
    backgroundColor: '#FFD700',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  bonusTagText: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#333',
  },
  habitDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  habitPeriodicity: {
    fontSize: 14,
    color: '#666',
  },
  habitPoints: {
    fontSize: 16,
    fontWeight: '700',
    color: '#4CAF50',
  },
  emptyContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 80,
  },
  emptyIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyText: {
    fontSize: 18,
    color: '#999',
    marginBottom: 8,
    fontWeight: '600',
  },
  emptySubtext: {
    fontSize: 14,
    color: '#bbb',
    textAlign: 'center',
  },
});
