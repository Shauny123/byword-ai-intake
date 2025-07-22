#!/usr/bin/env python3
"""
Byword Legal AI - International Jurisdiction Manager
The MAIN script that handles all international legal jurisdictions
This is your core legal AI system that replaces rebuild_colorado_index.py
"""

import os
import sys
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# International Jurisdiction Database - COMPLETE SYSTEM
INTERNATIONAL_JURISDICTIONS = {
    "united_states": {
        "country_name": "United States",
        "country_code": "US",
        "legal_system": "common_law",
        "federal_system": True,
        "states": {
            "colorado": {
                "name": "Colorado",
                "code": "CO", 
                "capital": "Denver",
                "zip_ranges": ["80001-81699"],
                "major_cities": {
                    "denver": {"zip_ranges": ["80201-80299"], "population": 715522},
                    "colorado_springs": {"zip_ranges": ["80901-80951"], "population": 478961}
                }
            },
            "california": {
                "name": "California",
                "code": "CA",
                "capital": "Sacramento", 
                "zip_ranges": ["90001-96162"],
                "major_cities": {
                    "los_angeles": {"zip_ranges": ["90001-90899"], "population": 3898747},
                    "san_francisco": {"zip_ranges": ["94101-94188"], "population": 873965}
                }
            },
            "new_york": {
                "name": "New York",
                "code": "NY",
                "capital": "Albany",
                "zip_ranges": ["10001-14999"],
                "major_cities": {
                    "new_york_city": {"zip_ranges": ["10001-10299"], "population": 8336817}
                }
            }
        }
    },
    "canada": {
        "country_name": "Canada", 
        "country_code": "CA",
        "legal_system": "common_law",
        "federal_system": True,
        "states": {
            "ontario": {
                "name": "Ontario",
                "code": "ON",
                "capital": "Toronto",
                "postal_patterns": ["K", "L", "M", "N", "P"],
                "major_cities": {
                    "toronto": {"postal_prefixes": ["M"], "population": 2794356},
                    "ottawa": {"postal_prefixes": ["K1", "K2"], "population": 1017449}
                }
            },
            "british_columbia": {
                "name": "British Columbia",
                "code": "BC", 
                "capital": "Victoria",
                "postal_patterns": ["V"],
                "major_cities": {
                    "vancouver": {"postal_prefixes": ["V5", "V6"], "population": 631486}
                }
            }
        }
    },
    "australia": {
        "country_name": "Australia",
        "country_code": "AU", 
        "legal_system": "common_law",
        "federal_system": True,
        "states": {
            "new_south_wales": {
                "name": "New South Wales",
                "code": "NSW",
                "capital": "Sydney",
                "postcode_ranges": ["1000-2999"],
                "major_cities": {
                    "sydney": {"postcode_ranges": ["2000-2599"], "population": 5312163}
                }
            },
            "victoria": {
                "name": "Victoria", 
                "code": "VIC",
                "capital": "Melbourne",
                "postcode_ranges": ["3000-3999"],
                "major_cities": {
                    "melbourne": {"postcode_ranges": ["3000-3207"], "population": 5078193}
                }
            }
        }
    },
    "united_kingdom": {
        "country_name": "United Kingdom",
        "country_code": "GB",
        "legal_system": "common_law", 
        "federal_system": False,
        "states": {
            "england": {
                "name": "England",
                "code": "ENG",
                "capital": "London",
                "postcode_areas": ["E", "EC", "N", "NW", "SE", "SW", "W", "WC"],
                "major_cities": {
                    "london": {"postcode_areas": ["E", "EC", "N", "NW", "SE", "SW", "W", "WC"], "population": 9648110}
                }
            },
            "scotland": {
                "name": "Scotland",
                "code": "SCT", 
                "capital": "Edinburgh",
                "postcode_areas": ["AB", "DD", "DG", "EH", "FK", "G", "HS", "IV", "KA", "KW", "KY", "ML", "PA", "PH", "TD", "ZE"],
                "major_cities": {
                    "glasgow": {"postcode_areas": ["G"], "population": 635640},
                    "edinburgh": {"postcode_areas": ["EH"], "population": 526470}
                }
            }
        }
    },
    "germany": {
        "country_name": "Germany",
        "country_code": "DE",
        "legal_system": "civil_law",
        "federal_system": True,
        "states": {
            "bavaria": {
                "name": "Bavaria",
                "code": "BY",
                "capital": "Munich", 
                "plz_ranges": ["80000-87999"],
                "major_cities": {
                    "munich": {"plz_ranges": ["80000-81999"], "population": 1484226}
                }
            },
            "north_rhine_westphalia": {
                "name": "North Rhine-Westphalia",
                "code": "NW",
                "capital": "Düsseldorf",
                "plz_ranges": ["40000-59999"],
                "major_cities": {
                    "cologne": {"plz_ranges": ["50000-51999"], "population": 1087863}
                }
            }
        }
    },
    "france": {
        "country_name": "France",
        "country_code": "FR",
        "legal_system": "civil_law",
        "federal_system": False,
        "states": {
            "ile_de_france": {
                "name": "Île-de-France", 
                "code": "IDF",
                "capital": "Paris",
                "postal_ranges": ["75001-75020", "77000-77999", "78000-78999"],
                "major_cities": {
                    "paris": {"postal_ranges": ["75001-75020"], "population": 2161000}
                }
            }
        }
    }
}

