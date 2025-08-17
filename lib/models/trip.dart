/// Trip data model for PilotShopping app
/// Represents a shopping trip with budget tracking and receipt management

class Trip {
  final String id;
  final String? storeName;
  final String? storeBranch;
  final DateTime startedAt;
  final DateTime? endedAt;
  final int budgetCents;
  final int alertGapCents;
  final int totalCents;
  final String currency;
  final String status;
  final String deviceId;
  final DateTime lastModified;

  Trip({
    required this.id,
    this.storeName,
    this.storeBranch,
    required this.startedAt,
    this.endedAt,
    required this.budgetCents,
    required this.alertGapCents,
    required this.totalCents,
    this.currency = 'ZAR',
    this.status = 'open',
    required this.deviceId,
    required this.lastModified,
  });

  /// Convert Trip object to Map for database storage
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'store_name': storeName,
      'store_branch': storeBranch,
      'started_at': startedAt.toIso8601String(),
      'ended_at': endedAt?.toIso8601String(),
      'budget_cents': budgetCents,
      'alert_gap_cents': alertGapCents,
      'total_cents': totalCents,
      'currency': currency,
      'status': status,
      'device_id': deviceId,
      'last_modified': lastModified.toIso8601String(),
    };
  }

  /// Create Trip object from Map (database retrieval)
  factory Trip.fromMap(Map<String, dynamic> map) {
    return Trip(
      id: map['id'],
      storeName: map['store_name'],
      storeBranch: map['store_branch'],
      startedAt: DateTime.parse(map['started_at']),
      endedAt: map['ended_at'] != null ? DateTime.parse(map['ended_at']) : null,
      budgetCents: map['budget_cents'],
      alertGapCents: map['alert_gap_cents'],
      totalCents: map['total_cents'],
      currency: map['currency'] ?? 'ZAR',
      status: map['status'] ?? 'open',
      deviceId: map['device_id'],
      lastModified: DateTime.parse(map['last_modified']),
    );
  }

  /// Create a new trip with default values
  factory Trip.createNew({
    required String storeName,
    required String storeBranch,
    required int budgetCents,
    required int alertGapCents,
    required String deviceId,
  }) {
    final now = DateTime.now();
    return Trip(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      storeName: storeName,
      storeBranch: storeBranch,
      startedAt: now,
      budgetCents: budgetCents,
      alertGapCents: alertGapCents,
      totalCents: 0,
      deviceId: deviceId,
      lastModified: now,
    );
  }

  /// Update trip status to closed
  Trip closeTrip() {
    final now = DateTime.now();
    return Trip(
      id: id,
      storeName: storeName,
      storeBranch: storeBranch,
      startedAt: startedAt,
      endedAt: now,
      budgetCents: budgetCents,
      alertGapCents: alertGapCents,
      totalCents: totalCents,
      currency: currency,
      status: 'closed',
      deviceId: deviceId,
      lastModified: now,
    );
  }

  /// Update total amount
  Trip updateTotal(int newTotalCents) {
    final now = DateTime.now();
    return Trip(
      id: id,
      storeName: storeName,
      storeBranch: storeBranch,
      startedAt: startedAt,
      endedAt: endedAt,
      budgetCents: budgetCents,
      alertGapCents: alertGapCents,
      totalCents: newTotalCents,
      currency: currency,
      status: status,
      deviceId: deviceId,
      lastModified: now,
    );
  }

  /// Check if budget threshold is reached
  bool isBudgetThresholdReached() {
    return totalCents >= (budgetCents - alertGapCents);
  }

  /// Get remaining budget
  int get remainingBudget => budgetCents - totalCents;

  /// Get formatted remaining budget
  String get formattedRemainingBudget {
    return 'R${(remainingBudget / 100).toStringAsFixed(2)}';
  }

  /// Get formatted total
  String get formattedTotal {
    return 'R${(totalCents / 100).toStringAsFixed(2)}';
  }

  /// Get formatted budget
  String get formattedBudget {
    return 'R${(budgetCents / 100).toStringAsFixed(2)}';
  }

  /// Get formatted alert gap
  String get formattedAlertGap {
    return 'R${(alertGapCents / 100).toStringAsFixed(2)}';
  }
}
