enum ItemUnit { each, kg }

class TripItem {
  final String id, name;
  final ItemUnit unit;
  final int quantity;     // when each
  final int weightGrams;  // when kg
  final int unitPriceCents;
  final bool priceIsPerKg;
  final int lineTotalCents;

  TripItem.each({
    required this.id,
    required this.name,
    required this.unitPriceCents,
    required this.quantity,
  }) : unit = ItemUnit.each,
       weightGrams = 0,
       priceIsPerKg = false,
       lineTotalCents = unitPriceCents * quantity;

  TripItem.perKg({
    required this.id,
    required this.name,
    required int pricePerKgCents,
    required this.weightGrams,
  }) : unit = ItemUnit.kg,
       quantity = 0,
       priceIsPerKg = true,
       unitPriceCents = pricePerKgCents,
       lineTotalCents = (pricePerKgCents * weightGrams) ~/ 1000;
}
