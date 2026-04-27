# Home Streak Mobile App - Complete Setup Guide

This guide will help you transform your CLI habit tracker into a mobile application for iOS and Android app stores.

## 📁 Project Structure

```
home-streak/
├── backend/              # FastAPI backend
│   ├── main.py
│   └── requirements.txt
├── mobile/              # React Native mobile app
│   ├── src/
│   │   ├── screens/
│   │   ├── services/
│   │   └── navigation/
│   ├── App.tsx
│   └── package.json
├── classes/             # Existing Python classes
├── services/            # Existing Python services
└── cli.py              # Original CLI (still works!)
```

## 🚀 Part 1: Backend Setup (FastAPI)

### Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

```bash
# From the backend directory
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Step 3: Test the Backend

Open http://localhost:8000/docs in your browser and test the endpoints.

---

## 📱 Part 2: Mobile App Setup (React Native)

### Prerequisites

1. **Node.js** (v18 or higher)
   - Download from https://nodejs.org/

2. **For Android Development:**
   - Android Studio
   - Android SDK (API 33)
   - Java Development Kit (JDK 11 or higher)

3. **For iOS Development (Mac only):**
   - Xcode 14+
   - CocoaPods (`sudo gem install cocoapods`)

### Step 1: Install Mobile Dependencies

```bash
cd mobile
npm install
```

### Step 2: Configure API Endpoint

Edit `mobile/src/services/api.ts` and update the API_BASE_URL:

```typescript
// For Android Emulator
const API_BASE_URL = 'http://10.0.2.2:8000';

// For iOS Simulator
const API_BASE_URL = 'http://localhost:8000';

// For Physical Device (replace with your computer's IP)
const API_BASE_URL = 'http://192.168.1.XXX:8000';
```

### Step 3: Run on Android

```bash
# Start Metro bundler
npm start

# In another terminal, run Android
npm run android
```

### Step 4: Run on iOS (Mac only)

```bash
# Install iOS dependencies
cd ios
pod install
cd ..

# Run iOS
npm run ios
```

---

## 🎨 App Features

### 1. **Login Screen**
- Create or join a household
- New user registration
- View available households

### 2. **Home Screen**
- View all habits (daily/weekly)
- Complete habits with one tap
- See bonus habits highlighted
- Pull to refresh

### 3. **Leaderboard Screen**
- View household rankings
- See top performers with medals
- Real-time point updates

### 4. **Profile Screen**
- View your stats
- See active streaks
- Total points and completions
- Logout functionality

---

## 📦 Building for App Stores

### Android (Google Play Store)

#### 1. Generate Release Keystore

```bash
cd mobile/android/app
keytool -genkeypair -v -storetype PKCS12 -keystore home-streak-release.keystore -alias home-streak -keyalg RSA -keysize 2048 -validity 10000
```

#### 2. Configure Signing

Edit `mobile/android/gradle.properties`:

```properties
MYAPP_RELEASE_STORE_FILE=home-streak-release.keystore
MYAPP_RELEASE_KEY_ALIAS=home-streak
MYAPP_RELEASE_STORE_PASSWORD=YOUR_PASSWORD
MYAPP_RELEASE_KEY_PASSWORD=YOUR_PASSWORD
```

#### 3. Build Release APK

```bash
cd mobile/android
./gradlew assembleRelease
```

The APK will be at: `android/app/build/outputs/apk/release/app-release.apk`

#### 4. Build AAB (for Play Store)

```bash
./gradlew bundleRelease
```

The AAB will be at: `android/app/build/outputs/bundle/release/app-release.aab`

### iOS (Apple App Store)

#### 1. Open Xcode

```bash
cd mobile/ios
open HomeStreakMobile.xcworkspace
```

#### 2. Configure Signing
- Select your project in Xcode
- Go to "Signing & Capabilities"
- Select your Apple Developer Team
- Configure Bundle Identifier (e.g., com.yourname.homestreak)

#### 3. Archive the App
- In Xcode: Product → Archive
- Once archived, click "Distribute App"
- Choose "App Store Connect"
- Follow the upload wizard

---

## 🌐 Backend Deployment Options

### Option 1: Heroku (Free Tier Available)

```bash
# Install Heroku CLI
# Create Procfile in backend/
echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > backend/Procfile

# Deploy
cd backend
heroku create home-streak-api
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### Option 2: Railway.app (Recommended)

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway will auto-detect Python and deploy
5. Get your deployment URL

### Option 3: AWS EC2

1. Launch an EC2 instance (Ubuntu)
2. SSH into the instance
3. Install Python and dependencies
4. Run the FastAPI server with systemd

### Option 4: DigitalOcean App Platform

1. Create a new app on DigitalOcean
2. Connect your GitHub repository
3. Configure build settings
4. Deploy

---

## 🔧 Configuration for Production

### Update Mobile API URL

After deploying your backend, update `mobile/src/services/api.ts`:

```typescript
const API_BASE_URL = 'https://your-backend-url.herokuapp.com';
```

### Environment Variables

Create `mobile/.env`:

```
API_URL=https://your-backend-url.com
```

Install dotenv:
```bash
npm install react-native-dotenv
```

---

## 📝 App Store Submission Checklist

### Google Play Store

- [ ] Create Google Play Developer account ($25 one-time fee)
- [ ] Prepare app icon (512x512 PNG)
- [ ] Create screenshots (phone, tablet)
- [ ] Write app description
- [ ] Set up privacy policy
- [ ] Build signed AAB
- [ ] Upload to Play Console
- [ ] Fill out content rating questionnaire
- [ ] Submit for review

### Apple App Store

- [ ] Create Apple Developer account ($99/year)
- [ ] Prepare app icon (1024x1024 PNG)
- [ ] Create screenshots for all device sizes
- [ ] Write app description
- [ ] Set up privacy policy
- [ ] Archive and upload via Xcode
- [ ] Fill out App Store Connect information
- [ ] Submit for review

---

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill
```

**Module not found:**
```bash
pip install -r requirements.txt
```

### Mobile Issues

**Metro bundler issues:**
```bash
npm start -- --reset-cache
```

**Android build fails:**
```bash
cd android
./gradlew clean
cd ..
npm run android
```

**iOS build fails:**
```bash
cd ios
pod deintegrate
pod install
cd ..
npm run ios
```

**Cannot connect to backend:**
- Check firewall settings
- Verify API_BASE_URL in api.ts
- Ensure backend is running
- For physical devices, use your computer's IP address

---

## 🎯 Next Steps

1. **Test thoroughly** on both iOS and Android
2. **Add features**:
   - Push notifications for habit reminders
   - Dark mode support
   - Social sharing
   - Habit analytics charts
3. **Optimize performance**
4. **Gather beta tester feedback**
5. **Submit to app stores**

---

## 📚 Additional Resources

- [React Native Documentation](https://reactnative.dev/docs/getting-started)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Play Console](https://play.google.com/console)
- [App Store Connect](https://appstoreconnect.apple.com/)

---

## 💡 Tips

- **Start with Android** - easier approval process
- **Test on real devices** - simulators don't catch everything
- **Use TestFlight** (iOS) and Internal Testing (Android) for beta testing
- **Monitor backend costs** - consider usage limits
- **Keep your CLI version** - useful for admin tasks

---

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review error logs
3. Test API endpoints in Swagger UI
4. Verify all dependencies are installed

Good luck with your mobile app! 🚀
