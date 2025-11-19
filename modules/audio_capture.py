"""
Audio Capture Module
Captures live system audio (what you hear in meetings)
Uses loopback recording - no bot appears in meeting!
"""

import soundcard as sc
import numpy as np
from loguru import logger
import time
import sys
from pathlib import Path
from typing import Optional, List, Dict
sys.path.append(str(Path(__file__).parent.parent))
from config import AUDIO_CONFIG

class AudioCapture:
    """
    Captures audio from system output (speakers/headphones)
    
    How it works:
    1. Gets your default speaker/output device
    2. Enables "loopback" mode (captures what's playing)
    3. Records in chunks (e.g., 10 seconds at a time)
    4. Returns audio data for transcription
    
    Example Usage:
        capture = AudioCapture()
        capture.start_capture()
        audio_chunk = capture.capture_chunk(duration=10)
        capture.stop_capture()
    """
    
    def __init__(self):
        """Initialize audio capture system"""
        self.sample_rate = AUDIO_CONFIG["sample_rate"]  # 16000 Hz (Whisper requirement)
        self.channels = AUDIO_CONFIG["channels"]         # 1 (mono)
        self.chunk_duration = AUDIO_CONFIG["chunk_duration"]  # 10 seconds
        
        self.is_recording = False
        self.microphone = None
        self.selected_device = None
        
        logger.info("AudioCapture initialized")
    
    def list_audio_devices(self) -> List[Dict]:
        """
        Lists all available audio output devices
        
        Returns:
            List of dictionaries with device info:
            [
                {"id": 0, "name": "Speakers (Realtek)", "channels": 2},
                {"id": 1, "name": "Headphones", "channels": 2}
            ]
        
        Why this is needed:
        - Users might have multiple audio outputs (speakers, headphones, etc.)
        - We need to capture from the one they're using for meetings
        """
        try:
            speakers = sc.all_speakers()
            logger.info(f"Found {len(speakers)} audio output devices")
            
            devices = []
            for i, speaker in enumerate(speakers):
                device_info = {
                    "id": i,
                    "name": speaker.name,
                    "channels": speaker.channels,
                    "is_default": (speaker.name == sc.default_speaker().name)
                }
                devices.append(device_info)
                logger.debug(f"Device {i}: {speaker.name} (Channels: {speaker.channels})")
            
            return devices
            
        except Exception as e:
            logger.error(f"Failed to list audio devices: {e}")
            return []
    
    def start_capture(self, device_id: Optional[int] = None) -> bool:
        """
        Starts capturing audio from selected device
        
        Args:
            device_id: ID of audio device (None = use default)
        
        Returns:
            True if successful, False otherwise
        
        How loopback works:
        - Normal mic: Captures INPUT (your voice going IN)
        - Loopback: Captures OUTPUT (sound coming OUT to speakers)
        - This way we capture ALL meeting participants' voices!
        """
        try:
            # Step 1: Get the speaker device
            if device_id is None:
                # Use default speaker
                speaker = sc.default_speaker()
                logger.info(f"Using default speaker: {speaker.name}")
            else:
                # Use user-selected speaker
                speakers = sc.all_speakers()
                if device_id >= len(speakers):
                    logger.error(f"Invalid device ID: {device_id}")
                    return False
                speaker = speakers[device_id]
                logger.info(f"Using selected speaker: {speaker.name}")
            
            self.selected_device = speaker
            
            # Step 2: Create microphone with LOOPBACK enabled
            # This is the MAGIC LINE that captures speaker output!
            self.microphone = sc.get_microphone(
                id=str(speaker.name),
                include_loopback=True  # ← KEY: Captures output instead of input
            )
            
            self.is_recording = True
            logger.success("✅ Audio capture started successfully")
            logger.info(f"Sample rate: {self.sample_rate} Hz, Channels: {self.channels}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start audio capture: {e}")
            logger.info("💡 Tip: Make sure you have audio playing or are in a meeting")
            return False
    
    def capture_chunk(self, duration_seconds: Optional[int] = None) -> Optional[np.ndarray]:
        """
        Captures a chunk of audio
        
        Args:
            duration_seconds: How long to record (default: from config)
        
        Returns:
            NumPy array of audio samples, or None if failed
        
        Audio data format:
        - Type: float32 array
        - Range: -1.0 to 1.0 (normalized)
        - Shape: (num_samples,) for mono
        - Example: 10 seconds at 16kHz = 160,000 samples
        
        This function is called repeatedly in a loop:
        while meeting_active:
            audio = capture_chunk(10)  # Get 10 seconds
            transcribe(audio)           # Convert to text
            check_keywords(text)        # Check if relevant
        """
        if not self.is_recording:
            logger.warning("⚠️  Audio capture not started. Call start_capture() first")
            return None
        
        if duration_seconds is None:
            duration_seconds = self.chunk_duration
        
        try:
            # Calculate how many samples we need
            # Example: 10 seconds × 16000 Hz = 160,000 samples
            num_frames = self.sample_rate * duration_seconds
            
            # Record audio
            with self.microphone.recorder(samplerate=self.sample_rate) as recorder:
                logger.debug(f"🎙️  Recording {duration_seconds}s audio chunk...")
                
                # This blocks for `duration_seconds` and returns audio data
                audio_data = recorder.record(numframes=num_frames)
                
                # Convert stereo to mono if needed
                if len(audio_data.shape) > 1 and audio_data.shape[1] > 1:
                    # Average left and right channels
                    audio_data = np.mean(audio_data, axis=1)
                    logger.debug("Converted stereo → mono")
                
                # Ensure correct data type
                if audio_data.dtype != np.float32:
                    audio_data = audio_data.astype(np.float32)
                
                # Check if audio is silent (all zeros = no meeting audio)
                if np.abs(audio_data).max() < 0.001:
                    logger.warning("⚠️  Captured audio is silent. Is meeting audio playing?")
                
                logger.debug(f"✅ Captured {len(audio_data)} samples ({duration_seconds}s)")
                return audio_data
                
        except Exception as e:
            logger.error(f"❌ Error capturing audio chunk: {e}")
            return None
    
    def stop_capture(self):
        """
        Stops audio recording
        
        Call this when:
        - Meeting ends
        - User clicks "Stop" button
        - Application closes
        """
        self.is_recording = False
        self.microphone = None
        logger.info("🛑 Audio capture stopped")
    
    def get_status(self) -> Dict:
        """
        Returns current recording status
        
        Returns:
            Dictionary with status info:
            {
                "is_recording": True/False,
                "device_name": "Speakers (Realtek)",
                "sample_rate": 16000,
                "channels": 1
            }
        
        Used by UI to show recording status
        """
        return {
            "is_recording": self.is_recording,
            "device_name": self.selected_device.name if self.selected_device else None,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "chunk_duration": self.chunk_duration
        }
    
    def test_audio_capture(self, duration: int = 5) -> bool:
        """
        Tests audio capture with a short recording
        
        Args:
            duration: Test duration in seconds
        
        Returns:
            True if test successful, False otherwise
        
        Use this to verify audio capture works before starting meeting
        """
        logger.info(f"🧪 Testing audio capture for {duration} seconds...")
        
        if not self.start_capture():
            return False
        
        try:
            audio = self.capture_chunk(duration)
            
            if audio is None:
                logger.error("❌ Test failed: No audio captured")
                return False
            
            if np.abs(audio).max() < 0.001:
                logger.warning("⚠️  Test captured silent audio. Play some audio and try again.")
                return False
            
            logger.success(f"✅ Test successful! Captured {len(audio)} samples")
            logger.info(f"Audio level: {np.abs(audio).max():.4f} (max amplitude)")
            return True
            
        finally:
            self.stop_capture()


# ============================================
# STANDALONE TEST CODE
# ============================================
if __name__ == "__main__":
    """
    Run this file directly to test audio capture:
    python modules/audio_capture.py
    
    What it does:
    1. Lists all audio devices
    2. Captures 5 seconds of audio
    3. Shows audio statistics
    """
    from loguru import logger
    
    logger.info("=" * 60)
    logger.info("AUDIO CAPTURE TEST")
    logger.info("=" * 60)
    
    # Create capture instance
    capture = AudioCapture()
    
    # List available devices
    logger.info("\n📋 Available Audio Devices:")
    devices = capture.list_audio_devices()
    for device in devices:
        default_marker = " (DEFAULT)" if device["is_default"] else ""
        logger.info(f"  {device['id']}: {device['name']}{default_marker}")
    
    # Test capture
    logger.info("\n🎙️  Starting 5-second test capture...")
    logger.info("💡 IMPORTANT: Play some audio (YouTube video, music, etc.) now!")
    time.sleep(2)  # Give user time to start audio
    
    success = capture.test_audio_capture(duration=5)
    
    if success:
        logger.success("\n✅ Audio capture is working correctly!")
    else:
        logger.error("\n❌ Audio capture test failed. Check the tips above.")