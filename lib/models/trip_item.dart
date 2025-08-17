/// TripItem data model for PilotShopping app
/// Represents individual items added to a shopping trip

class TripItem {
  final String id;
  final String tripId;
  final String name;
  final int priceCents;
  final int quantity;
  final String source;
  final String unit;
  final String? notes;
  final DateTime createdAt;
  final DateTime lastModified;

  TripItem({
    required this.id,
    required this.tripId,
    required this.name,
    required this.priceCents,
    this.quantity = 1,
    this.source = 'ocr',
    this.unit = 'each',
    this.notes,
    required this.createdAt,
    required this.lastModified,
  });

  /// Convert TripItem object to Map for database storage
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'trip_id': tripId,
      'name': name,
      'price_cents': priceCents,
      'quantity': quantity,
      'source': source,
      'unit': unit,
      'notes': notes,
      'created_at': createdAt.toIso8601String(),
      'last_modified': lastModified.toIso8601String(),
    };
  }

  /// Create TripItem object from Map (database retrieval)
  factory TripItem.fromMap(Map<String, dynamic> map) {
    return TripItem(
      id: map['id'],
      tripId: map['trip_id'],
      name: map['name'],
      priceCents: map['price_cents'],
      quantity: map['quantity'] ?? 1,
      source: map['source'] ?? 'ocr',
      unit: map['unit'] ?? 'each',
      notes: map['notes'],
      createdAt: DateTime.parse(map['created_at']),
      lastModified: DateTime.parse(map['last_modified']),
    );
  }

  /// Create a new trip item
  factory TripItem.createNew({
    required String tripId,
    required String name,
    required int priceCents,
    int quantity = 1,
    String source = 'ocr',
    String unit = 'each',
    String? notes,
  }) {
    final now = DateTime.now();
    return TripItem(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      tripId: tripId,
      name: name,
      priceCents: priceCents,
      quantity: quantity,
      source: source,
      unit: unit,
      notes: notes,
      createdAt: now,
      lastModified: now,
    );
  }

  /// Update item details
  TripItem update({
    String? name,
    int? priceCents,
    int? quantity,
    String? notes,
  }) {
    final now = DateTime.now();
    return TripItem(
      id: id,
      tripId: tripId,
      name: name ?? this.name,
      priceCents: priceCents ?? this.priceCents,
      quantity: quantity ?? this.quantity,
      source: source,
      unit: unit,
      notes: notes ?? this.notes,
      createdAt: createdAt,
      lastModified: now,
    );
  }

  /// Get formatted price
  String get formattedPrice {
    return 'R${(priceCents / 100).toStringAsFixed(2)}';
  }

  /// Get total price for this item (price * quantity)
  int get totalPriceCents => priceCents * quantity;

  /// Get formatted total price
  String get formattedTotalPrice {
    return 'R${(totalPriceCents / 100).toStringAsFixed(2)}';
  }

  /// Get source display name
  String get sourceDisplayName {
    switch (source) {
      case 'ocr':
        return 'Scanned';
      case 'manual':
        return 'Manual Entry';
      case 'barcode':
        return 'Barcode';
      default:
        return source;
    }
  }

  /// Get unit display name
  String get unitDisplayName {
    switch (unit) {
      case 'each':
        return 'Each';
      case 'kg':
        return 'Per kg';
      case 'L':
        return 'Per L';
      case 'other':
        return 'Other';
      default:
        return unit;
    }
  }
}
