"""
Transcription Module
Converts audio to text using OpenAI's Whisper model
Runs locally - no API calls, completely free!
"""

import whisper
import numpy as np
from loguru import logger
import sys
from pathlib import Path
from typing import Dict, Optional
import torch

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from config import WHISPER_CONFIG, MODELS_DIR

class Transcriber:
    """
    Handles speech-to-text conversion using Whisper AI
    
    Whisper is an automatic speech recognition (ASR) model by OpenAI
    that can transcribe audio with high accuracy.
    
    Model sizes available:
    - tiny: 39M params, ~1GB RAM, fastest (we won't use - less accurate)
    - base: 74M params, ~1GB RAM, good balance ← WE USE THIS
    - small: 244M params, ~2GB RAM, better accuracy
    - medium: 769M params, ~5GB RAM, very accurate
    - large: 1550M params, ~10GB RAM, best accuracy
    
    We use 'base' because:
    - Fits easily in 8GB RAM
    - Fast enough for real-time (~1-2s for 10s audio)
    - 95%+ accuracy for clear English speech
    - Free and runs offline
    
    Example Usage:
        transcriber = Transcriber()
        transcriber.load_model()
        result = transcriber.transcribe(audio_data)
        print(result["text"])  # "Hello, how are you?"
    """
    
    def __init__(self):
        """Initialize transcriber"""
        self.model = None
        self.model_loaded = False
        self.model_name = WHISPER_CONFIG["model_name"]
        self.language = WHISPER_CONFIG["language"]
        self.device = WHISPER_CONFIG["device"]
        
        logger.info(f"Transcriber initialized (model: {self.model_name})")
    
    def load_model(self) -> bool:
        """
        Loads Whisper model into memory
        
        First time: Downloads model from internet (~74MB for 'base')
        After that: Loads from disk (models/ folder)
        
        Returns:
            True if successful, False otherwise
        
        What happens during loading:
        1. Checks if model already downloaded
        2. If not, downloads from Hugging Face
        3. Loads model into RAM
        4. Prepares for transcription
        
        Time: ~10 seconds first time, ~2 seconds after
        """
        try:
            logger.info(f"Loading Whisper model: {self.model_name}")
            logger.info(f"Device: {self.device}")
            
            # Check if CUDA (GPU) is available
            if self.device == "cuda" and not torch.cuda.is_available():
                logger.warning("CUDA requested but not available, falling back to CPU")
                self.device = "cpu"
            
            # Download/load model
            # First time: downloads to models/ folder
            # Subsequent times: loads from models/ folder
            self.model = whisper.load_model(
                self.model_name,
                device=self.device,
                download_root=str(MODELS_DIR)
            )
            
            self.model_loaded = True
            logger.success(f"✅ Whisper model '{self.model_name}' loaded successfully!")
            logger.info(f"Model stored in: {MODELS_DIR}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load Whisper model: {e}")
            logger.info("💡 Tip: Check your internet connection (needed for first download)")
            return False
    
    def transcribe(self, audio_data: np.ndarray, language: Optional[str] = None) -> Dict:
        """
        Converts audio to text
        
        Args:
            audio_data: NumPy array of audio samples (float32, -1.0 to 1.0)
            language: Language code (en, hi, es, fr, etc.) - None = auto-detect
        
        Returns:
            Dictionary with transcription results:
            {
                "text": "The transcribed text",
                "language": "en",
                "confidence": 0.95,
                "segments": [...],  # Word-level timing info
            }
        
        How Whisper works:
        1. Takes audio samples
        2. Converts to mel spectrogram (visual representation of sound)
        3. Runs through neural network
        4. Outputs text with timing information
        5. Calculates confidence scores
        
        Time: ~1-2 seconds for 10 seconds of audio (on CPU)
        """
        if not self.model_loaded:
            logger.warning("Model not loaded. Loading now...")
            if not self.load_model():
                return {"text": "", "confidence": 0.0, "error": "Model load failed"}
        
        try:
            # Validate audio data
            if audio_data is None or len(audio_data) == 0:
                logger.error("Empty audio data provided")
                return {"text": "", "confidence": 0.0, "error": "Empty audio"}
            
            # Ensure audio is float32
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Normalize audio to [-1, 1] range (Whisper requirement)
            if np.abs(audio_data).max() > 1.0:
                audio_data = audio_data / np.abs(audio_data).max()
                logger.debug("Audio normalized to [-1, 1] range")
            
            # Use provided language or default from config
            transcribe_language = language or self.language
            
            # Transcribe using Whisper
            logger.debug(f"Transcribing {len(audio_data)} samples...")
            
            result = self.model.transcribe(
                audio_data,
                language=transcribe_language,
                fp16=False,  # Use float32 (required for CPU)
                verbose=False,  # Don't print progress
                task="transcribe"  # 'transcribe' or 'translate'
            )
            
            # Extract transcribed text
            transcribed_text = result["text"].strip()
            
            # Calculate confidence (average of segment probabilities)
            confidence = self._calculate_confidence(result)
            
            # Detected language (if auto-detect was used)
            detected_language = result.get("language", transcribe_language)
            
            logger.debug(f"Transcribed: '{transcribed_text}' (confidence: {confidence:.2f})")
            
            # Return structured result
            return {
                "text": transcribed_text,
                "language": detected_language,
                "confidence": confidence,
                "segments": result.get("segments", []),
                "duration": len(audio_data) / 16000,  # Duration in seconds
            }
            
        except Exception as e:
            logger.error(f"❌ Transcription failed: {e}")
            return {
                "text": "",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _calculate_confidence(self, result: Dict) -> float:
        """
        Calculates overall confidence score from Whisper result
        
        Args:
            result: Raw Whisper output dictionary
        
        Returns:
            Confidence score between 0.0 and 1.0
        
        How it works:
        - Whisper provides log probabilities for each word segment
        - We convert log probs to regular probabilities
        - Average them to get overall confidence
        
        Confidence levels:
        - 0.9+: Very high (clear speech)
        - 0.7-0.9: Good (some background noise)
        - 0.5-0.7: Fair (noisy audio)
        - <0.5: Poor (very noisy or unclear)
        """
        if "segments" not in result or not result["segments"]:
            return 0.5  # Default confidence if no segments
        
        confidences = []
        for segment in result["segments"]:
            if "avg_logprob" in segment:
                # Convert log probability to regular probability
                # log_prob is negative (e.g., -0.5)
                # exp(-0.5) ≈ 0.61 (61% confidence)
                prob = np.exp(segment["avg_logprob"])
                confidences.append(prob)
        
        if confidences:
            return float(np.mean(confidences))
        return 0.5
    
    def transcribe_file(self, audio_file_path: str, language: Optional[str] = None) -> Dict:
        """
        Transcribes audio from a file (WAV, MP3, etc.)
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (optional)
        
        Returns:
            Dictionary with transcription results
        
        Supported formats: WAV, MP3, M4A, FLAC, OGG
        
        Useful for:
        - Testing with pre-recorded audio
        - Batch processing audio files
        - Transcribing saved meetings
        """
        if not self.model_loaded:
            logger.warning("Model not loaded. Loading now...")
            if not self.load_model():
                return {"text": "", "confidence": 0.0, "error": "Model load failed"}
        
        try:
            logger.info(f"Transcribing file: {audio_file_path}")
            
            # Whisper can handle files directly
            result = self.model.transcribe(
                audio_file_path,
                language=language or self.language,
                fp16=False,
                verbose=False
            )
            
            transcribed_text = result["text"].strip()
            confidence = self._calculate_confidence(result)
            
            logger.success(f"✅ File transcribed: {len(transcribed_text)} characters")
            
            return {
                "text": transcribed_text,
                "language": result.get("language", language or self.language),
                "confidence": confidence,
                "segments": result.get("segments", []),
            }
            
        except Exception as e:
            logger.error(f"❌ File transcription failed: {e}")
            return {
                "text": "",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def get_supported_languages(self) -> list:
        """
        Returns list of languages supported by Whisper
        
        Returns:
            List of language codes: ['en', 'hi', 'es', 'fr', ...]
        
        Whisper supports 99 languages including:
        - English (en)
        - Hindi (hi)
        - Spanish (es)
        - French (fr)
        - German (de)
        - Chinese (zh)
        - Japanese (ja)
        - Korean (ko)
        - Arabic (ar)
        - Russian (ru)
        - Portuguese (pt)
        - And 88 more!
        """
        return list(whisper.tokenizer.LANGUAGES.keys())
    
    def get_model_info(self) -> Dict:
        """
        Returns information about the loaded model
        
        Returns:
            Dictionary with model details:
            {
                "name": "base",
                "loaded": True,
                "device": "cpu",
                "parameters": "74M",
                "languages": 99
            }
        """
        return {
            "name": self.model_name,
            "loaded": self.model_loaded,
            "device": self.device,
            "language": self.language,
            "supported_languages": len(self.get_supported_languages())
        }


# ============================================
# STANDALONE TEST CODE
# ============================================
if __name__ == "__main__":
    """
    Run this file directly to test transcription:
    python modules/transcription.py
    
    What it does:
    1. Loads Whisper model
    2. Creates 3 seconds of test audio (beep sound)
    3. Transcribes it
    4. Shows results
    """
    from loguru import logger
    
    logger.info("=" * 60)
    logger.info("TRANSCRIPTION MODULE TEST")
    logger.info("=" * 60)
    
    # Create transcriber instance
    transcriber = Transcriber()
    
    # Load model
    logger.info("\n📥 Loading Whisper model...")
    if not transcriber.load_model():
        logger.error("Failed to load model. Exiting.")
        exit(1)
    
    logger.success("✅ Model loaded successfully!")
    
    # Show model info
    info = transcriber.get_model_info()
    logger.info(f"\n📊 Model Information:")
    logger.info(f"   Name: {info['name']}")
    logger.info(f"   Device: {info['device']}")
    logger.info(f"   Supported languages: {info['supported_languages']}")
    
    # Test with sample audio (silence - just for testing)
    logger.info("\n🎤 Testing transcription with sample audio...")
    logger.info("   (Note: This is just testing the module works)")
    logger.info("   (For real test, use actual meeting audio)")
    
    # Create 3 seconds of silent audio (just for testing)
    sample_audio = np.zeros(16000 * 3, dtype=np.float32)
    
    result = transcriber.transcribe(sample_audio)
    
    if "error" in result:
        logger.error(f"❌ Transcription failed: {result['error']}")
    else:
        logger.success("✅ Transcription successful!")
        logger.info(f"   Text: '{result['text']}'")
        logger.info(f"   Language: {result['language']}")
        logger.info(f"   Confidence: {result['confidence']:.2f}")
        logger.info(f"   Duration: {result['duration']:.1f}s")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ Transcription module is ready!")
    logger.info("=" * 60)