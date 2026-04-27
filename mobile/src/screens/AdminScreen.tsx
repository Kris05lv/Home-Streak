import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert,
  FlatList,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useAuthStore } from '../stores/authStore';
import { adminAPI } from '../services/api';

interface Member {
  username: string;
  points: number;
  is_admin: boolean;
}

export default function AdminScreen() {
  const { household } = useAuthStore();
  const [newMemberName, setNewMemberName] = useState('');
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(false);
  const [showPasswordSection, setShowPasswordSection] = useState(false);
  const [newPassword, setNewPassword] = useState('');

  useEffect(() => {
    loadMembers();
  }, []);

  const loadMembers = async () => {
    if (!household) return;
    
    try {
      const memberList = await adminAPI.getMembers(household);
      setMembers(memberList);
    } catch (error) {
      console.error('Error loading members:', error);
    }
  };

  const handleAddMember = async () => {
    if (!newMemberName.trim()) {
      Alert.alert('Error', 'Please enter a member name');
      return;
    }

    if (!household) {
      Alert.alert('Error', 'No household selected');
      return;
    }

    setLoading(true);
    try {
      await adminAPI.addMember(newMemberName, household);
      Alert.alert('Success', `${newMemberName} added to family!`);
      setNewMemberName('');
      await loadMembers();
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to add member');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdatePassword = async () => {
    if (!newPassword.trim()) {
      Alert.alert('Error', 'Please enter a password');
      return;
    }

    if (!household) return;

    setLoading(true);
    try {
      await householdAPI.updatePassword(household, newPassword);
      Alert.alert('Success', 'Family password updated! Share it with your family members.');
      setNewPassword('');
      setShowPasswordSection(false);
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to update password');
    } finally {
      setLoading(false);
    }
  };

  const renderMember = ({ item }: { item: Member }) => (
    <View style={styles.memberCard}>
      <View style={styles.memberInfo}>
        <Text style={styles.memberName}>{item.username}</Text>
        {item.is_admin && (
          <View style={styles.adminBadge}>
            <Text style={styles.adminBadgeText}>Admin</Text>
          </View>
        )}
      </View>
      <Text style={styles.memberPoints}>{item.points} pts</Text>
    </View>
  );

  return (
    <ScrollView style={styles.container}>
      <StatusBar style="light" />
      
      <View style={styles.header}>
        <Text style={styles.title}>👨‍👩‍👧‍👦 Family Admin</Text>
        <Text style={styles.household}>{household}</Text>
      </View>

      <View style={styles.content}>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>🔒 Family Password</Text>
          {!showPasswordSection ? (
            <TouchableOpacity
              style={[styles.button, styles.secondaryButton]}
              onPress={() => setShowPasswordSection(true)}
            >
              <Text style={styles.secondaryButtonText}>Change Password/PIN</Text>
            </TouchableOpacity>
          ) : (
            <>
              <Text style={styles.sectionSubtitle}>
                Set or update the password that family members use to login
              </Text>
              <TextInput
                style={styles.input}
                placeholder="New Password/PIN"
                value={newPassword}
                onChangeText={setNewPassword}
                secureTextEntry
                editable={!loading}
              />
              <View style={styles.buttonRow}>
                <TouchableOpacity
                  style={[styles.button, styles.halfButton]}
                  onPress={handleUpdatePassword}
                  disabled={loading}
                >
                  <Text style={styles.buttonText}>Update</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.button, styles.secondaryButton, styles.halfButton]}
                  onPress={() => {
                    setShowPasswordSection(false);
                    setNewPassword('');
                  }}
                  disabled={loading}
                >
                  <Text style={styles.secondaryButtonText}>Cancel</Text>
                </TouchableOpacity>
              </View>
            </>
          )}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Add Family Member</Text>
          <Text style={styles.sectionSubtitle}>
            Add members who can login on their own devices
          </Text>

          <TextInput
            style={styles.input}
            placeholder="Member name (e.g., Mom, Dad, Sarah)"
            value={newMemberName}
            onChangeText={setNewMemberName}
            autoCapitalize="words"
            editable={!loading}
          />

          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={handleAddMember}
            disabled={loading}
          >
            <Text style={styles.buttonText}>
              {loading ? 'Adding...' : 'Add Member'}
            </Text>
          </TouchableOpacity>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Family Members ({members.length})</Text>
          <Text style={styles.instructionText}>
            💡 Members can login using just their name on any device
          </Text>

          <FlatList
            data={members}
            renderItem={renderMember}
            keyExtractor={(item) => item.username}
            scrollEnabled={false}
            ListEmptyComponent={
              <View style={styles.emptyContainer}>
                <Text style={styles.emptyText}>No members yet</Text>
                <Text style={styles.emptySubtext}>Add your first family member above</Text>
              </View>
            }
          />
        </View>
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
  content: {
    padding: 20,
  },
  section: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  sectionSubtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 16,
  },
  instructionText: {
    fontSize: 14,
    color: '#4CAF50',
    marginBottom: 16,
    fontWeight: '500',
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
  button: {
    backgroundColor: '#4CAF50',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  memberCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#f9f9f9',
    borderRadius: 12,
    marginBottom: 10,
  },
  memberInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  memberName: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
  },
  adminBadge: {
    backgroundColor: '#FFD700',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
    marginLeft: 10,
  },
  adminBadgeText: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#333',
  },
  memberPoints: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyText: {
    fontSize: 16,
    color: '#999',
    marginBottom: 4,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#bbb',
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
  buttonRow: {
    flexDirection: 'row',
    gap: 10,
  },
  halfButton: {
    flex: 1,
  },
});
