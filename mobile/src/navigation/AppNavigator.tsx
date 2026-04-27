import React, { useState, useEffect, useRef } from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { useNavigation } from '@react-navigation/native';
import HomeScreen from '../screens/HomeScreen';
import LeaderboardScreen from '../screens/LeaderboardScreen';
import ProfileScreen from '../screens/ProfileScreen';
import AdminScreen from '../screens/AdminScreen';
import { useAuthStore } from '../stores/authStore';
import { userAPI } from '../services/api';

const Tab = createBottomTabNavigator();

export default function AppNavigator() {
  const username = useAuthStore((state) => state.username);
  const [isAdmin, setIsAdmin] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAdminStatus();
  }, [username]);

  const checkAdminStatus = async () => {
    if (!username) {
      setIsLoading(false);
      return;
    }
    
    setIsLoading(true);
    try {
      const user = await userAPI.get(username);
      const adminStatus = user.is_admin || false;
      setIsAdmin(adminStatus);
      console.log('Admin status:', adminStatus);
    } catch (error) {
      console.error('Error checking admin status:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return null; // Don't render tabs until we know admin status
  }

  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: '#4CAF50',
        tabBarInactiveTintColor: '#999',
        tabBarStyle: {
          paddingBottom: 8,
          paddingTop: 8,
          height: 60,
          borderTopWidth: 1,
          borderTopColor: '#e0e0e0',
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '600',
        },
      }}
    >
      {isAdmin && (
        <Tab.Screen
          name="Admin"
          component={AdminScreen}
          options={{
            tabBarLabel: 'Family',
            tabBarIcon: ({ color }) => <TabIcon icon="👨‍👩‍👧‍👦" color={color} />,
          }}
        />
      )}
      
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarLabel: 'Habits',
          tabBarIcon: ({ color }) => <TabIcon icon="�" color={color} />,
        }}
      />
      
      <Tab.Screen
        name="Leaderboard"
        component={LeaderboardScreen}
        options={{
          tabBarLabel: 'Leaderboard',
          tabBarIcon: ({ color }) => <TabIcon icon="🏆" color={color} />,
        }}
      />
      
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          tabBarLabel: 'Profile',
          tabBarIcon: ({ color }) => <TabIcon icon="👤" color={color} />,
        }}
      />
    </Tab.Navigator>
  );
}

interface TabIconProps {
  icon: string;
  color: string;
}

function TabIcon({ icon }: TabIconProps) {
  return (
    <span style={{ fontSize: 24 }}>{icon}</span>
  );
}
