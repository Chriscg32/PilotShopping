import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../data/repositories/item_repository.dart';
import '../../../data/repositories/shopping_list_repository.dart';
import '../../../domain/models/item.dart';
import '../../../domain/models/shopping_list.dart';
import '../../../services/quick_add_service.dart';
import '../../widgets/common/custom_app_bar.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';
import '../../widgets/common/loading_indicator.dart';

class QuickAddScreen extends StatefulWidget {
  final String? barcode;
  final String? preSelectedShoppingListId;

  const QuickAddScreen({
    Key? key,
    this.barcode,
    this.preSelectedShoppingListId,
  }) : super(key: key);

  @override
  _QuickAddScreenState createState() => _QuickAddScreenState();
}

class _QuickAddScreenState extends State<QuickAddScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _notesController = TextEditingController();
  final _priceController = TextEditingController();
  final _barcodeController = TextEditingController();

  String? _selectedShoppingListId;
  bool _isLoading = false;
  bool _isFavorite = false;
  Item? _existingItem;

  @override
  void initState() {
    super.initState();
    _selectedShoppingListId = widget.preSelectedShoppingListId;
    _barcodeController.text = widget.barcode ?? '';
    _loadItemFromBarcode();
  }

  Future<void> _loadItemFromBarcode() async {
    if (widget.barcode != null && widget.barcode!.isNotEmpty) {
      setState(() => _isLoading = true);
      
      final quickAddService = context.read<QuickAddService>();
      final item = await quickAddService.getItemByBarcode(widget.barcode!);
      
      if (item != null) {
        _existingItem = item;
        _nameController.text = item.name;
        _notesController.text = item.notes ?? '';
        if (item.lastPrice != null) {
          _priceController.text = item.lastPrice.toString();
        }
        setState(() {
          _isFavorite = item.favoriteFlag;
        });
      }
      
      setState(() => _isLoading = false);
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _notesController.dispose();
    _priceController.dispose();
    _barcodeController.dispose();
    super.dispose();
  }

  Future<void> _scanBarcode() async {
    final quickAddService = context.read<QuickAddService>();
    final barcode = await quickAddService.scanBarcode();
    
    if (barcode != null) {
      _barcodeController.text = barcode;
      await _loadItemFromBarcode();
    }
  }

  Future<void> _saveAndAddToList() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final quickAddService = context.read<QuickAddService>();
      
      // Prepare barcodes list
      final List<String> barcodes = [];
      if (_barcodeController.text.isNotEmpty) {
        barcodes.add(_barcodeController.text);
      }
      if (_existingItem != null) {
        for (final code in _existingItem!.barcodes) {
          if (!barcodes.contains(code)) {
            barcodes.add(code);
          }
        }
      }
      
      // Parse price
      double? price;
      if (_priceController.text.isNotEmpty) {
        price = double.tryParse(_priceController.text);
      }
      
      // Create or update item
      final itemId = await quickAddService.createOrUpdateItem(
        id: _existingItem?.id,
        name: _nameController.text,
        barcodes: barcodes,
        notes: _notesController.text.isEmpty ? null : _notesController.text,
        lastPrice: price,
        favoriteFlag: _isFavorite,
      );
      
      // Add to shopping list if selected
      if (_selectedShoppingListId != null) {
        await quickAddService.quickAddItemToList(
          itemId: itemId,
          shoppingListId: _selectedShoppingListId!,
        );
      }
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Item added successfully!')),
        );
        Navigator.of(context).pop(true); // Return success
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: ${e.toString()}')),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final shoppingListRepository = Provider.of<ShoppingListRepository>(context);
    final shoppingLists = shoppingListRepository.getAllShoppingLists();
    
    return Scaffold(
      appBar: CustomAppBar(
        title: _existingItem != null ? 'Update Item' : 'Quick Add Item',
        actions: [
          IconButton(
            icon: Icon(_isFavorite ? Icons.favorite : Icons.favorite_border),
            onPressed: () {
              setState(() {
                _isFavorite = !_isFavorite;
              });
            },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: LoadingIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Barcode field with scan button
                    Row(
                      children: [
                        Expanded(
                          child: CustomTextField(
                            controller: _barcodeController,
                            labelText: 'Barcode',
                            keyboardType: TextInputType.text,
                            readOnly: true,
                          ),
                        ),
                        IconButton(
                          icon: const Icon(Icons.qr_code_scanner),
                          onPressed: _scanBarcode,
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    
                    // Name field
                    CustomTextField(
                      controller: _nameController,
                      labelText: 'Item Name',
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter an item name';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 16),
                    
                    // Price field
                    CustomTextField(
                      controller: _priceController,
                      labelText: 'Price',
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                    ),
                    const SizedBox(height: 16),
                    
                    // Notes field
                    CustomTextField(
                      controller: _notesController,
                      labelText: 'Notes',
                      maxLines: 3,
                    ),
                    const SizedBox(height: 24),
                    
                    // Shopping list dropdown
                    DropdownButtonFormField<String>(
                      decoration: const InputDecoration(
                        labelText: 'Add to Shopping List',
                        border: OutlineInputBorder(),
                      ),
                      value: _selectedShoppingListId,
                      items: [
                        const DropdownMenuItem<String>(
                          value: null,
                          child: Text('None'),
                        ),
                        ...shoppingLists.map((list) => DropdownMenuItem<String>(
                              value: list.id,
                              child: Text(list.name),
                            )),
                      ],
                      onChanged: (value) {
                        setState(() {
                          _selectedShoppingListId = value;
                        });
                      },
                    ),
                    const SizedBox(height: 32),
                    
                    // Save button
                    CustomButton(
                      text: 'Save & Add to List',
                      onPressed: _saveAndAddToList,
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}
