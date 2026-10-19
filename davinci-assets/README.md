# DaVinci Resolve Master Plugin Suite (578 Free Plugins, Effects, DCTLs & Presets)

DaVinci Resolve (Mac / Windows) တွင် အသုံးပြုရန် အလွန်လူကြိုက်များပြီး အသုံးဝင်သော **Free Plugins, Visual Effects, Text Animations, DCTL Color Science နှင့် LUTs စုစုပေါင်း ၅၇၈ မျိုး** ကို အမျိုးအစားအလိုက် စနစ်တကျ ခွဲခြားစုစည်းပေးထားပါသည်။

---

## ၁။ Folder ဖွဲ့စည်းပုံနှင့် ပါဝင်သော ပစ္စည်းများ (Categories)

```
DaVinci plugin/
├── 1. Text Animation Plugins/ (စုစုပေါင်း ၄၃ မျိုး)
│   ├── Kinetic & Pop Animations/        (Bounce, Snap, Stomp, Impact, Slide)
│   ├── Lower Thirds & Callouts/         (Two-Line, Accent Bar, Social Handle, News Ticker)
│   ├── Subtitles & Captions/            (TikTok/Hormozi Word Pop, Typewriter, Highlight)
│   ├── Cinematic & Minimal Titles/      (Tracking Expand, Defocus Blur, A24 Title)
│   └── Glitch & Retro Titles/           (RGB Chromatic Glitch, Neon Flicker, VHS 80s)
│
├── 2. Effect Plugins/ (စုစုပေါင်း ၂၅၉ မျိုး)
│   ├── Abstract & Light Shaders/        (Nebula, Rainbow Slices, Plasma, Particle Glow)
│   ├── Distortion & Glitch Effects/     (Turbulent Displace, Wave Warp, Lens Distortion)
│   ├── Retro CRT & VHS Displays/        (CRT Monitor Sim, Scanlines, Matrix Rain)
│   ├── Audio Reactive & Waveforms/      (Audio Waveform Visualizers, Frequency Ripples)
│   ├── Tunnels & Space Warps/           (Infinite Zoom, Space Warps, Hypnotic Tunnels)
│   └── Overlays & Safe Zones/           (TikTok, Shorts & Reels Safe Zone Guide)
│
└── 3. Color Plugins/ (စုစုပေါင်း ၂၇၆ မျိုး)
    ├── ACES & Color Science DCTLs/      (LMT Color Balance, DNG, HSL, Print Film Emulation)
    ├── Film Emulation & Tone Curve/     (S-Curves, Power Knee, Convolutions, Transfers)
    ├── Hue Saturation & Exposure DCTLs/ (Gamut Compression, Skin Tone Limiter, Saturation)
    ├── Charts & Technical Analysis/     (Macbeth ColorChecker, Linear Ramp, Waveform Bars)
    └── Cinematic LUTs (.cube)/          (Amber, Fade, Neon, Film, Portrait Looks)
```

---

## ၂။ DaVinci Resolve တွင် ထည့်သွင်းအသုံးပြုနည်း (Installation Guide)

### နည်းလမ်း (၁) - Mac တွင် ၁ စက္ကန့်အတွင်း အလိုအလျောက် ထည့်သွင်းခြင်း (Recommended)
ဤ Folder ထဲတွင် ထည့်ပေးထားသော `install_to_davinci.sh` Script ကို Terminal တွင် Run လိုက်ရုံဖြင့် DaVinci Resolve ၏ System Folder များထဲသို့ သက်ဆိုင်ရာနေရာအလိုက် အလိုအလျောက် ကူးယူပေးသွားမည်ဖြစ်ပါသည် -
```bash
bash "/Users/sithu/Desktop/DaVinci plugin/install_to_davinci.sh"
```

---

### နည်းလမ်း (၂) - မိမိကိုယ်တိုင် Manual ကူးယူထည့်သွင်းခြင်း

#### (က) Text Animation Plugins များ ထည့်သွင်းရန် (`.setting` ဖိုင်များ)
* **Mac:** 
  `Finder` ကိုဖွင့်ပြီး `Cmd + Shift + G` နှိပ်ကာ အောက်ပါလမ်းကြောင်းသို့ သွားပါ -
  `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Templates/Edit/Titles`
  *(အဆိုပါ Titles folder ထဲသို့ `1. Text Animation Plugins` ထဲရှိ ဖိုင်များကို ထည့်ပါ)*
* **Windows:**
  `Win + R` နှိပ်ပြီး အောက်ပါလမ်းကြောင်းသို့ သွားပါ -
  `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Templates\Edit\Titles`

#### (ခ) Visual Effect Plugins များ ထည့်သွင်းရန် (`.fuse` ဖိုင်များ)
* **Mac:**
  `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Fuses`
  *(Fuses folder မရှိပါက Folder အသစ်ဆောက်၍ ထည့်နိုင်ပါသည်)*
* **Windows:**
  `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Fuses`

#### (ဂ) Color Grading DCTLs နှင့် LUTs များ ထည့်သွင်းရန် (`.dctl` နှင့် `.cube` ဖိုင်များ)
1. DaVinci Resolve ကို ဖွင့်ပါ။
2. ညာဘက်အောက်ထောင့်ရှိ **Project Settings (ဂီယာပုံစံ Icon)** ကို နှိပ်ပါ။
3. **Color Management** Tab သို့ သွားပါ။
4. **Lookup Tables** အောက်ရှိ **"Open LUT Folder"** ခလုတ်ကို နှိပ်ပါ။
5. ပွင့်လာသော Folder ထဲသို့ `3. Color Plugins` Folder တစ်ခုလုံးကို ကူးထည့်လိုက်ပါ။
6. DaVinci Resolve သို့ ပြန်သွားပြီး **"Update Lists"** ခလုတ်ကို နှိပ်လိုက်ပါက ချက်ချင်း စတင် အသုံးပြုနိုင်ပါပြီ။
