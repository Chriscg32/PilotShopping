import 'package:flutter/material.dart';
import '../models/trip.dart';
import '../models/trip_item.dart';
import '../services/database_service.dart';

class TripListScreen extends StatefulWidget {
  const TripListScreen({super.key});

  @override
  State<TripListScreen> createState() => _TripListScreenState();
}

class _TripListScreenState extends State<TripListScreen> {
  final DatabaseService _databaseService = DatabaseService();
  List<Trip> _trips = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadTrips();
  }

  Future<void> _loadTrips() async {
    setState(() => _isLoading = true);
    final trips = await _databaseService.getAllTrips();
    setState(() {
      _trips = trips;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('PilotShopping'),
        backgroundColor: Colors.blue,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _trips.isEmpty
              ? const Center(
                  child: Text('No trips yet. Tap + to start shopping!'),
                )
              : ListView.builder(
                  itemCount: _trips.length,
                  itemBuilder: (context, index) {
                    final trip = _trips[index];
                    return Card(
                      margin: const EdgeInsets.all(8),
                      child: ListTile(
                        title: Text(trip.storeName ?? 'Shopping Trip'),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Budget: ${trip.formattedBudget}'),
                            Text('Spent: ${trip.formattedTotal}'),
                            Text('Remaining: ${trip.formattedRemainingBudget}'),
                            Text(
                                'Started: ${trip.startedAt.toString().substring(0, 16)}'),
                          ],
                        ),
                        trailing: Chip(
                          label: Text(trip.status.toUpperCase()),
                          backgroundColor:
                              trip.status == 'open' ? Colors.green : Colors.grey,
                        ),
                        onTap: () => _navigateToTripDetails(trip),
                      ),
                    );
                  },
                ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _createNewTrip(),
        child: const Icon(Icons.add),
      ),
    );
  }

  void _navigateToTripDetails(Trip trip) {
    // Navigate to trip details screen
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => TripDetailsScreen(trip: trip),
      ),
    ).then((_) => _loadTrips());
  }

  void _createNewTrip() {
    // Navigate to create trip screen
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const CreateTripScreen(),
      ),
    ).then((_) => _loadTrips());
  }
}

class TripDetailsScreen extends StatefulWidget {
  final Trip trip;

  const TripDetailsScreen({super.key, required this.trip});

  @override
  State<TripDetailsScreen> createState() => _TripDetailsScreenState();
}

class _TripDetailsScreenState extends State<TripDetailsScreen> {
  final DatabaseService _databaseService = DatabaseService();
  List<TripItem> _items = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadTripItems();
  }

  Future<void> _loadTripItems() async {
    setState(() => _isLoading = true);
    final items = await _databaseService.getTripItems(widget.trip.id);
    setState(() {
      _items = items;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.trip.storeName ?? 'Trip Details'),
        actions: [
          if (widget.trip.status == 'open')
            IconButton(
              icon: const Icon(Icons.close),
              onPressed: () => _closeTrip(),
            ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        children: [
                          Text('Budget: ${widget.trip.formattedBudget}',
                              style: const TextStyle(fontSize: 18)),
                          Text('Spent: ${widget.trip.formattedTotal}',
                              style: const TextStyle(fontSize: 18)),
                          Text('Remaining: ${widget.trip.formattedRemainingBudget}',
                              style: TextStyle(
                                  fontSize: 18,
                                  color: widget.trip.remainingBudget < 0
                                      ? Colors.red
                                      : Colors.green)),
                          if (widget.trip.isBudgetThresholdReached())
                            const Padding(
                              padding: EdgeInsets.only(top: 8),
                              child: Text('⚠️ Budget threshold reached!',
                                  style: TextStyle(color: Colors.red)),
                            ),
                        ],
                      ),
                    ),
                  ),
                ),
                Expanded(
                  child: _items.isEmpty
                      ? const Center(child: Text('No items added yet'))
                      : ListView.builder(
                          itemCount: _items.length,
                          itemBuilder: (context, index) {
                            final item = _items[index];
                            return ListTile(
                              title: Text(item.name),
                              subtitle: Text(
                                  '${item.formattedPrice} x ${item.quantity} = ${item.formattedTotalPrice}'),
                              trailing: IconButton(
                                icon: const Icon(Icons.delete),
                                onPressed: () => _deleteItem(item),
                              ),
                            );
                          },
                        ),
                ),
              ],
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _addItem(),
        child: const Icon(Icons.add),
      ),
    );
  }

  void _addItem() {
    // Show add item dialog
    showDialog(
      context: context,
      builder: (context) => AddItemDialog(
        tripId: widget.trip.id,
        onItemAdded: _loadTripItems,
      ),
    );
  }

  void _deleteItem(TripItem item) async {
    await _databaseService.deleteTripItem(item.id);
    _loadTripItems();
  }

  void _closeTrip() async {
    final updatedTrip = widget.trip.closeTrip();
    await _databaseService.updateTrip(updatedTrip);
    Navigator.pop(context);
  }
}

