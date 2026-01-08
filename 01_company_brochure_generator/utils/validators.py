"""Validation utilities for the Company Brochure Generator."""

import re
from urllib.parse import urlparse


def validate_url(url: str) -> tuple[bool, str]:
    """
    Validate and normalize a URL.
    
    Args:
        url: The URL to validate
        
    Returns:
        Tuple of (is_valid, normalized_url or error_message)
    """
    if not url or not isinstance(url, str):
        return False, "URL cannot be empty"
    
    # Remove whitespace
    url = url.strip()
    
    # Add https:// if no protocol specified
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Parse URL
    try:
        result = urlparse(url)
        
        # Check if has scheme and netloc
        if not all([result.scheme, result.netloc]):
            return False, "Invalid URL format"
        
        # Check if scheme is http or https
        if result.scheme not in ['http', 'https']:
            return False, "URL must use http or https protocol"
        
        # Check if netloc has at least one dot (basic domain validation)
        if '.' not in result.netloc:
            return False, "Invalid domain name"
        
        return True, url
        
    except Exception as e:
        return False, f"Invalid URL: {str(e)}"


def validate_company_name(name: str) -> tuple[bool, str]:
    """
    Validate company name.
    
    Args:
        name: The company name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not isinstance(name, str):
        return False, "Company name cannot be empty"
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "Company name must be at least 2 characters"
    
    if len(name) > 100:
        return False, "Company name must be less than 100 characters"
    
    return True, ""


def sanitize_text(text: str) -> str:
    """
    Sanitize text input by removing potential harmful content.
    
    Args:
        text: The text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove any HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    return text


def validate_temperature(temp: float) -> tuple[bool, str]:
    """
    Validate temperature parameter.
    
    Args:
        temp: The temperature value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        temp = float(temp)
        if 0 <= temp <= 1:
            return True, ""
        return False, "Temperature must be between 0 and 1"
    except (ValueError, TypeError):
        return False, "Temperature must be a valid number"


def validate_max_content_length(length: int) -> tuple[bool, str]:
    """
    Validate max content length parameter.
    
    Args:
        length: The max content length to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        length = int(length)
        if 1000 <= length <= 10000:
            return True, ""
        return False, "Max content length must be between 1000 and 10000"
    except (ValueError, TypeError):
        return False, "Max content length must be a valid number"