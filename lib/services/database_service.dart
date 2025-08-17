import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/trip.dart';
import '../models/trip_item.dart';

class DatabaseService {
  static Database? _database;
  static final DatabaseService instance = DatabaseService._();

  DatabaseService._();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB();
    return _database!;
  }

  Future<Database> _initDB() async {
    String path = join(await getDatabasesPath(), 'shopping_database.db');
    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDB,
    );
  }

  Future<void> _createDB(Database db, int version) async {
    await db.execute('''
      CREATE TABLE trips(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        budget REAL,
        totalCost REAL
      )
    ''');
    await db.execute('''
      CREATE TABLE trip_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tripId INTEGER,
        name TEXT,
        price REAL,
        quantity INTEGER,
        FOREIGN KEY (tripId) REFERENCES trips(id) ON DELETE CASCADE
      )
    ''');
  }

  // Trip operations
  Future<int> insertTrip(Trip trip) async {
    Database db = await database;
    return await db.insert('trips', trip.toMap());
  }

  Future<List<Trip>> getTrips() async {
    Database db = await database;
    final List<Map<String, dynamic>> maps = await db.query('trips');
    return List.generate(maps.length, (i) {
      return Trip.fromMap(maps[i]);
    });
  }

  Future<int> updateTrip(Trip trip) async {
    Database db = await database;
    return await db.update('trips', trip.toMap(), where: 'id = ?', whereArgs: [trip.id]);
  }

  Future<int> deleteTrip(int id) async {
    Database db = await database;
    return await db.delete('trips', where: 'id = ?', whereArgs: [id]);
  }

  // TripItem operations
  Future<int> insertTripItem(TripItem item) async {
    Database db = await database;
    return await db.insert('trip_items', item.toMap());
  }

  Future<List<TripItem>> getTripItems(int tripId) async {
    Database db = await database;
    final List<Map<String, dynamic>> maps = await db.query('trip_items', where: 'tripId = ?', whereArgs: [tripId]);
    return List.generate(maps.length, (i) {
      return TripItem.fromMap(maps[i]);
    });
  }

  Future<int> updateTripItem(TripItem item) async {
    Database db = await database;
    return await db.update('trip_items', item.toMap(), where: 'id = ?', whereArgs: [item.id]);
  }

  Future<int> deleteTripItem(int id) async {
    Database db = await database;
    return await db.delete('trip_items', where: 'id = ?', whereArgs: [id]);
  }
}