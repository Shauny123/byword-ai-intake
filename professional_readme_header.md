<div align="center">

# 🏛️ Byword Legal AI - International Intake System

**A comprehensive legal intake system supporting 50+ global jurisdictions with intelligent case routing and multi-jurisdiction legal equivalencies.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/Shauny123/byword-legal-ai-intake)
[![GitHub stars](https://img.shields.io/github/stars/Shauny123/byword-legal-ai-intake.svg?style=social&label=Star)](https://github.com/Shauny123/byword-legal-ai-intake/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Shauny123/byword-legal-ai-intake.svg?style=social&label=Fork)](https://github.com/Shauny123/byword-legal-ai-intake/network/members)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub issues](https://img.shields.io/github/issues/Shauny123/byword-legal-ai-intake.svg)](https://github.com/Shauny123/byword-legal-ai-intake/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/Shauny123/byword-legal-ai-intake.svg)](https://github.com/Shauny123/byword-legal-ai-intake/commits/main)

</div>

---

## 🚀 Quick Start

```bash
pip install git+https://github.com/Shauny123/byword-legal-ai-intake.git
```

```python
from byword_legal import search_jurisdictions, validate_phone

# Search jurisdictions globally
results = search_jurisdictions("colorado")
print(f"Found: {results[0]['state_name']}, {results[0]['country_name']}")

# Validate international phone numbers
phone_info = validate_phone("+1 (303) 555-0123", "US")
print(f"Valid: {phone_info['is_valid']}, Location: {phone_info['area_location']}")
```

---

## 🌍 Supported Jurisdictions

<div align="center">

[![🇺🇸 United States](https://img.shields.io/badge/🇺🇸-50_States_+_Territories-blue?style=for-the-badge)](docs/jurisdictions/united-states.md)
[![🇨🇦 Canada](https://img.shields.io/badge/🇨🇦-13_Provinces_+_Territories-red?style=for-the-badge)](docs/jurisdictions/canada.md)
[![🇦🇺 Australia](https://img.shields.io/badge/🇦🇺-8_States_+_Territories-green?style=for-the-badge)](docs/jurisdictions/australia.md)

[![🇬🇧 United Kingdom](https://img.shields.io/badge/🇬🇧-4_Countries-navy?style=for-the-badge)](docs/jurisdictions/united-kingdom.md)
[![🇩🇪 Germany](https://img.shields.io/badge/🇩🇪-16_Federal_States-black?style=for-the-badge)](docs/jurisdictions/germany.md)
[![🇫🇷 France](https://img.shields.io/badge/🇫🇷-13_Regions-blue?style=for-the-badge)](docs/jurisdictions/france.md)

</div>

---

## 🎯 Key Features

<div align="center">

[![Jurisdictions](https://img.shields.io/badge/🌍_Jurisdictions-200+-brightgreen?style=for-the-badge)](docs/features/jurisdictions.md)
[![Phone System](https://img.shields.io/badge/📞_Phone_System-International-blue?style=for-the-badge)](docs/features/phone-system.md)
[![Legal AI](https://img.shields.io/badge/⚖️_Legal_AI-Powered-purple?style=for-the-badge)](docs/features/legal-ai.md)
[![Court Mapping](https://img.shields.io/badge/🏛️_Court_Mapping-Local-orange?style=for-the-badge)](docs/features/court-mapping.md)

</div>

---

## 🛠️ Built With

<div align="center">

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange?style=for-the-badge&logo=facebook)](https://github.com/facebookresearch/faiss)
[![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org)
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)

</div>

---