import React, { useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  RefreshControl,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useAuthStore } from '../stores/authStore';
import { useLeaderboardStore } from '../stores/leaderboardStore';
import { LeaderboardEntry } from '../services/api';

export default function LeaderboardScreen() {
  const household = useAuthStore((state) => state.household);
  const { rankings, isLoading, fetchLeaderboard } = useLeaderboardStore();

  useEffect(() => {
    if (household) {
      fetchLeaderboard(household);
    }
  }, [household]);

  const onRefresh = useCallback(async () => {
    if (household) {
      await fetchLeaderboard(household);
    }
  }, [household, fetchLeaderboard]);

  const getMedalEmoji = (rank: number) => {
    switch (rank) {
      case 1:
        return '🥇';
      case 2:
        return '🥈';
      case 3:
        return '🥉';
      default:
        return `#${rank}`;
    }
  };

  const renderRanking = ({ item }: { item: LeaderboardEntry }) => (
    <View style={[styles.rankCard, item.rank === 1 && styles.firstPlace]}>
      <View style={styles.rankNumber}>
        <Text style={styles.rankText}>{getMedalEmoji(item.rank)}</Text>
      </View>
      <Text style={styles.username}>{item.username}</Text>
      <Text style={styles.points}>{item.points} pts</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      
      <View style={styles.header}>
        <Text style={styles.title}>🏆 Leaderboard</Text>
        <Text style={styles.household}>{household}</Text>
      </View>

      <FlatList
        data={rankings}
        renderItem={renderRanking}
        keyExtractor={(item) => item.username}
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
            <Text style={styles.emptyIcon}>🏅</Text>
            <Text style={styles.emptyText}>No rankings yet!</Text>
            <Text style={styles.emptySubtext}>
              Complete habits to earn points
            </Text>
          </View>
        }
      />
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
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  household: {
    fontSize: 16,
    color: '#fff',
    opacity: 0.9,
  },
  listContainer: {
    padding: 20,
  },
  rankCard: {
    backgroundColor: '#fff',
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    borderRadius: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  firstPlace: {
    borderWidth: 2,
    borderColor: '#FFD700',
    backgroundColor: '#FFFEF0',
  },
  rankNumber: {
    width: 60,
    alignItems: 'center',
  },
  rankText: {
    fontSize: 28,
    fontWeight: 'bold',
  },
  username: {
    flex: 1,
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
  },
  points: {
    fontSize: 18,
    fontWeight: 'bold',
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
  },
});
