import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  ScrollView,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { userAPI, householdAPI, adminAPI } from '../services/api';
import { useAuthStore } from '../stores/authStore';

export default function LoginScreen() {
  const [username, setUsername] = useState('');
  const [household, setHousehold] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const login = useAuthStore((state) => state.login);

  const handleLogin = async () => {
    if (!username.trim() || !household.trim()) {
      Alert.alert('Error', 'Please enter both username and household');
      return;
    }

    if (!isAdmin && !password.trim()) {
      Alert.alert('Error', 'Please enter the family password/PIN');
      return;
    }

    setLoading(true);
    try {
      if (isAdmin) {
        // Admin creating new household with optional password
        await adminAPI.createHouseholdWithAdmin(household, username, password || undefined);
      } else {
        // Member logging in - verify password first
        await householdAPI.verifyPassword(household, password);
        await userAPI.get(username);
      }
      
      await login(username, household);
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <StatusBar style="dark" />
      
      <View style={styles.header}>
        <Text style={styles.title}>🏠 Home Streak</Text>
        <Text style={styles.subtitle}>Track habits with your family</Text>
      </View>

      <View style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
          autoCapitalize="none"
          editable={!loading}
        />

        <TextInput
          style={styles.input}
          placeholder="Household Name"
          value={household}
          onChangeText={setHousehold}
          autoCapitalize="none"
          editable={!loading}
        />

        <TextInput
          style={styles.input}
          placeholder={isAdmin ? "Family Password/PIN (optional)" : "Family Password/PIN"}
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          editable={!loading}
          keyboardType="default"
        />

        <TouchableOpacity
          style={styles.checkboxContainer}
          onPress={() => setIsAdmin(!isAdmin)}
          disabled={loading}
        >
          <View style={[styles.checkbox, isAdmin && styles.checkboxChecked]}>
            {isAdmin && <Text style={styles.checkmark}>✓</Text>}
          </View>
          <Text style={styles.checkboxLabel}>I'm setting up a new family (Admin)</Text>
        </TouchableOpacity>

        <View style={styles.instructionBox}>
          <Text style={styles.instructionTitle}>
            {isAdmin ? '👨‍👩‍👧‍👦 Admin Setup' : '👤 Member Login'}
          </Text>
          <Text style={styles.instructionText}>
            {isAdmin 
              ? 'Set a password/PIN to secure your family. You can add members after login.'
              : 'Enter your name and the family password/PIN (ask your admin if you don\'t know it)'}
          </Text>
        </View>

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleLogin}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>{isAdmin ? 'Create Family & Login' : 'Login'}</Text>
          )}
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    paddingTop: 60,
    paddingBottom: 40,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 42,
    fontWeight: 'bold',
    color: '#4CAF50',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
  },
  form: {
    backgroundColor: '#fff',
    margin: 20,
    padding: 20,
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    fontSize: 16,
    backgroundColor: '#fafafa',
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderWidth: 2,
    borderColor: '#4CAF50',
    borderRadius: 6,
    marginRight: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxChecked: {
    backgroundColor: '#4CAF50',
  },
  checkmark: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  checkboxLabel: {
    fontSize: 16,
    color: '#333',
  },
  householdsContainer: {
    marginBottom: 20,
  },
  householdsTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    marginBottom: 10,
  },
  householdItem: {
    padding: 12,
    backgroundColor: '#f0f0f0',
    borderRadius: 8,
    marginBottom: 8,
  },
  householdText: {
    fontSize: 14,
    color: '#333',
  },
  button: {
    backgroundColor: '#4CAF50',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 12,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  secondaryButton: {
    backgroundColor: '#fff',
    borderWidth: 2,
    borderColor: '#4CAF50',
  },
  secondaryButtonText: {
    color: '#4CAF50',
    fontSize: 16,
    fontWeight: '600',
  },
  instructionBox: {
    backgroundColor: '#E8F5E9',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  instructionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2E7D32',
    marginBottom: 8,
  },
  instructionText: {
    fontSize: 14,
    color: '#1B5E20',
    lineHeight: 20,
  },
});
