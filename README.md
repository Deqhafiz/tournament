# TIKTOP - T-Coin Tournament App

Aplikasi Android untuk tournament T-Coin dengan animasi koin emas yang bergerak seperti Bitcoin.

## Fitur

🪙 **25 T-Coin Creatures** - Koin emas dengan huruf "T" yang bergerak-gerak di skrin
⚡ **Circuit Animation** - Garis laser emas menghubungkan koin yang berdekatan
🎨 **Bitcoin-Style Design** - Warna emas metalik seperti Bitcoin asli
🏆 **Tournament UI** - Interface cantik dengan glass-morphism effect

## Cara Build & Run

### 1. Menggunakan Android Studio
1. Buka Android Studio
2. File > Open > Pilih folder TIKTOP
3. Tunggu Gradle sync selesai
4. Klik Run (▶️) atau tekan Shift+F10
5. Pilih device/emulator anda

### 2. Menggunakan Command Line
```bash
# Build debug APK
./gradlew assembleDebug

# Install ke device yang tersambung
./gradlew installDebug

# Build dan run
./gradlew installDebug && adb shell am start -n com.tiktop.tournament/.TournamentActivity
```

## Struktur File

```
TIKTOP/
├── app/
│   ├── src/main/
│   │   ├── assets/www/
│   │   │   └── tournament.html          # Halaman tournament dengan animasi
│   │   ├── java/com/tiktop/tournament/
│   │   │   └── TournamentActivity.kt    # Activity utama (WebView)
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   └── activity_tournament.xml
│   │   │   └── values/
│   │   │       ├── strings.xml
│   │   │       ├── colors.xml
│   │   │       └── themes.xml
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle
├── settings.gradle
└── gradle.properties
```

## Requirements

- Android SDK 24+ (Android 7.0 Nougat)
- Target SDK: 34 (Android 14)
- Kotlin 1.9.0
- Gradle 8.1.0

## Teknologi

- **Kotlin** - Bahasa programming
- **WebView** - Untuk display HTML dengan JavaScript
- **TailwindCSS** - Framework CSS (via CDN)
- **Canvas API** - Untuk animasi circuit background
- **JavaScript** - Untuk animasi T-Coin creatures

## Preview

Apabila anda run app ini, anda akan nampak:
- Background hitam dengan circuit grid pattern emas
- 25 koin T-Coin emas bergerak-gerak di skrin
- Garis laser emas yang connect koin-koin berdekatan
- Panel tengah dengan info tournament
- Tombol "MULAI SEKARANG" untuk start tournament

## Developer

Created with ❤️ for TIKTOP Tournament System
