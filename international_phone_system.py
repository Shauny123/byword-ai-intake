#!/usr/bin/env python3
"""
International Phone Number System for Byword Legal AI
Handles phone number validation, formatting, and international dialing codes
for client contact management across all supported jurisdictions
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum

@dataclass
class PhoneNumberInfo:
    """Complete phone number information"""
    raw_number: str
    formatted_number: str
    international_format: str
    country_code: str
    national_number: str
    area_code: Optional[str]
    is_valid: bool
    phone_type: str  # "mobile", "landline", "toll_free", "emergency"
    country_name: str
    timezone: str

@dataclass
class CountryPhoneInfo:
    """Phone system information for a country"""
    country_code: str  # ISO 3166-1 alpha-2
    calling_code: str  # International dialing code
    country_name: str
    phone_formats: Dict[str, str]  # Different format patterns
    national_prefix: str  # Domestic dialing prefix
    international_prefix: str  # International dialing prefix
    mobile_prefixes: List[str]  # Mobile number prefixes
    emergency_numbers: Dict[str, str]  # Emergency service numbers
    area_codes: Optional[Dict[str, str]] = None  # Geographic area codes

# Comprehensive international phone number database
INTERNATIONAL_PHONE_DATABASE = {
    "united_states": {
        "country_code": "US",
        "calling_code": "+1",
        "country_name": "United States",
        "phone_formats": {
            "international": "+1 (XXX) XXX-XXXX",
            "national": "(XXX) XXX-XXXX",
            "compact": "XXX-XXX-XXXX",
            "digits_only": "XXXXXXXXXX"
        },
        "national_prefix": "1",
        "international_prefix": "011",
        "mobile_prefixes": [],  # US doesn't distinguish mobile by prefix
        "emergency_numbers": {
            "police": "911",
            "fire": "911", 
            "medical": "911",
            "general": "911"
        },
        "area_codes": {
            # Colorado area codes
            "303": "Denver Metro Area",
            "720": "Denver Metro Area (overlay)",
            "719": "Colorado Springs, Pueblo",
            "970": "Northern and Western Colorado",
            # California area codes
            "213": "Los Angeles",
            "310": "West Los Angeles, Beverly Hills",
            "323": "Los Angeles (overlay)",
            "415": "San Francisco",
            "510": "Oakland, Berkeley",
            "650": "San Mateo County",
            "707": "Napa, Santa Rosa",
            "714": "Orange County",
            "760": "San Diego County North",
            "805": "Santa Barbara, Ventura",
            "818": "San Fernando Valley",
            "831": "Monterey, Santa Cruz",
            "858": "San Diego",
            "909": "San Bernardino",
            "916": "Sacramento",
            "949": "South Orange County",
            # New York area codes
            "212": "Manhattan",
            "347": "NYC (overlay)",
            "646": "Manhattan (overlay)",
            "718": "Brooklyn, Queens, Bronx, Staten Island",
            "917": "NYC (overlay)",
            # Texas area codes
            "214": "Dallas",
            "281": "Houston suburbs",
            "512": "Austin",
            "713": "Houston",
            "832": "Houston (overlay)",
            "972": "Dallas suburbs"
        }
    },
    "canada": {
        "country_code": "CA",
        "calling_code": "+1",
        "country_name": "Canada",
        "phone_formats": {
            "international": "+1 (XXX) XXX-XXXX",
            "national": "(XXX) XXX-XXXX",
            "compact": "XXX-XXX-XXXX",
            "digits_only": "XXXXXXXXXX"
        },
        "national_prefix": "1",
        "international_prefix": "011",
        "mobile_prefixes": [],  # Canada uses same format as landlines
        "emergency_numbers": {
            "police": "911",
            "fire": "911",
            "medical": "911",
            "general": "911"
        },
        "area_codes": {
            # Ontario
            "416": "Toronto",
            "647": "Toronto (overlay)", 
            "437": "Toronto (overlay)",
            "613": "Ottawa",
            "905": "Greater Toronto Area",
            "289": "Hamilton area (overlay)",
            "519": "London, Windsor",
            "705": "Northern Ontario",
            "807": "Thunder Bay area",
            # British Columbia
            "604": "Vancouver",
            "778": "Vancouver (overlay)",
            "236": "Vancouver (overlay)",
            "250": "Rest of British Columbia",
            # Alberta
            "403": "Calgary",
            "587": "Calgary (overlay)",
            "780": "Edmonton",
            "825": "Edmonton (overlay)",
            # Quebec
            "514": "Montreal",
            "438": "Montreal (overlay)",
            "450": "Montreal suburbs",
            "579": "Montreal suburbs (overlay)",
            "418": "Quebec City",
            "819": "Eastern Quebec"
        }
    },
    "australia": {
        "country_code": "AU",
        "calling_code": "+61",
        "country_name": "Australia",
        "phone_formats": {
            "international": "+61 X XXXX XXXX",
            "national": "0X XXXX XXXX",
            "compact": "XXXXXXXXXX",
            "digits_only": "XXXXXXXXXX"
        },
        "national_prefix": "0",
        "international_prefix": "0011",
        "mobile_prefixes": ["04", "05"],
        "emergency_numbers": {
            "police": "000",
            "fire": "000",
            "medical": "000",
            "general": "000"
        },
        "area_codes": {
            "02": "New South Wales, Australian Capital Territory",
            "03": "Victoria, Tasmania",
            "07": "Queensland", 
            "08": "South Australia, Western Australia, Northern Territory",
            "04": "Mobile phones",
            "05": "Mobile phones (alternative)"
        }
    },
    "united_kingdom": {
        "country_code": "GB",
        "calling_code": "+44",
        "country_name": "United Kingdom",
        "phone_formats": {
            "international": "+44 XXXX XXX XXX",
            "national": "0XXXX XXX XXX",
            "compact": "XXXXXXXXXXX",
            "digits_only": "XXXXXXXXXXX"
        },
        "national_prefix": "0",
        "international_prefix": "00",
        "mobile_prefixes": ["07"],
        "emergency_numbers": {
            "police": "999",
            "fire": "999",
            "medical": "999",
            "general": "999",
            "european": "112"
        },
        "area_codes": {
            "020": "London",
            "0121": "Birmingham",
            "0131": "Edinburgh",
            "0141": "Glasgow", 
            "0151": "Liverpool",
            "0161": "Manchester",
            "0113": "Leeds",
            "0114": "Sheffield",
            "0115": "Nottingham",
            "0116": "Leicester",
            "0117": "Bristol",
            "0118": "Reading",
            "01223": "Cambridge",
            "01865": "Oxford",
            "01904": "York"
        }
    },
    "germany": {
        "country_code": "DE",
        "calling_code": "+49",
        "country_name": "Germany",
        "phone_formats": {
            "international": "+49 XXX XXXXXXX",
            "national": "0XXX XXXXXXX",
            "compact": "XXXXXXXXXXX",
            "digits_only": "XXXXXXXXXXX"
        },
        "national_prefix": "0",
        "international_prefix": "00",
        "mobile_prefixes": ["015", "016", "017"],
        "emergency_numbers": {
            "police": "110",
            "fire": "112",
            "medical": "112",
            "general": "112"
        },
        "area_codes": {
            "030": "Berlin",
            "040": "Hamburg",
            "069": "Frankfurt am Main",
            "089": "Munich",
            "0221": "Cologne",
            "0211": "Düsseldorf",
            "0201": "Essen",
            "0231": "Dortmund",
            "0711": "Stuttgart",
            "0351": "Dresden"
        }
    },
    "france": {
        "country_code": "FR", 
        "calling_code": "+33",
        "country_name": "France",
        "phone_formats": {
            "international": "+33 X XX XX XX XX",
            "national": "0X XX XX XX XX",
            "compact": "XXXXXXXXXX",
            "digits_only": "XXXXXXXXXX"
        },
        "national_prefix": "0",
        "international_prefix": "00",
        "mobile_prefixes": ["06", "07"],
        "emergency_numbers": {
            "police": "17",
            "fire": "18",
            "medical": "15",
            "general": "112"
        },
        "area_codes": {
            "01": "Île-de-France (Paris region)",
            "02": "Northwest France",
            "03": "Northeast France", 
            "04": "Southeast France",
            "05": "Southwest France",
            "06": "Mobile phones",
            "07": "Mobile phones"
        }
    },
    "brazil": {
        "country_code": "BR",
        "calling_code": "+55",
        "country_name": "Brazil",
        "phone_formats": {
            "international": "+55 XX XXXXX-XXXX",
            "national": "(XX) XXXXX-XXXX",
            "compact": "XXXXXXXXXXX",
            "digits_only": "XXXXXXXXXXX"
        },
        "national_prefix": "0",
        "international_prefix": "00",
        "mobile_prefixes": ["9"],  # Mobile numbers start with 9
        "emergency_numbers": {
            "police": "190",
            "fire": "193",
            "medical": "192",
            "general": "911"
        },
        "area_codes": {
            "11": "São Paulo",
            "21": "Rio de Janeiro",
            "31": "Belo Horizonte",
            "41": "Curitiba",
            "47": "Joinville",
            "48": "Florianópolis",
            "51": "Porto Alegre",
            "61": "Brasília",
            "62": "Goiânia",
            "71": "Salvador",
            "81": "Recife",
            "85": "Fortaleza"
        }
    },
    "india": {
        "country_code": "IN",
        "calling_code": "+91",
        "country_name": "India",
        "phone_formats": {
            "international": "+91 XXXXX XXXXX",
            "national": "XXXXX XXXXX",
            "compact": "XXXXXXXXXX",
            "digits_only": "XXXXXXXXXX"
        },
        "national_prefix": "0",
        "international_prefix": "00",
        "mobile_prefixes": ["6", "7", "8", "9"],
        "emergency_numbers": {
            "police": "100",
            "fire": "101", 
            "medical": "102",
            "general": "112"
        },
        "area_codes": {
            "11": "Delhi",
            "22": "Mumbai",
            "33": "Kolkata",
            "40": "Hyderabad",
            "44": "Chennai",
            "80": "Bangalore",
            "20": "Pune",
            "79": "Ahmedabad"
        }
    },
    "japan": {
        "country_code": "JP",
        "calling_code": "+81",
        "country_name": "Japan",
        "phone_formats": {
            "international": "+81 XX-XXXX-XXXX",
            "national": "0XX-XXXX-XXXX",
            "compact": "XXXXXXXXXXX",
            "digits_only": "XXXXXXXXXXX"
        },
        "national_prefix": "0",
        "international_prefix": "010",
        "mobile_prefixes": ["070", "080", "090"],
        "emergency_numbers": {
            "police": "110",
            "fire": "119",
            "medical": "119",
            "general": "110"
        },
        "area_codes": {
            "03": "Tokyo",
            "06": "Osaka",
            "052": "Nagoya",
            "011": "Sapporo",
            "022": "Sendai",
            "092": "Fukuoka",
            "075": "Kyoto",
            "045": "Yokohama"
        }
    },
    "mexico": {
        "country_code": "MX",
        "calling_code": "+52",
        "country_name": "Mexico",
        "phone_formats": {
            "international": "+52 XX XXXX XXXX",
            "national": "XX XXXX XXXX",
            "compact": "XXXXXXXXXX",
            "digits_only": "XXXXXXXXXX"
        },
        "national_prefix": "01",
        "international_prefix": "00",
        "mobile_prefixes": ["1"],  # Mobile numbers have 1 after area code
        "emergency_numbers": {
            "police": "911",
            "fire": "911",
            "medical": "911",
            "general": "911"
        },
        "area_codes": {
            "55": "Mexico City",
            "33": "Guadalajara",
            "81": "Monterrey",
            "222": "Puebla",
            "228": "Veracruz",
            "664": "Tijuana",
            "998": "Cancún"
        }
    }
}

class InternationalPhoneManager:
    """Manages international phone numbers for client contact system"""
    
    def __init__(self):
        self.phone_db = INTERNATIONAL_PHONE_DATABASE
    
    def parse_phone_number(self, phone_number: str, country_hint: str = None) -> PhoneNumberInfo:
        """
        Parse and validate an international phone number
        
        Args:
            phone_number: Raw phone number string
            country_hint: ISO country code hint for better parsing
            
        Returns:
            PhoneNumberInfo with complete parsed information
        """
        # Clean the input
        cleaned_number = self._clean_phone_number(phone_number)
        
        # Try to detect country if international format
        detected_country = self._detect_country_from_number(cleaned_number)
        
        # Use hint if no country detected
        if not detected_country and country_hint:
            detected_country = self._get_country_key_from_code(country_hint)
        
        if not detected_country:
            # Default to US format for unrecognized numbers
            detected_country = "united_states"
        
        country_info = self.phone_db[detected_country]
        
        # Parse the number
        return self._parse_for_country(cleaned_number, detected_country, country_info)
    
    def _clean_phone_number(self, phone_number: str) -> str:
        """Remove all non-digit characters except + at the beginning"""
        # Keep + at the beginning if present
        if phone_number.startswith('+'):
            return '+' + re.sub(r'[^\d]', '', phone_number[1:])
        else:
            return re.sub(r'[^\d]', '', phone_number)
    
    def _detect_country_from_number(self, cleaned_number: str) -> Optional[str]:
        """Detect country from international format"""
        if not cleaned_number.startswith('+'):
            return None
        
        # Try to match calling codes
        for country_key, country_info in self.phone_db.items():
            calling_code = country_info["calling_code"].replace('+', '')
            if cleaned_number[1:].startswith(calling_code):
                return country_key
        
        return None
    
    def _get_country_key_from_code(self, country_code: str) -> Optional[str]:
        """Get country key from ISO country code"""
        for country_key, country_info in self.phone_db.items():
            if country_info["country_code"] == country_code.upper():
                return country_key
        return None
    
    def _parse_for_country(self, cleaned_number: str, country_key: str, country_info: CountryPhoneInfo) -> PhoneNumberInfo:
        """Parse number for specific country format"""
        calling_code = country_info["calling_code"].replace('+', '')
        
        # Remove country code if present
        if cleaned_number.startswith('+' + calling_code):
            national_number = cleaned_number[len(calling_code) + 1:]
        elif cleaned_number.startswith(calling_code):
            national_number = cleaned_number[len(calling_code):]
        else:
            national_number = cleaned_number
        
        # Remove national prefix if present
        national_prefix = country_info["national_prefix"]
        if national_prefix and national_number.startswith(national_prefix):
            national_number = national_number[len(national_prefix):]
        
        # Validate number length and format
        is_valid = self._validate_number_for_country(national_number, country_info)
        
        # Determine phone type
        phone_type = self._determine_phone_type(national_number, country_info)
        
        # Extract area code
        area_code = self._extract_area_code(national_number, country_info)
        
        # Format the number
        formatted_number = self._format_number(national_number, country_info, "national")
        international_format = self._format_number(national_number, country_info, "international")
        
        return PhoneNumberInfo(
            raw_number=cleaned_number,
            formatted_number=formatted_number,
            international_format=international_format,
            country_code=country_info["country_code"],
            national_number=national_number,
            area_code=area_code,
            is_valid=is_valid,
            phone_type=phone_type,
            country_name=country_info["country_name"],
            timezone=self._get_timezone_for_area_code(area_code, country_key)
        )
    
    def _validate_number_for_country(self, national_number: str, country_info: CountryPhoneInfo) -> bool:
        """Validate if number matches country's format requirements"""
        # Basic length validation (this would be more sophisticated in production)
        if country_info["country_code"] in ["US", "CA"]:
            return len(national_number) == 10
        elif country_info["country_code"] == "AU":
            return len(national_number) == 9
        elif country_info["country_code"] == "GB":
            return 10 <= len(national_number) <= 11
        elif country_info["country_code"] == "DE":
            return 10 <= len(national_number) <= 12
        elif country_info["country_code"] == "FR":
            return len(national_number) == 9
        elif country_info["country_code"] == "IN":
            return len(national_number) == 10
        elif country_info["country_code"] == "JP":
            return 10 <= len(national_number) <= 11
        else:
            return len(national_number) >= 7  # Minimum reasonable length
    
    def _determine_phone_type(self, national_number: str, country_info: CountryPhoneInfo) -> str:
        """Determine if number is mobile, landline, etc."""
        mobile_prefixes = country_info["mobile_prefixes"]
        
        for prefix in mobile_prefixes:
            if national_number.startswith(prefix):
                return "mobile"
        
        # Check for special prefixes
        if national_number.startswith("800") or national_number.startswith("855"):
            return "toll_free"
        elif national_number.startswith("900"):
            return "premium"
        else:
            return "landline"
    
    def _extract_area_code(self, national_number: str, country_info: CountryPhoneInfo) -> Optional[str]:
        """Extract area code from national number"""
        area_codes = country_info.get("area_codes", {})
        
        # Try different area code lengths
        for length in [2, 3, 4, 5]:
            if len(national_number) >= length:
                potential_area_code = national_number[:length]
                if potential_area_code in area_codes:
                    return potential_area_code
        
        return None
    
    def _format_number(self, national_number: str, country_info: CountryPhoneInfo, format_type: str) -> str:
        """Format number according to country conventions"""
        if format_type == "international":
            return f"{country_info['calling_code']} {self._apply_formatting(national_number, country_info)}"
        else:
            return self._apply_formatting(national_number, country_info)
    
    def _apply_formatting(self, national_number: str, country_info: CountryPhoneInfo) -> str:
        """Apply country-specific formatting"""
        country_code = country_info["country_code"]
        
        if country_code in ["US", "CA"] and len(national_number) == 10:
            return f"({national_number[:3]}) {national_number[3:6]}-{national_number[6:]}"
        elif country_code == "AU" and len(national_number) == 9:
            return f"{national_number[0]} {national_number[1:5]} {national_number[5:]}"
        elif country_code == "GB":
            if len(national_number) == 10:
                return f"{national_number[:4]} {national_number[4:7]} {national_number[7:]}"
            else:
                return f"{national_number[:3]} {national_number[3:6]} {national_number[6:]}"
        elif country_code == "DE":
            return f"{national_number[:3]} {national_number[3:]}"
        elif country_code == "FR" and len(national_number) == 9:
            return f"{national_number[0]} {national_number[1:3]} {national_number[3:5]} {national_number[5:7]} {national_number[7:]}"
        else:
            # Default formatting
            return national_number
    
    def _get_timezone_for_area_code(self, area_code: str, country_key: str) -> str:
        """Get timezone information for area code"""
        # Simplified timezone mapping - would be more comprehensive in production
        timezone_mapping = {
            "united_states": {
                "303": "America/Denver",  # Colorado
                "720": "America/Denver",  # Colorado
                "719": "America/Denver",  # Colorado
                "970": "America/Denver",  # Colorado
                "213": "America/Los_Angeles",  # California
                "415": "America/Los_Angeles",  # California
                "212": "America/New_York",  # New York
            },
            "canada": {
                "416": "America/Toronto",  # Ontario
                "604": "America/Vancouver",  # British Columbia
            },
            "australia": {
                "02": "Australia/Sydney",
                "03": "Australia/Melbourne",
                "07": "Australia/Brisbane",
                "08": "Australia/Perth",
            }
        }
        
        if country_key in timezone_mapping and area_code in timezone_mapping[country_key]:
            return timezone_mapping[country_key][area_code]
        
        # Default timezone for country
        default_timezones = {
            "united_states": "America/New_York",
            "canada": "America/Toronto", 
            "australia": "Australia/Sydney",
            "united_kingdom": "Europe/London",
            "germany": "Europe/Berlin",
            "france": "Europe/Paris"
        }
        
        return default_timezones.get(country_key, "UTC")
    
    def format_for_dialing(self, phone_info: PhoneNumberInfo, calling_from_country: str) -> Dict[str, str]:
        """Format phone number for dialing from different countries"""
        calling_from_info = None
        for country_key, country_data in self.phone_db.items():
            if country_data["country_code"] == calling_from_country:
                calling_from_info = country_data
                break
        
        if not calling_from_info:
            return {"error": f"Unknown calling country: {calling_from_country}"}
        
        # International dialing format
        international_prefix = calling_from_info["international_prefix"]
        target_calling_code = None
        
        for country_key, country_data in self.phone_db.items():
            if country_data["country_code"] == phone_info.country_code:
                target_calling_code = country_data["calling_code"].replace('+', '')
                break
        
        if not target_calling_code:
            return {"error": f"Unknown target country: {phone_info.country_code}"}
        
        # Same country dialing
        if calling_from_country == phone_info.country_code:
            return {
                "domestic": phone_info.formatted_number,
                "international": phone_info.international_format,
                "dial_string": phone_info.national_number
            }
        
        # International dialing
        dial_string = f"{international_prefix}{target_calling_code}{phone_info.national_number}"
        
        return {
            "international": phone_info.international_format,
            "dial_string": dial_string,
            "instructions": f"Dial {international_prefix} + {target_calling_code} + {phone_info.national_number}"
        }
    
    def get_emergency_numbers(self, country_code: str) -> Dict[str, str]:
        """Get emergency numbers for a country"""
        for country_key, country_info in self.phone_db.items():
            if country_info["country_code"] == country_code:
                return country_info["emergency_numbers"]
        
        return {"error": f"Emergency numbers not found for {country_code}"}
    
    def validate_client_phone(self, phone_number: str, country_code: str = None) -> Dict:
        """Validate and format client phone number for legal system"""
        phone_info = self.parse_phone_number(phone_number, country_code)
        
        return {
            "is_valid": phone_info.is_valid,
            "formatted_number": phone_info.formatted_number,
            "international_format": phone_info.international_format,
            "country": phone_info.country_name,
            "phone_type": phone_info.phone_type,
            "area_location": self._get_area_location(phone_info.area_code, phone_info.country_code),
            "timezone": phone_info.timezone,
            "emergency_numbers": self.get_emergency_numbers(phone_info.country_code)
        }
    
    def _get_area_location(self, area_code: str, country_code: str) -> str:
        """Get geographic location for area code"""
        for country_key, country_info in self.phone_db.items():
            if country_info["country_code"] == country_code:
                area_codes = country_info.get("area_codes", {})
                return area_codes.get(area_code, "Unknown location")
        
        return "Unknown location"

