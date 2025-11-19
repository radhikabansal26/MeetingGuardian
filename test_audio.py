"""
Audio Diagnostic Test
"""
import soundcard as sc
import numpy as np
import time

print("=" * 60)
print("AUDIO DIAGNOSTIC TEST")
print("=" * 60)

# Test 1: List all speakers
print("\n📋 Step 1: Detecting audio devices...")
try:
    speakers = sc.all_speakers()
    print(f"✅ Found {len(speakers)} audio device(s):")
    for i, speaker in enumerate(speakers):
        is_default = "(DEFAULT)" if speaker.name == sc.default_speaker().name else ""
        print(f"   {i}: {speaker.name} {is_default}")
except Exception as e:
    print(f"❌ ERROR detecting devices: {e}")
    exit(1)

# Test 2: Get default speaker
print("\n📋 Step 2: Selecting default speaker...")
try:
    default_speaker = sc.default_speaker()
    print(f"✅ Default speaker: {default_speaker.name}")
except Exception as e:
    print(f"❌ ERROR getting default speaker: {e}")
    exit(1)

# Test 3: Create microphone with loopback
print("\n📋 Step 3: Setting up loopback recording...")
try:
    mic = sc.get_microphone(id=str(default_speaker.name), include_loopback=True)
    print(f"✅ Loopback microphone created")
except Exception as e:
    print(f"❌ ERROR creating loopback: {e}")
    print("\n💡 SOLUTION: Try running VS Code as Administrator")
    exit(1)

# Test 4: Record audio
print("\n📋 Step 4: Recording 5 seconds of audio...")
print("🔊 PLAY AUDIO NOW (YouTube, music, etc.)!")
print("   Waiting 2 seconds for you to start audio...")
time.sleep(2)

try:
    with mic.recorder(samplerate=16000) as recorder:
        print("🎙️  Recording...")
        audio = recorder.record(numframes=16000 * 5)  # 5 seconds
        print(f"✅ Recorded {len(audio)} samples")
        
        # Check if audio is silent
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        
        max_amplitude = np.abs(audio).max()
        print(f"\n📊 Audio Statistics:")
        print(f"   Max amplitude: {max_amplitude:.4f}")
        print(f"   Min amplitude: {np.abs(audio).min():.4f}")
        print(f"   Mean amplitude: {np.abs(audio).mean():.4f}")
        
        if max_amplitude < 0.001:
            print("\n❌ PROBLEM: Audio is SILENT!")
            print("\n💡 SOLUTIONS TO TRY:")
            print("   1. Make sure audio is PLAYING (YouTube/Music)")
            print("   2. Turn UP your volume (50%+)")
            print("   3. Check if audio is MUTED")
            print("   4. Try different speaker/headphones")
            print("   5. Restart your computer")
        else:
            print("\n✅ SUCCESS! Audio captured correctly!")
            print(f"   Audio level is good: {max_amplitude:.4f}")
            
except Exception as e:
    print(f"❌ ERROR during recording: {e}")
    exit(1)

print("\n" + "=" * 60)