class CreateTripScreen extends StatefulWidget {
  const CreateTripScreen({super.key});

  @override
  State<CreateTripScreen> createState() => _CreateTripScreenState();
}

class _CreateTripScreenState extends State<CreateTripScreen> {
  final _formKey = GlobalKey<FormState>();
  final _storeNameController = TextEditingController();
  final _storeBranchController = TextEditingController();
  final _budgetController = TextEditingController();
  final _alertGapController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Create New Trip')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _storeNameController,
                decoration: const InputDecoration(labelText: 'Store Name'),
                validator: (value) =>
                    value?.isEmpty ?? true ? 'Required' : null,
              ),
              TextFormField(
                controller: _storeBranchController,
                decoration: const InputDecoration(labelText: 'Store Branch'),
                validator: (value) =>
                    value?.isEmpty ?? true ? 'Required' : null,
              ),
              TextFormField(
                controller: _budgetController,
                decoration: const InputDecoration(
                    labelText: 'Budget (R)', prefixText: 'R'),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Required';
                  if (double.tryParse(value!) == null) return 'Invalid number';
                  return null;
                },
              ),
              TextFormField(
                controller: _alertGapController,
                decoration: const InputDecoration(
                    labelText: 'Alert Gap (R)', prefixText: 'R'),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Required';
                  if (double.tryParse(value!) == null) return 'Invalid number';
                  return null;
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _createTrip,
                child: const Text('Create Trip'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _createTrip() async {
    if (_formKey.currentState?.validate() ?? false) {
      final budget = (double.parse(_budgetController.text) * 100).toInt();
      final alertGap = (double.parse(_alertGapController.text) * 100).toInt();

      final trip = Trip.createNew(
        storeName: _storeNameController.text,
        storeBranch: _storeBranchController.text,
        budgetCents: budget,
        alertGapCents: alertGap,
        deviceId: 'device_001', // In real app, use device_info
      );

      await DatabaseService().insertTrip(trip);
      Navigator.pop(context);
    }
  }
}

class AddItemDialog extends StatefulWidget {
  final String tripId;
  final VoidCallback onItemAdded;

  const AddItemDialog({
    super.key,
    required this.tripId,
    required this.onItemAdded,
  });

  @override
  State<AddItemDialog> createState() => _AddItemDialogState();
}

class _AddItemDialogState extends State<AddItemDialog> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _priceController = TextEditingController();
  final _quantityController = TextEditingController(text: '1');

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Add Item'),
      content: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextFormField(
              controller: _nameController,
              decoration: const InputDecoration(labelText: 'Item Name'),
              validator: (value) =>
                  value?.isEmpty ?? true ? 'Required' : null,
            ),
            TextFormField(
              controller: _priceController,
              decoration: const InputDecoration(
                  labelText: 'Price (R)', prefixText: 'R'),
              keyboardType: TextInputType.number,
              validator: (value) {
                if (value?.isEmpty ?? true) return 'Required';
                if (double.tryParse(value!) == null) return 'Invalid number';
                return null;
              },
            ),
            TextFormField(
              controller: _quantityController,
              decoration: const InputDecoration(labelText: 'Quantity'),
              keyboardType: TextInputType.number,
              validator: (value) {
                if (value?.isEmpty ?? true) return 'Required';
                if (int.tryParse(value!) == null) return 'Invalid number';
                return null;
              },
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: _addItem,
          child: const Text('Add'),
        ),
      ],
    );
  }

  void _addItem() async {
    if (_formKey.currentState?.validate() ?? false) {
      final price = (double.parse(_priceController.text) * 100).toInt();
      final quantity = int.parse(_quantityController.text);

      final item = TripItem.createNew(
        tripId: widget.tripId,
        name: _nameController.text,
        priceCents: price,
        quantity: quantity,
      );

      await DatabaseService().insertTripItem(item);
      widget.onItemAdded();
      Navigator.pop(context);
    }
  }
}
