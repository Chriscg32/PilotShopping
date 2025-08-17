# Spec — Bulk & Weight-based
Bulk (per unit)
- Inputs: quantity (int), unit_price_cents (int)
- line_total_cents = quantity × unit_price_cents
- UI: quantity stepper; max 1000

Per-kg
- Detect '/kg' or 'per kg'
- Inputs: weight_kg (0.01 precision) → weight_grams = round(kg × 1000)
- line_total_cents = (price_per_kg_cents × weight_grams) // 1000
- Presets: 0.5/1.0/2.0/5.0 kg

Storage & Edge
- unit in {each,kg}
- price_basis in {unit,per_kg}
- toggle for member vs normal price if multiple prices on tag
