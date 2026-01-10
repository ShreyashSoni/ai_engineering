"""Test script to verify the setup is working correctly."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from config import Config
        print("✓ Config imported")
        
        from utils.validators import validate_url, validate_company_name
        print("✓ Validators imported")
        
        from utils.prompts import get_brochure_system_prompt
        print("✓ Prompts imported")
        
        from services.scraper_service import ScraperService
        print("✓ ScraperService imported")
        
        from services.llm_service import LLMService
        print("✓ LLMService imported")
        
        from services.brochure_service import BrochureService
        print("✓ BrochureService imported")
        
        from services.export_service import ExportService
        print("✓ ExportService imported")
        
        print("\n✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        return False

def test_config():
    """Test configuration."""
    print("\nTesting configuration...")
    from config import Config
    
    errors = Config.validate_api_keys()
    if errors:
        print("⚠️  API Key warnings:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✓ API keys configured")
    
    print(f"✓ Available models: {len(Config.MODELS)}")
    print(f"✓ Available tones: {len(Config.TONES)}")
    print(f"✓ Model choices: {Config.get_model_choices()}")
    print(f"✓ Tone choices: {Config.get_tone_choices()}")

def test_validators():
    """Test validators."""
    print("\nTesting validators...")
    from utils.validators import validate_url, validate_company_name
    
    # Test URL validation
    valid, result = validate_url("https://example.com")
    assert valid, "Valid URL should pass"
    print("✓ URL validation works")
    
    # Test company name validation
    valid, error = validate_company_name("Test Company")
    assert valid, "Valid name should pass"
    print("✓ Company name validation works")

def test_services():
    """Test service initialization."""
    print("\nTesting service initialization...")
    
    try:
        from services.scraper_service import ScraperService
        scraper = ScraperService()
        print("✓ ScraperService initialized")
        
        from services.export_service import ExportService
        export = ExportService()
        print("✓ ExportService initialized")
        
        # LLM service requires API keys, so we just test import
        from services.llm_service import LLMService
        print("✓ LLMService can be imported")
        
        from services.brochure_service import BrochureService
        print("✓ BrochureService can be imported")
        
        return True
    except Exception as e:
        print(f"❌ Service initialization error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Company Brochure Generator - Setup Test")
    print("=" * 60)
    
    # Run tests
    imports_ok = test_imports()
    if not imports_ok:
        print("\n❌ Setup incomplete. Fix import errors first.")
        return False
    
    test_config()
    test_validators()
    services_ok = test_services()
    
    print("\n" + "=" * 60)
    if imports_ok and services_ok:
        print("✅ ALL TESTS PASSED!")
        print("\nYou can now run the application with:")
        print("  python app.py")
    else:
        print("⚠️  Some tests failed. Review the errors above.")
    print("=" * 60)
    
    return imports_ok and services_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)