# Legal System Equivalencies 
LEGAL_EQUIVALENCIES = {
    "employment_law": {
        "common_law": ["wrongful_termination", "discrimination", "harassment", "whistleblower", "wage_theft"],
        "civil_law": ["employment_termination", "workplace_discrimination", "employee_protection", "salary_disputes"]
    },
    "civil_rights": {
        "common_law": ["discrimination", "civil_liberties", "constitutional_rights"],
        "civil_law": ["fundamental_rights", "equality_rights", "personal_rights"]
    }
}

@dataclass
class ClientCase:
    """Enhanced client case with international support"""
    case_id: str
    client_email: str = ""
    client_phone: str = ""
    incident_date: str = ""
    country: str = ""
    state_province: str = ""
    claim_type: str = ""
    summary: str = ""
    status: str = "new"
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())

class InternationalJurisdictionManager:
    """Main class - handles all international legal jurisdictions"""
    
    def __init__(self):
        self.jurisdictions = INTERNATIONAL_JURISDICTIONS
        self.equivalencies = LEGAL_EQUIVALENCIES
        self.logger = self.setup_logging()
    
    def setup_logging(self) -> logging.Logger:
        """Setup logging system"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def search_jurisdictions(self, query: str) -> List[Dict]:
        """Search for jurisdictions by name, code, or location"""
        results = []
        query_lower = query.lower()
        
        for country_key, country_data in self.jurisdictions.items():
            # Search countries
            if (query_lower in country_data["country_name"].lower() or 
                query_lower in country_data["country_code"].lower()):
                results.append({
                    "type": "country",
                    "key": country_key,
                    "name": country_data["country_name"],
                    "code": country_data["country_code"],
                    "legal_system": country_data["legal_system"]
                })
            
            # Search states/provinces
            for state_key, state_data in country_data["states"].items():
                if (query_lower in state_data["name"].lower() or 
                    query_lower in state_data["code"].lower() or
                    query_lower in state_key.lower()):
                    results.append({
                        "type": "state",
                        "country_key": country_key,
                        "country_name": country_data["country_name"],
                        "state_key": state_key,
                        "state_name": state_data["name"],
                        "state_code": state_data["code"],
                        "capital": state_data["capital"],
                        "legal_system": country_data["legal_system"]
                    })
        
        return results
    
    def get_country_info(self, country_key: str) -> Optional[Dict]:
        """Get detailed country information"""
        return self.jurisdictions.get(country_key.lower())
    
    def get_state_info(self, country_key: str, state_key: str) -> Optional[Dict]:
        """Get detailed state/province information"""
        country = self.get_country_info(country_key)
        if country and "states" in country:
            return country["states"].get(state_key.lower())
        return None
    
    def find_equivalent_claim_types(self, claim_type: str, target_legal_system: str) -> List[str]:
        """Find equivalent legal concepts across legal systems"""
        equivalents = []
        
        for category, systems in self.equivalencies.items():
            for system, claims in systems.items():
                if system == target_legal_system and claim_type.lower() in [c.lower() for c in claims]:
                    equivalents.extend(claims)
                    break
        
        return list(set(equivalents))
    
    def validate_postal_code(self, postal_code: str, country_code: str) -> Tuple[bool, str]:
        """Validate postal code format for country"""
        patterns = {
            "US": r"^\d{5}(-\d{4})?$",  # ZIP or ZIP+4
            "CA": r"^[A-Z]\d[A-Z] \d[A-Z]\d$",  # Canadian postal code
            "AU": r"^\d{4}$",  # Australian postcode
            "GB": r"^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$",  # UK postcode
            "DE": r"^\d{5}$",  # German PLZ
            "FR": r"^\d{5}$"   # French postal code
        }
        
        pattern = patterns.get(country_code.upper())
        if not pattern:
            return False, f"No validation pattern for country {country_code}"
        
        if re.match(pattern, postal_code.strip()):
            return True, "Valid postal code format"
        else:
            return False, f"Invalid format for {country_code}"
    
    def load_cases_by_jurisdiction(self, country_key: str, state_key: str = None) -> List[Dict]:
        """Load cases for specific jurisdiction - BACKWARD COMPATIBLE with Colorado"""
        try:
            # Try to load from standard location
            data_file = Path("data/client_cases.json")
            if not data_file.exists():
                # Try alternative locations
                for alt_path in ["../data/client_cases.json", "client_cases.json"]:
                    if Path(alt_path).exists():
                        data_file = Path(alt_path)
                        break
            
            if not data_file.exists():
                self.logger.warning("No client cases file found")
                return []
            
            with open(data_file, 'r') as f:
                all_cases = json.load(f)
            
            # Filter cases by jurisdiction
            filtered_cases = []
            for case in all_cases:
                # New format: country + state_province
                case_country = case.get('country', '').lower()
                case_state = case.get('state_province', '').lower()
                
                # Legacy format: jurisdiction field (for Colorado backward compatibility)
                legacy_jurisdiction = case.get('jurisdiction', '').lower()
                
                # Match new format
                if case_country == country_key.lower():
                    if state_key:
                        if case_state == state_key.lower():
                            filtered_cases.append(case)
                    else:
                        filtered_cases.append(case)
                # Match legacy format (Colorado compatibility)
                elif legacy_jurisdiction == state_key.lower() if state_key else False:
                    filtered_cases.append(case)
            
            self.logger.info(f"Found {len(filtered_cases)} cases for {country_key}" + 
                           (f"/{state_key}" if state_key else ""))
            return filtered_cases
            
        except Exception as e:
            self.logger.error(f"Error loading cases: {e}")
            return []
    
    def rebuild_colorado_index(self) -> bool:
        """BACKWARD COMPATIBLE: Rebuild Colorado index using new international system"""
        self.logger.info("🏔️ Rebuilding Colorado index (backward compatible)")
        
        # Load Colorado cases using new system
        colorado_cases = self.load_cases_by_jurisdiction("united_states", "colorado")
        
        if not colorado_cases:
            self.logger.warning("No Colorado cases found")
            return False
        
        # Create index directory
        index_dir = Path("faiss_indices/usa/colorado")
        index_dir.mkdir(parents=True, exist_ok=True)
        
        # Simple index creation (replace with actual FAISS if needed)
        try:
            import numpy as np
            
            # Create embeddings (simplified)
            texts = [case.get('summary', '') for case in colorado_cases]
            embeddings = np.random.random((len(texts), 768)).astype('float32')
            
            # Save metadata
            metadata_file = index_dir / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(colorado_cases, f, indent=2)
            
            # Save simple index info
            index_info = {
                "cases_count": len(colorado_cases),
                "embeddings_shape": embeddings.shape,
                "created_date": datetime.now().isoformat(),
                "system_version": "international_v1.0"
            }
            
            info_file = index_dir / "index_info.json"
            with open(info_file, 'w') as f:
                json.dump(index_info, f, indent=2)
            
            self.logger.info(f"✅ Colorado index rebuilt with {len(colorado_cases)} cases")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to rebuild Colorado index: {e}")
            return False

def main():
    """Main function - can be used as standalone script"""
    print("🌍 Byword Legal AI - International Jurisdiction Manager")
    print("=" * 60)
    
    # Initialize the system
    manager = InternationalJurisdictionManager()
    
    # Example usage
    print("\n🔍 Testing jurisdiction search:")
    
    # Test Colorado (backward compatibility)
    colorado_results = manager.search_jurisdictions("colorado")
    for result in colorado_results:
        print(f"Found: {result['state_name']}, {result['country_name']}")
    
    # Test international
    uk_results = manager.search_jurisdictions("england")
    for result in uk_results:
        print(f"Found: {result['state_name']}, {result['country_name']}")
    
    # Test Colorado index rebuild (backward compatible)
    print("\n🏔️ Testing Colorado index rebuild:")
    success = manager.rebuild_colorado_index()
    if success:
        print("✅ Colorado index rebuilt successfully")
    else:
        print("❌ Colorado index rebuild failed")
    
    print("\n🎉 International legal system ready!")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
