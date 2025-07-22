"""
Byword Legal AI - Communications Module
Handles international phone numbers, client notifications, and contact management
"""

# Import main classes
try:
    from .international_phone_system import InternationalPhoneManager
except ImportError:
    # Graceful fallback during development
    pass

# Module metadata
__version__ = "0.1.0"
__author__ = "Byword Legal AI Team"

# Supported phone systems
SUPPORTED_PHONE_COUNTRIES = [
    "US", "CA", "AU", "GB", "DE", "FR", "BR", "IN", "JP", "MX"
]

# Emergency numbers by country
EMERGENCY_NUMBERS = {
    "US": "911",
    "CA": "911", 
    "AU": "000",
    "GB": "999",
    "DE": "112",
    "FR": "112",
    "BR": "190",
    "IN": "112",
    "JP": "110",
    "MX": "911"
}

# Quick access functions
def validate_phone_quick(phone_number: str, country_code: str = "US"):
    """Quick phone number validation"""
    try:
        phone_manager =