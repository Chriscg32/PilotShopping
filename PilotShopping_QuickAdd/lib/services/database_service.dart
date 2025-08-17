import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/trip.dart';
import '../models/trip_item.dart';

/// Database service for managing local SQLite storage
class DatabaseService {
  static final DatabaseService _instance = DatabaseService._internal();
  static Database? _database;

  factory DatabaseService() {
    return _instance;
  }

  DatabaseService._internal();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    final path = await getDatabasesPath();
    final databasePath = join(path, 'pilot_shopping.db');

    return await openDatabase(
      databasePath,
      version: 1,
      onCreate: _onCreate,
    );
  }

  Future<void> _onCreate(Database db, int version) async {
    await db.execute('''
      CREATE TABLE trips (
        id TEXT PRIMARY KEY,
        store_name TEXT,
        store_branch TEXT,
        started_at TEXT NOT NULL,
        ended_at TEXT,
        budget_cents INTEGER NOT NULL,
        alert_gap_cents INTEGER NOT NULL,
        total_cents INTEGER NOT NULL DEFAULT 0,
        currency TEXT NOT NULL DEFAULT 'ZAR',
        status TEXT NOT NULL DEFAULT 'open',
        device_id TEXT NOT NULL,
        last_modified TEXT NOT NULL
      )
    ''');

    await db.execute('''
      CREATE TABLE trip_items (
        id TEXT PRIMARY KEY,
        trip_id TEXT NOT NULL,
        name TEXT NOT NULL,
        price_cents INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        source TEXT NOT NULL DEFAULT 'ocr',
        unit TEXT NOT NULL DEFAULT 'each',
        notes TEXT,
        created_at TEXT NOT NULL,
        last_modified TEXT NOT NULL
      )
    ''');
  }

  Future<String> insertTrip(Trip trip) async {
    final db = await database;
    await db.insert('trips', trip.toMap());
    return trip.id;
  }

  Future<List<Trip>> getAllTrips() async {
    final db = await database;
    final maps = await db.query('trips', orderBy: 'started_at DESC');
    return List.generate(maps.length, (i) => Trip.fromMap(maps[i]));
  }

  Future<List<TripItem>> getTripItems(String tripId) async {
    final db = await database;
    final maps = await db.query('trip_items', where: 'trip_id = ?', whereArgs: [tripId]);
    return List.generate(maps.length, (i) => TripItem.fromMap(maps[i]));
  }

  Future<String> insertTripItem(TripItem item) async {
    final db = await database;
    await db.insert('trip_items', item.toMap());
    return item.id;
  }

  Future<int> getTripTotal(String tripId) async {
    final db = await database;
    final result = await db.rawQuery(
      'SELECT SUM(price_cents * quantity) as total FROM trip_items WHERE trip_id = ?',
      [tripId],
    );
    return result.first['total'] as int? ?? 0;
  }

  Future<int> updateTrip(Trip trip) async {
    final db = await database;
    return await db.update(
      'trips',
      trip.toMap(),
      where: 'id = ?',
      whereArgs: [trip.id],
    );
  }

  Future<int> updateTripItem(TripItem item) async {
    final db = await database;
    return await db.update(
      'trip_items',
      item.toMap(),
      where: 'id = ?',
      whereArgs: [item.id],
    );
  }

  Future<int> deleteTrip(String tripId) async {
    final db = await database;
    return await db.delete(
      'trips',
      where: 'id = ?',
      whereArgs: [tripId],
    );
  }

  Future<int> deleteTripItem(String itemId) async {
    final db = await database;
    return await db.delete(
      'trip_items',
      where: 'id = ?',
      whereArgs: [itemId],
    );
  }

  Future<Trip?> getTrip(String tripId) async {
    final db = await database;
    final maps = await db.query(
      'trips',
      where: 'id = ?',
      whereArgs: [tripId],
      limit: 1,
    );
    if (maps.isNotEmpty) {
      return Trip.fromMap(maps.first);
    }
    return null;
  }

  Future<List<Trip>> getActiveTrips() async {
    final db = await database;
    final maps = await db.query(
      'trips',
      where: 'status = ?',
      whereArgs: ['open'],
      orderBy: 'started_at DESC',
    );
    return List.generate(maps.length, (i) => Trip.fromMap(maps[i]));
  }

  Future<void> clearAllData() async {
    final db = await database;
    await db.delete('trip_items');
    await db.delete('trips');
  }
}
