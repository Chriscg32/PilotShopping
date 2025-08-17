/// A helper class for parsing prices from text recognized by the OCR engine.
///
/// The shopping app relies on optical character recognition (OCR) to turn
/// shelf price tags into text. This service contains static methods to
/// extract structured data from those texts. In this MVP we only extract
/// the first numeric price that looks like a currency amount. Future
/// iterations might also parse item names or handle per‑kilogram pricing.
class OcrService {
  OcrService._();

  /// Extracts the most likely price in cents from the given [text]. Returns
  /// `null` if no valid price is found. Prices are expected to follow the
  /// pattern of one to four digits, optionally followed by a decimal
  /// separator (dot or comma) and exactly two decimal digits. An optional
  /// currency symbol (`R` for South African Rand) and whitespace may appear
  /// before the number.
  ///
  /// For example, the string "Special Offer R 29.99 Apples per kg" would
  /// return `2999`. If multiple prices are present, the largest value is
  /// returned since shelf tags sometimes show per‑unit and per‑kilogram
  /// prices together.
  static int? extractPrice(String text) {
    final regex = RegExp(r'(?:R\s*)?(\d{1,4}(?:[.,]\d{2})?)');
    final matches = regex.allMatches(text);
    if (matches.isEmpty) return null;
    // Convert each match into a numeric value in cents.
    final values = <int>[];
    for (final match in matches) {
      final group = match.group(1);
      if (group == null) continue;
      final normalized = group.replaceAll(',', '.');
      final value = double.tryParse(normalized);
      if (value != null) {
        values.add((value * 100).round());
      }
    }
    if (values.isEmpty) return null;
    // Choose the largest price. This heuristic helps when multiple prices are
    // printed on a tag (e.g. price per kg vs price per item).
    values.sort();
    return values.last;
  }
}