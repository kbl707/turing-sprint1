import re
import time
import streamlit as st
from typing import List, Dict

# Profanity patterns to filter out
PROFANITY_PATTERNS = [
    r'\b(ass|shit|fuck|bitch|cunt|dick|pussy|whore|slut)\b',
    r'\b(nigger|nigga|chink|spic|kike|gook)\b',
    r'\b(rape|kill|murder|suicide|terrorist)\b',
    r'\b(hitler|nazi|kkk|isis|al-qaeda)\b'
]

# Rate limiting configuration
RATE_LIMIT_WINDOW = 2  # seconds between requests

def validate_role(role: str) -> tuple[bool, str]:
    """Validate the role input"""
    if not role:
        return False, "Role cannot be empty"
        
    if len(role) > 100:
        return False, "Role must be less than 100 characters"
        
    # Check for profanity
    for pattern in PROFANITY_PATTERNS:
        if re.search(pattern, role.lower()):
            return False, "Role contains inappropriate content"
            
    return True, ""

def rate_limit() -> bool:
    """Check if we should rate limit the request"""
    current_time = time.time()
    
    # Initialize last_call if not exists
    if 'last_call' not in st.session_state:
        st.session_state.last_call = 0
        
    # Check if enough time has passed
    time_since_last_call = current_time - st.session_state.last_call
    if time_since_last_call < RATE_LIMIT_WINDOW:
        time_remaining = RATE_LIMIT_WINDOW - time_since_last_call
        st.info(f"Please wait {int(time_remaining) + 1} seconds before generating the next scenario...")
        return False
        
    # Update last call time
    st.session_state.last_call = current_time
    return True

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS"""
    if not text:
        return ""
        
    # Remove script tags and their content
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove other potentially dangerous HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Escape special characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    
    return text

def handle_api_error(e: Exception) -> str:
    """Handle API errors and return user-friendly message"""
    error_message = str(e).lower()
    
    if "rate limit" in error_message:
        return "The API is currently rate limited. Please try again in a few minutes."
    elif "authentication" in error_message:
        return "There was an authentication error. Please check your API key."
    elif "timeout" in error_message:
        return "The request timed out. Please try again."
    else:
        return "An unexpected error occurred. Please try again later." 