# Example usage and testing
def main():
    """Test the international phone system"""
    phone_manager = InternationalPhoneManager()
    
    print("📞 International Phone Number System Demo")
    print("=" * 50)
    
    # Test phone numbers from different countries
    test_numbers = [
        ("+1 (303) 555-0123", "US", "Colorado number"),
        ("+1-416-555-0123", "CA", "Toronto number"),
        ("+61 2 9876 5432", "AU", "Sydney number"),
        ("+44 20 7946 0958", "GB", "London number"),
        ("+49 30 12345678", "DE", "Berlin number"),
        ("+33 1 42 86 83 26", "FR", "Paris number"),
        ("(303) 555-0123", "US", "Colorado local format"),
        ("416-555-0123", "CA", "Toronto local format")
    ]
    
    for phone_number, country_hint, description in test_numbers:
        print(f"\n📱 Testing: {phone_number} ({description})")
        print("-" * 40)
        
        # Parse and validate
        phone_info = phone_manager.parse_phone_number(phone_number, country_hint)
        
        print(f"✅ Valid: {phone_info.is_valid}")
        print(f"🌍 Country: {phone_info.country_name} ({phone_info.country_code})")
        print(f"📍 Area: {phone_manager._get_area_location(phone_info.area_code, phone_info.country_code)}")
        print(f"📞 Type: {phone_info.phone_type}")
        print(f"🔢 National: {phone_info.formatted_number}")
        print(f"🌐 International: {phone_info.international_format}")
        print(f"🕐 Timezone: {phone_info.timezone}")
        
        # Test dialing from different countries
        if phone_info.is_valid:
            print(f"\n📞 Dialing Instructions:")
            for calling_from in ["US", "CA", "GB"]:
                dial_info = phone_manager.format_for_dialing(phone_info, calling_from)
                if "error" not in dial_info:
                    print(f"  From {calling_from}: {dial_info.get('dial_string', 'Same country')}")
        
        # Emergency numbers
        emergency = phone_manager.get_emergency_numbers(phone_info.country_code)
        if "error" not in emergency:
            print(f"🚨 Emergency: {emergency.get('general', 'N/A')}")

if __name__ == "__main__":
    main()
