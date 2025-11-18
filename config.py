"""
Configuration file for MeetingGuardian
Contains all settings and constants used across the application
"""

import os
from pathlib import Path

# ============================================
# PROJECT PATHS
# ============================================
BASE_DIR = Path(__file__).parent.absolute()
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
TESTS_DIR = BASE_DIR / "tests"

# Create directories if they don't exist
for dir_path in [MODELS_DIR, DATA_DIR, ASSETS_DIR, DATA_DIR / "meeting_history"]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ============================================
# AUDIO SETTINGS
# ============================================
AUDIO_CONFIG = {
    "sample_rate": 16000,           # 16kHz (required by Whisper)
    "channels": 1,                  # Mono audio
    "chunk_duration": 10,           # Process every 10 seconds
    "buffer_size": 1024,            # Audio buffer size
    "dtype": "float32",             # Audio data type
}

# ============================================
# WHISPER MODEL SETTINGS
# ============================================
WHISPER_CONFIG = {
    "model_name": "base",           # Options: tiny, base, small, medium, large
                                    # base = 74MB, good accuracy, fast
    "language": "en",               # English (change for other languages)
    "device": "cpu",                # Use "cuda" if GPU available
    "fp16": False,                  # Use float16 (only for GPU)
}

# ============================================
# SEMANTIC MATCHING SETTINGS
# ============================================
SEMANTIC_CONFIG = {
    "model_name": "all-MiniLM-L6-v2",   # Sentence-BERT model (420MB)
    "similarity_threshold": 0.70,        # 70% match = relevant
    "urgent_threshold": 0.85,            # 85% match = urgent alert
}

# ============================================
# NOTIFICATION SETTINGS
# ============================================
NOTIFICATION_CONFIG = {
    "enable_windows_popup": True,        # Desktop notifications
    "enable_in_app": True,               # Streamlit alerts
    "sound_enabled": True,               # Play sound on alert
    "urgent_sound_enabled": True,        # Different sound for urgent
    "cooldown_seconds": 30,              # Wait 30s between similar alerts
    "max_notifications_per_minute": 3,   # Prevent spam
}

# ============================================
# ROLE TEMPLATES (Auto-suggest keywords)
# ============================================
ROLE_TEMPLATES = {
    "AI Engineer": [
        # Core AI/ML Terms
        "machine learning", "deep learning", "artificial intelligence",
        "neural network", "model training", "model deployment",
        
        # Frameworks
        "tensorflow", "pytorch", "keras", "scikit-learn",
        "hugging face", "transformers",
        
        # Techniques
        "supervised learning", "unsupervised learning",
        "reinforcement learning", "transfer learning",
        "computer vision", "natural language processing", "NLP",
        
        # Model Types
        "CNN", "RNN", "LSTM", "GRU", "transformer", "BERT", "GPT",
        "autoencoder", "GAN", "VAE",
        
        # ML Operations
        "data pipeline", "feature engineering", "hyperparameter tuning",
        "cross validation", "overfitting", "underfitting",
        "accuracy", "precision", "recall", "F1 score", "loss function",
        
        # Deployment
        "model serving", "inference", "optimization", "quantization",
        "ONNX", "TensorRT", "API deployment", "MLOps"
    ],
    
    "Data Scientist": [
        # Analysis
        "data analysis", "exploratory data analysis", "EDA",
        "statistical analysis", "hypothesis testing",
        "A/B testing", "regression analysis",
        
        # Statistics
        "probability", "distribution", "correlation", "causation",
        "p-value", "confidence interval", "significance",
        
        # Tools
        "pandas", "numpy", "matplotlib", "seaborn", "plotly",
        "SQL", "database", "ETL", "data warehouse",
        
        # Techniques
        "data cleaning", "data wrangling", "missing values",
        "outlier detection", "feature selection", "dimensionality reduction",
        "clustering", "classification", "regression", "time series"
    ],
    
    "Software Engineer": [
        # Development
        "API", "REST API", "GraphQL", "backend", "frontend",
        "full stack", "microservices", "monolith",
        
        # Languages/Frameworks
        "Python", "JavaScript", "Java", "C++", "Go", "Rust",
        "React", "Node.js", "Django", "Flask", "FastAPI",
        
        # DevOps
        "CI/CD", "continuous integration", "continuous deployment",
        "Git", "version control", "Docker", "Kubernetes",
        "AWS", "Azure", "GCP", "cloud deployment",
        
        # Practices
        "code review", "testing", "unit test", "integration test",
        "debugging", "refactoring", "design patterns",
        "scalability", "performance optimization"
    ],
    
    "Product Manager": [
        # Planning
        "roadmap", "product roadmap", "sprint planning",
        "backlog", "user story", "requirements", "specification",
        
        # Metrics
        "KPI", "metrics", "analytics", "user engagement",
        "retention", "churn", "conversion rate", "funnel",
        
        # Process
        "agile", "scrum", "kanban", "sprint", "iteration",
        "stakeholder", "user research", "user feedback",
        
        # Strategy
        "feature prioritization", "MVP", "minimum viable product",
        "go-to-market", "product strategy", "competitive analysis"
    ],
    
    "Designer": [
        # Design
        "UI", "UX", "user interface", "user experience",
        "wireframe", "mockup", "prototype", "design system",
        
        # Tools
        "Figma", "Sketch", "Adobe XD", "Photoshop", "Illustrator",
        
        # Concepts
        "user flow", "information architecture", "interaction design",
        "visual design", "accessibility", "responsive design",
        "design thinking", "usability testing"
    ],
    
    "Marketing": [
        "campaign", "branding", "content strategy",
        "SEO", "social media", "email marketing",
        "analytics", "conversion", "lead generation",
        "customer acquisition", "growth hacking"
    ],
    
    "Finance": [
        "budget", "financial planning", "forecasting",
        "revenue", "expenses", "profit", "loss",
        "ROI", "return on investment", "cash flow",
        "financial model", "valuation"
    ]
}

