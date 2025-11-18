# 🎯 MeetingGuardian 

**AI-Powered Meeting Assistant with Role-Specific Attention Alerts**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 💡 Never miss important discussions in meetings again! MeetingGuardian intelligently monitors meeting conversations in real-time and alerts you when topics relevant to your role are being discussed.

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Demo](#-demo)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 🎯 Problem Statement

### **The Challenge:**

In today's remote work environment, professionals often face:

1. **Back-to-back meetings** with no time to prepare or catch up
2. **Late joins** - Missing crucial context from the first 10-15 minutes
3. **Multi-tasking** - Working on other tasks while in meetings
4. **Information overload** - Hour-long meetings where only 10 minutes are relevant to your role
5. **Missed mentions** - Someone asks you a question but you weren't paying attention

### **Current Solutions Fall Short:**

| Existing Tools | Limitations |
|----------------|-------------|
| **Fathom, Fireflies** | Visible bot in meeting (unprofessional), summaries only AFTER meeting ends |
| **Otter.ai** | No real-time alerts, doesn't understand role-specific relevance |
| **Manual note-taking** | Cognitive load, miss important points, can't multitask |

### **Impact:**

- 😰 **Anxiety** - "Did I miss something important?"
- ⏰ **Time waste** - Attending full meetings when only partially relevant
- 🔇 **Missed opportunities** - Fail to contribute when expertise is needed
- 📉 **Productivity loss** - Can't work on other tasks during irrelevant discussions

---

## ✨ Solution

**MeetingGuardian Pro** is an AI-powered desktop application that:

✅ **Runs invisibly** - No bot appears in participant list  
✅ **Monitors in real-time** - Transcribes and analyzes as meeting happens  
✅ **Understands context** - Uses semantic AI to detect role-relevant topics  
✅ **Alerts instantly** - Desktop notifications when your expertise is needed  
✅ **Provides summaries** - Catch-up brief if you join late  

### **Who Benefits:**

- 👨‍💻 **Software Engineers** - Alerted when code/architecture discussed
- 🤖 **AI/ML Engineers** - Notified when models/deployment mentioned
- 📊 **Data Scientists** - Alerted for data/analytics topics
- 📱 **Product Managers** - Notified for roadmap/feature discussions
- 🎨 **Designers** - Alerted for UI/UX topics

---

## 🚀 Key Features

### **1. 🎤 Invisible Audio Capture**
- Captures meeting audio locally (no bot joins meeting)
- Works with Zoom, Google Meet, Microsoft Teams, any platform
- Privacy-first: Audio processed locally, never uploaded

### **2. 🧠 Smart Keyword Detection**
- **Semantic matching**: Understands "neural network" ≈ "deep learning" ≈ "AI model"
- **Role-based**: Configure keywords for your specific role
- **Auto-suggest**: Pre-configured templates for common roles

### **3. 🔔 Dual Notification System**
- **Desktop alerts**: Windows notifications (works even with app minimized)
- **In-app alerts**: Visual alerts within Streamlit dashboard
- **Urgency levels**: Different alerts for "relevant" vs "urgent" topics

### **4. ⏰ Late-Join Catch-Up**
- Join 15 minutes late? Get instant 30-second summary
- Topic tracking: See what's been discussed so far
- Decision log: Key decisions made before you joined

### **5. 📊 Real-Time Dashboard**
- Live transcript display
- Topic timeline visualization
- Notification history
- Relevance score tracking

### **6. 👤 Name Mention Detection**
- Instantly alerted when your name is mentioned
- Different sound/notification for direct questions
- Context provided: "Alice asked: 'Radhika, what's the timeline?'"

---

## 🛠️ Tech Stack

### **Machine Learning & AI**

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **Whisper (OpenAI)** | Speech-to-text | 95%+ accuracy, works offline, free |
| **Sentence-BERT** | Semantic matching | Understands context, not just keywords |
| **KeyBERT** | Keyword extraction | Identifies main topics in discussion |

### **Backend & Processing**

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core language |
| **NumPy & SciPy** | Audio processing |
| **soundcard** | System audio capture |
| **Pandas** | Data manipulation |

### **Frontend & UI**

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web-based UI (no HTML/CSS needed!) |
| **Plyer** | Cross-platform notifications |

### **Deployment**

| Platform | Use Case |
|----------|----------|
| **Streamlit Cloud** | Free hosting for web app |
| **Hugging Face Spaces** | Alternative deployment (more resources) |

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                      MEETING PLATFORM                       │
│              (Zoom / Google Meet / Teams)                   │
└────────────────────────┬────────────────────────────────────┘
                         │ Audio Output
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   AUDIO CAPTURE MODULE                      │
│            (Loopback capture - no bot visible)              │
└────────────────────────┬────────────────────────────────────┘
                         │ Audio Chunks (10s)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  TRANSCRIPTION MODULE                       │
│              (Whisper AI - Speech to Text)                  │
└────────────────────────┬────────────────────────────────────┘
                         │ Text Transcript
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                KEYWORD DETECTION MODULE                     │
│         (Sentence-BERT + KeyBERT + User Profile)            │
└────────────┬───────────────────────┬────────────────────────┘
             │                       │
             │ Relevant?             │ Not Relevant
             ▼                       ▼
┌──────────────────────┐   ┌──────────────────────┐
│  NOTIFICATION        │   │  Continue            │
│  MANAGER             │   │  Monitoring          │
│  • Desktop Alert     │   └──────────────────────┘
│  • In-App Alert      │
│  • Sound (optional)  │
└──────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                   STREAMLIT DASHBOARD                       │
│  • Live Transcript  • Topic Timeline  • Alert History       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📥 Installation

### **Prerequisites**

- Python 3.10 or 3.11 (not 3.12)
- Windows 10/11, macOS, or Linux
- 8GB RAM minimum
- Internet connection (for first-time model downloads)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/radhikabansal26/MeetingGuardian.git
cd MeetingGuardian
```

### **Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Note:** First installation takes 5-10 minutes (downloads ML models ~500MB)

### **Step 4: Run Application**
```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`

---

## 🎮 Usage

### **First-Time Setup**

1. **Configure Your Role**
   - Select your role (AI Engineer, Data Scientist, etc.)
   - Review auto-suggested keywords
   - Add custom keywords if needed

2. **Select Audio Device**
   - Choose your system audio output (speakers/headphones)
   - Test audio capture with sample recording

3. **Set Notification Preferences**
   - Enable/disable desktop notifications
   - Choose notification sound
   - Set urgency thresholds

### **During Meetings**

1. **Join your meeting** (Zoom/Meet/Teams)
2. **Start MeetingGuardian** (click "Start Monitoring")
3. **Work on other tasks** - App runs in background
4. **Get notified** when relevant topics discussed

### **Example Notification:**
```
┌─────────────────────────────────────────┐
│ 🔔 MeetingGuardian Alert                │
│                                         │
│ ⚠️  RELEVANT TOPIC DETECTED             │
│                                         │
│ "machine learning model deployment"     │
│                                         │
│ Relevance Score: 87%                    │
│ Speaker: Bob                            │
│ Time: 14:23                             │
│                                         │
│ [View Context] [Dismiss]                │
└─────────────────────────────────────────┘
```

---

## 🔬 How It Works

### **1. Audio Capture (No Bot!)**

Unlike Fathom/Fireflies, MeetingGuardian doesn't join as a bot:
```python
# Captures your computer's audio output (what YOU hear)
speaker = sc.default_speaker()
mic = sc.get_microphone(id=speaker.name, include_loopback=True)
audio = mic.record(duration=10)  # 10-second chunks
```

### **2. Real-Time Transcription**
```python
# Whisper AI converts speech to text
model = whisper.load_model("base")
result = model.transcribe(audio)
text = result["text"]  # "Let's discuss the ML model deployment"
```

### **3. Semantic Keyword Matching**
```python
# Not just exact matches - understands meaning!
user_keywords = ["machine learning", "AI", "model"]
meeting_text = "neural network training pipeline"

# Sentence-BERT calculates similarity
similarity = calculate_semantic_similarity(user_keywords, meeting_text)
# Result: 0.89 (89% match!) → Send notification!
```

### **4. Smart Notifications**
```python
if similarity >= 0.85:
    send_notification(urgency="urgent", sound=True)
elif similarity >= 0.70:
    send_notification(urgency="high", sound=False)
# else: continue monitoring
```

---

## 🎥 Demo

### **Live Demo**
🔗 [Try MeetingGuardian](YOUR_DEPLOYMENT_URL_HERE) *(Add after deployment)*

### **Video Walkthrough**
📹 [Watch Demo Video](YOUR_YOUTUBE_LINK_HERE) *(Add on Day 5)*

### **Screenshots**

*Add screenshots here on Day 5 after building UI*

---

## 🚀 Future Enhancements

### **Phase 2 (After Initial Release)**

- [ ] **Speaker Diarization** - Identify who is speaking
- [ ] **Multi-language Support** - Hindi, Spanish, French, etc.
- [ ] **Meeting Analytics** - Weekly reports on meeting time
- [ ] **Integration with Calendar** - Auto-join scheduled meetings
- [ ] **Mobile App** - iOS/Android companion app
- [ ] **Browser Extension** - One-click activation
- [ ] **Team Features** - Share summaries with team members

### **Phase 3 (Advanced)**

- [ ] **Action Item Extraction** - "Radhika to submit report by Friday"
- [ ] **Sentiment Analysis** - Detect meeting mood/tone
- [ ] **Auto-follow-up Emails** - Generate summary emails
- [ ] **CRM Integration** - Sync with Salesforce, HubSpot
- [ ] **Voice Commands** - "MeetingGuardian, summarize last 5 minutes"

---

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Radhika Bansal**

- 📧 Email: radhikabansal405@gmail.com
- 💼 LinkedIn: [https://www.linkedin.com/in/radhika-bansal-0852a42a6/](https://www.linkedin.com/in/radhika-bansal-0852a42a6/) 
- 🐙 GitHub: [@radhikabansal26](https://github.com/radhikabansal26)
- 🎓 University: Noida Institute of Engineering and Technology, Greater Noida
- 🎯 Specialization: Artificial Intelligence

---

## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition
- Sentence-Transformers for semantic matching
- Streamlit for rapid UI development
- The open-source community

---

## ⭐ Show Your Support

If you find this project useful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs via Issues
- 💡 Suggesting features
- 🔀 Contributing code

---

**Built with ❤️ by Radhika Bansal**

*Last Updated: November 2025*