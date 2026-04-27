# Fix Android Build Issues

The Android build is failing because React Native requires a complete native project setup. Here are your options:

## Option A: Use Expo (EASIEST - Recommended)

Expo doesn't require Android Studio or complex setup:

```bash
# 1. Install Expo CLI globally
npm install -g expo-cli

# 2. Create new Expo project
cd "c:\Users\Owner\Documents\Code\coding projects\home streak"
npx create-expo-app home-streak-mobile

# 3. Navigate to new project
cd home-streak-mobile

# 4. Install dependencies
npm install axios @react-navigation/native @react-navigation/bottom-tabs
npx expo install react-native-screens react-native-safe-area-context @react-native-async-storage/async-storage

# 5. Copy your source files
# Copy everything from mobile/src/ to home-streak-mobile/src/
# Copy App.tsx content to App.js

# 6. Start Expo
npx expo start

# 7. Install "Expo Go" on your phone and scan QR code
```

**Benefits:**
- Works immediately without Android Studio
- Test on real phone in seconds
- Easy to build for app stores later with `eas build`

## Option B: Complete React Native CLI Setup (HARDER)

If you want the full React Native setup:

### 1. Install Android Studio
- Download from: https://developer.android.com/studio
- Install Android SDK (API 33)
- Set up environment variables:
  - `ANDROID_HOME` = `C:\Users\YourName\AppData\Local\Android\Sdk`
  - Add to PATH: `%ANDROID_HOME%\platform-tools`
  - Add to PATH: `%ANDROID_HOME%\tools`

### 2. Enable PowerShell Scripts
Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Create Debug Keystore
```bash
# Find Java keytool (usually in Android Studio)
cd "C:\Program Files\Android\Android Studio\jbr\bin"
.\keytool -genkeypair -v -storetype PKCS12 -keystore "c:\Users\Owner\Documents\Code\coding projects\home streak\mobile\android\app\debug.keystore" -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000
```

### 4. Clean and Rebuild
```bash
cd "c:\Users\Owner\Documents\Code\coding projects\home streak\mobile"
cd android
.\gradlew clean
cd ..
npm run android
```

## Option C: Test on Web First

React Native Web lets you test in a browser:

```bash
cd mobile
npm install react-native-web react-dom
npx expo start --web
```

## My Recommendation

**Use Expo (Option A)**. It's:
- ✅ Much faster to set up
- ✅ Easier to maintain
- ✅ Still publishable to app stores
- ✅ Better developer experience
- ✅ Works on your phone immediately

The full React Native CLI setup requires:
- Android Studio (several GB download)
- Java JDK configuration
- Environment variables
- Gradle setup
- SDK management

Unless you specifically need native modules that Expo doesn't support, Expo is the better choice for your habit tracker app.

## Quick Start with Expo (5 minutes)

```bash
# Create Expo app
npx create-expo-app HomeStreakApp
cd HomeStreakApp

# Install deps
npm install axios @react-navigation/native @react-navigation/bottom-tabs
npx expo install react-native-screens react-native-safe-area-context @react-native-async-storage/async-storage

# Start
npx expo start

# Scan QR code with Expo Go app on your phone
```

Then just copy your screens and services into the new project!
