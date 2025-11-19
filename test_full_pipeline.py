"""
Full Pipeline Test: Audio Capture → Transcription
Tests the complete flow from meeting audio to text
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from modules.audio_capture import AudioCapture
from modules.transcription import Transcriber
import time

print("=" * 60)
print("FULL PIPELINE TEST: Audio → Text")
print("=" * 60)

# Step 1: Initialize modules
print("\n📋 Step 1: Initializing modules...")
audio_capture = AudioCapture()
transcriber = Transcriber()

# Step 2: Load transcription model
print("\n📋 Step 2: Loading Whisper model...")
if not transcriber.load_model():
    print("❌ Failed to load model")
    exit(1)
print("✅ Model loaded")

# Step 3: Start audio capture
print("\n📋 Step 3: Starting audio capture...")
if not audio_capture.start_capture():
    print("❌ Failed to start audio capture")
    exit(1)
print("✅ Audio capture started")

# Step 4: Record and transcribe
print("\n📋 Step 4: Recording 10 seconds of audio...")
print("🔊 PLAY AUDIO NOW (YouTube video with TALKING)!")
print("   Waiting 2 seconds for you to start...")
time.sleep(2)

print("🎙️  Recording...")
audio_chunk = audio_capture.capture_chunk(duration_seconds=10)

if audio_chunk is None:
    print("❌ Failed to capture audio")
    audio_capture.stop_capture()
    exit(1)

audio_capture.stop_capture()
print(f"✅ Captured {len(audio_chunk)} samples")

# Check if audio is not silent
max_amplitude = abs(audio_chunk).max()
print(f"   Audio level: {max_amplitude:.4f}")

if max_amplitude < 0.001:
    print("\n⚠️  Audio is SILENT - make sure audio is playing!")
    exit(1)

# Step 5: Transcribe
print("\n📋 Step 5: Transcribing audio to text...")
result = transcriber.transcribe(audio_chunk)

if "error" in result:
    print(f"❌ Transcription failed: {result['error']}")
    exit(1)

# Step 6: Display results
print("\n" + "=" * 60)
print("✅ SUCCESS! FULL PIPELINE WORKING!")
print("=" * 60)
print(f"\n📝 TRANSCRIBED TEXT:")
print(f"   '{result['text']}'")
print(f"\n📊 Details:")
print(f"   Language: {result['language']}")
print(f"   Confidence: {result['confidence']:.2f}")
print(f"   Duration: {result['duration']:.1f}s")
print(f"   Audio samples: {len(audio_chunk)}")

print("\n" + "=" * 60)
print("🎉 COMPLETE! Ready for keyword detection!")
print("=" * 60)