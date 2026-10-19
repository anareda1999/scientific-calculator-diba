"""
core/units.py
=============
Unit conversion tables (weight, currency, volume, area, distance).

Each category maps a language code to an ordered dictionary of
``{unit label: factor relative to the category base unit}``.
"""

__all__ = ["CATEGORIES", "CATEGORY_KEYS", "unit_names", "convert"]

CATEGORIES = {
    "Weight": {
        "en": {"Kilogram (kg)": 1.0, "Gram (g)": 1000.0, "Milligram (mg)": 1_000_000.0,
               "Tonne (t)": 0.001, "Pound (lb)": 2.20462, "Ounce (oz)": 35.274},
        "fr": {"Kilogramme (kg)": 1.0, "Gramme (g)": 1000.0, "Milligramme (mg)": 1_000_000.0,
               "Tonne (t)": 0.001, "Livre (lb)": 2.20462, "Once (oz)": 35.274},
        "ar": {"كيلوغرام (kg)": 1.0, "غرام (g)": 1000.0, "مليغرام (mg)": 1_000_000.0,
               "طن (t)": 0.001, "رطل (lb)": 2.20462, "أونصة (oz)": 35.274},
    },
    "Currency": {
        "en": {"US Dollar (USD)": 1.0, "Euro (EUR)": 0.92, "British Pound (GBP)": 0.79,
               "Japanese Yen (JPY)": 149.50, "Canadian Dollar (CAD)": 1.36,
               "Australian Dollar (AUD)": 1.53, "Swiss Franc (CHF)": 0.88,
               "Chinese Yuan (CNY)": 7.24, "Indian Rupee (INR)": 83.50,
               "Algerian Dinar (DZD)": 134.50, "Moroccan Dirham (MAD)": 9.90,
               "Tunisian Dinar (TND)": 3.10},
        "fr": {"Dollar américain (USD)": 1.0, "Euro (EUR)": 0.92, "Livre sterling (GBP)": 0.79,
               "Yen japonais (JPY)": 149.50, "Dollar canadien (CAD)": 1.36,
               "Dollar australien (AUD)": 1.53, "Franc suisse (CHF)": 0.88,
               "Yuan chinois (CNY)": 7.24, "Roupie indienne (INR)": 83.50,
               "Dinar algérien (DZD)": 134.50, "Dirham marocain (MAD)": 9.90,
               "Dinar tunisien (TND)": 3.10},
        "ar": {"دولار أمريكي (USD)": 1.0, "يورو (EUR)": 0.92, "جنيه إسترليني (GBP)": 0.79,
               "ين ياباني (JPY)": 149.50, "دولار كندي (CAD)": 1.36,
               "دولار أسترالي (AUD)": 1.53, "فرنك سويسري (CHF)": 0.88,
               "يوان صيني (CNY)": 7.24, "روبية هندية (INR)": 83.50,
               "دينار جزائري (DZD)": 134.50, "درهم مغربي (MAD)": 9.90,
               "دينار تونسي (TND)": 3.10},
    },
    "Volume": {
        "en": {"Liter (L)": 1.0, "Milliliter (mL)": 1000.0, "Cubic Meter (m³)": 0.001,
               "Gallon (US gal)": 0.264172, "Quart (US qt)": 1.05669,
               "Pint (US pt)": 2.11338, "Cup (US)": 4.22675,
               "Fluid Ounce (US fl oz)": 33.814},
        "fr": {"Litre (L)": 1.0, "Millilitre (mL)": 1000.0, "Mètre cube (m³)": 0.001,
               "Gallon (US gal)": 0.264172, "Quart (US qt)": 1.05669,
               "Pinte (US pt)": 2.11338, "Tasse (US)": 4.22675,
               "Once liquide (US fl oz)": 33.814},
        "ar": {"لتر (L)": 1.0, "مليلتر (mL)": 1000.0, "متر مكعب (m³)": 0.001,
               "غالون (US gal)": 0.264172, "كوارت (US qt)": 1.05669,
               "باينت (US pt)": 2.11338, "كوب (US)": 4.22675,
               "أونصة سائلة (US fl oz)": 33.814},
    },
    "Area": {
        "en": {"Square Meter (m²)": 1.0, "Square Centimeter (cm²)": 10000.0,
               "Square Millimeter (mm²)": 1_000_000.0, "Square Kilometer (km²)": 0.000001,
               "Square Foot (ft²)": 10.7639, "Square Inch (in²)": 1550.0,
               "Hectare (ha)": 0.0001, "Acre": 0.000247105},
        "fr": {"Mètre carré (m²)": 1.0, "Centimètre carré (cm²)": 10000.0,
               "Millimètre carré (mm²)": 1_000_000.0, "Kilomètre carré (km²)": 0.000001,
               "Pied carré (ft²)": 10.7639, "Pouce carré (in²)": 1550.0,
               "Hectare (ha)": 0.0001, "Acre": 0.000247105},
        "ar": {"متر مربع (m²)": 1.0, "سنتيمتر مربع (cm²)": 10000.0,
               "مليمتر مربع (mm²)": 1_000_000.0, "كيلومتر مربع (km²)": 0.000001,
               "قدم مربع (ft²)": 10.7639, "بوصة مربعة (in²)": 1550.0,
               "هكتار (ha)": 0.0001, "فدان": 0.000247105},
    },
    "Distance": {
        "en": {"Kilometer (km)": 1.0, "Meter (m)": 1000.0, "Centimeter (cm)": 100000.0,
               "Millimeter (mm)": 1_000_000.0, "Mile (mi)": 0.621371,
               "Yard (yd)": 1093.61, "Foot (ft)": 3280.84, "Inch (in)": 39370.1,
               "Nautical Mile (nmi)": 0.539957},
        "fr": {"Kilomètre (km)": 1.0, "Mètre (m)": 1000.0, "Centimètre (cm)": 100000.0,
               "Millimètre (mm)": 1_000_000.0, "Mile (mi)": 0.621371,
               "Yard (yd)": 1093.61, "Pied (ft)": 3280.84, "Pouce (in)": 39370.1,
               "Mille marin (nmi)": 0.539957},
        "ar": {"كيلومتر (km)": 1.0, "متر (m)": 1000.0, "سنتيمتر (cm)": 100000.0,
               "مليمتر (mm)": 1_000_000.0, "ميل (mi)": 0.621371,
               "ياردة (yd)": 1093.61, "قدم (ft)": 3280.84, "بوصة (in)": 39370.1,
               "ميل بحري (nmi)": 0.539957},
    },
}

CATEGORY_KEYS = list(CATEGORIES.keys())


def unit_names(category, lang="en"):
    """Ordered list of unit labels for a category in a given language."""
    return list(CATEGORIES[category].get(lang, CATEGORIES[category]["en"]).keys())


def convert(category, lang, value, from_unit, to_unit):
    """Convert *value* from *from_unit* to *to_unit* inside *category*."""
    table = CATEGORIES[category].get(lang, CATEGORIES[category]["en"])
    base = value / table[from_unit]
    return base * table[to_unit]
