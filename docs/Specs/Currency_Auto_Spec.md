# Spec — Currency Auto-detect & Formatting
- On first run, read device region/locale → currency_code (ZA→ZAR, US→USD)
- Allow manual override in Settings; persist locally
- Format using intl NumberFormat.currency(locale, name: currency_code)
- Store money as integer cents; no FX conversion in v2
