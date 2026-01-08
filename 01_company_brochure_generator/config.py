"""Configuration module for the Company Brochure Generator."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the application."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # Model Configuration
    OPENAI_MODEL = "gpt-5-nano"
    GEMINI_MODEL = "gemini-2.5-flash"
    GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
    
    # Available models for user selection
    MODELS = {
        "gpt-5-nano": {
            "provider": "openai",
            "name": "GPT-5 Nano",
            "max_tokens": 16000,
            "supports_streaming": True
        },
        "gemini-2.5-flash": {
            "provider": "gemini",
            "name": "Gemini 2.5 Flash",
            "max_tokens": 32000,
            "supports_streaming": True
        }
    }
    
    # Tone/Style templates
    TONES = {
        "professional": {
            "name": "Professional",
            "description": "Formal and authoritative language suitable for investors and stakeholders"
        },
        "friendly": {
            "name": "Friendly",
            "description": "Warm and approachable tone for general audience"
        },
        "humorous": {
            "name": "Humorous",
            "description": "Witty and entertaining while maintaining professionalism"
        },
        "technical": {
            "name": "Technical",
            "description": "Detailed and precise for technical stakeholders"
        },
        "executive": {
            "name": "Executive",
            "description": "Concise and high-level for C-suite readers"
        }
    }
    
    # Scraper Settings
    MAX_CONTENT_LENGTH = 2000
    MAX_AGGREGATED_CONTENT = 5000
    REQUEST_TIMEOUT = 10
    MAX_RETRIES = 3
    CACHE_TIMEOUT = 300  # 5 minutes
    
    # LLM Settings
    DEFAULT_TEMPERATURE = 0.7
    MAX_TOKENS = 2000
    
    # Export Settings
    PDF_PAGE_SIZE = "A4"
    PDF_MARGIN = "1cm"
    
    # UI Settings
    GRADIO_THEME = "soft"
    MAX_FILE_SIZE_MB = 10
    
    @classmethod
    def validate_api_keys(cls):
        """Validate that required API keys are set."""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY not set in environment")
        
        if not cls.GOOGLE_API_KEY:
            errors.append("GOOGLE_API_KEY not set in environment")
        
        return errors
    
    @classmethod
    def get_model_choices(cls):
        """Get list of model names for UI dropdown."""
        return [model["name"] for model in cls.MODELS.values()]
    
    @classmethod
    def get_tone_choices(cls):
        """Get list of tone names for UI dropdown."""
        return [tone["name"] for tone in cls.TONES.values()]
    
    @classmethod
    def get_model_key_by_name(cls, model_name):
        """Get model key from display name."""
        for key, value in cls.MODELS.items():
            if value["name"] == model_name:
                return key
        return cls.GEMINI_MODEL  # Default
    
    @classmethod
    def get_tone_key_by_name(cls, tone_name):
        """Get tone key from display name."""
        for key, value in cls.TONES.items():
            if value["name"] == tone_name:
                return key
        return "professional"  # Default