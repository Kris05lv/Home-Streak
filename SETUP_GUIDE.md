# 🚀 Home Streak - Complete Setup Guide

Transform your CLI habit tracker into a modern mobile app!

## 📱 What You're Building

A production-ready mobile app with:
- ✅ Expo SDK 54 + React Native 0.81
- ✅ TypeScript 5.9
- ✅ Zustand state management
- ✅ React Navigation 7
- ✅ RevenueCat monetization
- ✅ Sentry error tracking
- ✅ EAS build system

## 🎯 Quick Start (5 Minutes)

### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

✅ Backend running at http://localhost:8000

### Step 2: Mobile App Setup

```bash
# Navigate to mobile directory
cd mobile

# Install dependencies
npm install

# Start Expo
npm start
```

### Step 3: Run on Your Phone

1. Install **Expo Go** app on your phone
2. Scan the QR code from terminal
3. App loads instantly! 🎉

## 📋 Detailed Setup

### Prerequisites

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.11+ (already have it)
- **Expo Go** app on your phone

### Backend Configuration

Your backend is already set up! It uses:
- FastAPI for REST API
- Your existing Python classes and services
- JSON file storage (data.json)

**API Endpoints:**
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/redoc - ReDoc

### Mobile App Configuration

1. **Copy environment file:**
```bash
cd mobile
cp .env.example .env
```

2. **Update `.env` with your settings:**
```env
API_URL=http://10.0.2.2:8000  # For Android emulator
# API_URL=http://localhost:8000  # For iOS simulator
# API_URL=http://YOUR_IP:8000  # For physical device
```

3. **Find your computer's IP (for physical device):**
```bash
# Windows
ipconfig

# Look for "IPv4 Address" under your WiFi adapter
# Example: 192.168.1.100
```

## 🏃 Running the App

### Option 1: Expo Go (Easiest)

```bash
cd mobile
npm start
```

Then:
1. Open Expo Go on your phone
2. Scan the QR code
3. Done! 🎉

### Option 2: Android Emulator

```bash
npm run android
```

Requires Android Studio installed.

### Option 3: iOS Simulator (Mac only)

```bash
npm run ios
```

Requires Xcode installed.

### Option 4: Web Browser

```bash
npm run web
```

## 🎨 App Features

### Login Screen
- Create or join households
- New user registration
- View available households

### Home Screen
- View all habits (daily/weekly)
- Complete habits with one tap
- Bonus habits highlighted
- Pull to refresh

### Leaderboard
- Household rankings
- Medal system (🥇🥈🥉)
- Real-time updates

### Profile
- User stats
- Active streaks 🔥
- Total completions
- Logout

## 🔧 Advanced Configuration

### Sentry Error Tracking

1. Create account at https://sentry.io
2. Get your DSN
3. Update `.env`:
```env
SENTRY_DSN=your-sentry-dsn-here
```

### RevenueCat Monetization

1. Create account at https://revenuecat.com
2. Get API keys
3. Update `.env`:
```env
REVENUECAT_IOS_KEY=your-key
REVENUECAT_ANDROID_KEY=your-key
```

## 📦 Building for App Stores

### Setup EAS (Expo Application Services)

```bash
# Install EAS CLI
npm install -g eas-cli

# Login
eas login

# Configure
cd mobile
eas build:configure
```

### Build for Android

```bash
# Development build
eas build --platform android --profile development

# Production build (for Play Store)
eas build --platform android --profile production
```

### Build for iOS

```bash
# Development build
eas build --platform ios --profile development

# Production build (for App Store)
eas build --platform ios --profile production
```

### Submit to Stores

```bash
# Google Play Store
eas submit --platform android

# Apple App Store
eas submit --platform ios
```

## 🐛 Troubleshooting

### "Cannot connect to server"

**Problem:** Mobile app can't reach backend

**Solutions:**
1. Check backend is running (`python main.py`)
2. Verify API_URL in `.env`
3. For Android emulator, use `http://10.0.2.2:8000`
4. For iOS simulator, use `http://localhost:8000`
5. For physical device:
   - Find your computer's IP with `ipconfig`
   - Use `http://YOUR_IP:8000`
   - Ensure phone and computer on same WiFi

### "Module not found" errors

```bash
cd mobile
rm -rf node_modules
npm install
```

### Metro bundler issues

```bash
npm start -- --clear
```

### Backend port already in use

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 📱 Testing on Physical Device

1. **Ensure same WiFi network**
   - Phone and computer must be on same network

2. **Find your IP address**
   ```bash
   ipconfig  # Windows
   ```

3. **Update API URL**
   ```env
   API_URL=http://192.168.1.XXX:8000
   ```

4. **Allow firewall**
   - Windows may block port 8000
   - Add firewall exception if needed

## 🎯 Next Steps

### Immediate
- [x] Backend running
- [x] Mobile app running
- [ ] Test on your phone
- [ ] Create your first household
- [ ] Add habits
- [ ] Complete your first habit!

### Short Term
- [ ] Customize app icon and splash screen
- [ ] Add more habits
- [ ] Invite family members
- [ ] Set up Sentry for error tracking

### Long Term
- [ ] Configure RevenueCat for premium features
- [ ] Build production version
- [ ] Submit to app stores
- [ ] Launch! 🚀

## 📚 Resources

- **Expo Docs:** https://docs.expo.dev/
- **React Navigation:** https://reactnavigation.org/
- **Zustand:** https://github.com/pmndrs/zustand
- **EAS Build:** https://docs.expo.dev/build/introduction/
- **Backend API Docs:** http://localhost:8000/docs

## 💡 Tips

- **Start with Expo Go** - fastest way to test
- **Use physical device** - better than emulators
- **Check backend logs** - helpful for debugging
- **Test API first** - visit http://localhost:8000/docs
- **Keep backend running** - mobile app needs it

## 🆘 Getting Help

1. Check troubleshooting section above
2. Review error messages in terminal
3. Test API at http://localhost:8000/docs
4. Check mobile app logs in Expo

---

**You're all set! Start the backend, run the mobile app, and start tracking habits! 🎉**