# ============================================
# FILE PATHS
# ============================================
USER_PROFILE_PATH = DATA_DIR / "user_profile.json"
ROLE_TEMPLATES_PATH = DATA_DIR / "role_templates.json"
NOTIFICATION_SOUND_PATH = ASSETS_DIR / "notification_sound.wav"

# ============================================
# LOGGING CONFIGURATION
# ============================================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = BASE_DIR / "meetingguardian.log"
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"

# ============================================
# STREAMLIT UI SETTINGS
# ============================================
UI_CONFIG = {
    "page_title": "MeetingGuardian Pro",
    "page_icon": "🎯",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "theme": "dark",  # or "light"
}

# ============================================
# FEATURE FLAGS
# ============================================
FEATURES = {
    "enable_late_join_summary": True,
    "enable_name_detection": True,
    "enable_topic_tracking": True,
    "enable_audio_save": False,  # Set to True if you want to save audio files
    "enable_speaker_diarization": False,  # Future feature (who is speaking)
}

# ============================================
# PERFORMANCE SETTINGS
# ============================================
PERFORMANCE = {
    "max_transcript_length": 10000,  # Characters to keep in memory
    "cleanup_interval": 300,  # Clean old data every 5 minutes
    "auto_save_interval": 60,  # Save data every 1 minute
}

# ============================================
# HELPER FUNCTIONS
# ============================================
def get_role_keywords(role_name):
    """
    Get keywords for a specific role
    
    Args:
        role_name: Name of the role (e.g., "AI Engineer")
    
    Returns:
        List of keywords for that role
    """
    return ROLE_TEMPLATES.get(role_name, [])

def get_all_roles():
    """
    Get list of all available roles
    
    Returns:
        List of role names
    """
    return list(ROLE_TEMPLATES.keys())

# ============================================
# VALIDATION
# ============================================
def validate_config():
    """
    Validates configuration settings
    Returns True if valid, raises ValueError if not
    """
    # Check audio settings
    if AUDIO_CONFIG["sample_rate"] not in [8000, 16000, 22050, 44100, 48000]:
        raise ValueError("Invalid sample rate. Use 16000 for Whisper.")
    
    # Check thresholds
    if not 0 <= SEMANTIC_CONFIG["similarity_threshold"] <= 1:
        raise ValueError("Similarity threshold must be between 0 and 1")
    
    if not 0 <= SEMANTIC_CONFIG["urgent_threshold"] <= 1:
        raise ValueError("Urgent threshold must be between 0 and 1")
    
    # Check Whisper model
    valid_models = ["tiny", "base", "small", "medium", "large"]
    if WHISPER_CONFIG["model_name"] not in valid_models:
        raise ValueError(f"Invalid Whisper model. Choose from: {valid_models}")
    
    return True

# Run validation on import
try:
    validate_config()
except ValueError as e:
    print(f"⚠️  Configuration Error: {e}")