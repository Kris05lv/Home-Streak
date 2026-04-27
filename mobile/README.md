# Home Streak Mobile App

A modern React Native mobile application built with Expo for tracking family habits and competing on a household leaderboard.

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Expo SDK 54 (managed workflow) |
| UI | React Native 0.81 + React 19 |
| Language | TypeScript 5.9 |
| Navigation | React Navigation 7 (stack + bottom tabs) |
| State Management | Zustand 5 |
| Local Storage | AsyncStorage |
| Monetization | RevenueCat (react-native-purchases) |
| Error Tracking | Sentry (@sentry/react-native) |
| Image/Camera | Expo Image Picker, Expo Image Manipulator |
| File & Sharing | Expo File System, Expo Sharing |
| Build/Deploy | EAS (Expo Application Services) |
| Platforms | Android, Web |

## 📋 Prerequisites

- Node.js 18+
- npm or yarn
- Expo CLI
- Android Studio (for Android development)
- Xcode (for iOS development, Mac only)

## 🛠️ Installation

### 1. Install Dependencies

```bash
cd mobile
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Update the following in `.env`:
- `API_URL` - Your backend API URL
- `SENTRY_DSN` - Your Sentry DSN (optional)
- `REVENUECAT_IOS_KEY` - Your RevenueCat iOS key (optional)
- `REVENUECAT_ANDROID_KEY` - Your RevenueCat Android key (optional)

### 3. Update app.json

Update `app.json` with your configuration:
- `expo.extra.eas.projectId` - Your EAS project ID
- `expo.ios.bundleIdentifier` - Your iOS bundle ID
- `expo.android.package` - Your Android package name

## 🏃 Running the App

### Development Mode

```bash
# Start Expo dev server
npm start

# Run on Android
npm run android

# Run on iOS (Mac only)
npm run ios

# Run on Web
npm run web
```

### Using Expo Go

1. Install **Expo Go** on your phone (from Play Store or App Store)
2. Run `npm start`
3. Scan the QR code with your phone
4. App will load instantly!

## 📱 Features

- ✅ **User Authentication** - Login/logout with household support
- 🏠 **Household Management** - Create and join households
- ✅ **Habit Tracking** - Complete daily and weekly habits
- 🏆 **Leaderboard** - Compete with family members
- 🔥 **Streaks** - Track your consistency
- 💎 **Bonus Habits** - First-come, first-served bonus points
- 📊 **Profile Stats** - View your progress and achievements
- 🎨 **Modern UI** - Beautiful, intuitive interface
- 🔄 **Pull to Refresh** - Easy data updates
- 💾 **Offline Support** - Local data persistence

## 🏗️ Project Structure

```
mobile/
├── src/
│   ├── screens/          # App screens
│   │   ├── LoginScreen.tsx
│   │   ├── HomeScreen.tsx
│   │   ├── LeaderboardScreen.tsx
│   │   └── ProfileScreen.tsx
│   ├── navigation/       # Navigation setup
│   │   └── AppNavigator.tsx
│   ├── stores/           # Zustand state management
│   │   ├── authStore.ts
│   │   ├── habitStore.ts
│   │   └── leaderboardStore.ts
│   ├── services/         # API and external services
│   │   ├── api.ts
│   │   ├── sentry.ts
│   │   └── revenuecat.ts
│   └── types/            # TypeScript types
├── App.tsx              # Main app component
├── app.json             # Expo configuration
├── eas.json             # EAS Build configuration
├── tsconfig.json        # TypeScript configuration
└── package.json         # Dependencies

## 🔨 Building for Production

### Using EAS Build

1. **Install EAS CLI**
```bash
npm install -g eas-cli
```

2. **Login to Expo**
```bash
eas login
```

3. **Configure EAS**
```bash
eas build:configure
```

4. **Build for Android**
```bash
npm run build:android
```

5. **Build for iOS**
```bash
npm run build:ios
```

### Build Profiles

- **development** - Development build with debugging
- **preview** - Internal testing build (APK for Android)
- **production** - Production build for app stores (AAB for Android)

## 📦 Submitting to App Stores

### Android (Google Play)

```bash
npm run submit:android
```

### iOS (App Store)

```bash
npm run submit:ios
```

## 🧪 Testing

```bash
# Run tests
npm test

# Type checking
npm run type-check

# Linting
npm run lint
```

## 🐛 Troubleshooting

### Clear Cache
```bash
npm start -- --clear
```

### Reset Metro Bundler
```bash
rm -rf node_modules
npm install
npm start -- --reset-cache
```

### Android Build Issues
```bash
cd android
./gradlew clean
cd ..
```

### iOS Build Issues (Mac only)
```bash
cd ios
pod deintegrate
pod install
cd ..
```

## 🔧 Configuration

### API Endpoint

Update the API URL in `src/services/api.ts`:

```typescript
// For Android Emulator
const API_BASE_URL = 'http://10.0.2.2:8000';

// For iOS Simulator
const API_BASE_URL = 'http://localhost:8000';

// For Physical Device (use your computer's IP)
const API_BASE_URL = 'http://192.168.1.XXX:8000';
```

### Sentry Setup

1. Create a Sentry project at https://sentry.io
2. Add your DSN to `.env`
3. Update `app.json` with your Sentry organization and project

### RevenueCat Setup

1. Create a RevenueCat account at https://www.revenuecat.com
2. Add your API keys to `.env`
3. Configure products in RevenueCat dashboard

## 📚 Documentation

- [Expo Documentation](https://docs.expo.dev/)
- [React Navigation](https://reactnavigation.org/)
- [Zustand](https://github.com/pmndrs/zustand)
- [RevenueCat](https://www.revenuecat.com/docs)
- [Sentry](https://docs.sentry.io/platforms/react-native/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review error logs with `npx expo start`
- Test API endpoints at http://localhost:8000/docs

---

**Happy Habit Tracking! 🎯**
