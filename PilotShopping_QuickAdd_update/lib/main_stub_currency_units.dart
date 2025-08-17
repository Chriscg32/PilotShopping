import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'models.dart';

void main() => runApp(const MaterialApp(home: Demo()));

class Demo extends StatefulWidget { const Demo({super.key}); @override State<Demo> createState() => _DemoState(); }
class _DemoState extends State<Demo> {
  String currencyCode = 'ZAR';
  final unitPriceCtrl = TextEditingController(text: '12.50');
  final quantityCtrl  = TextEditingController(text: '66');
  final ppkCtrl       = TextEditingController(text: '79.99');
  final weightCtrl    = TextEditingController(text: '5.00');

  String fmt(int cents) => NumberFormat.currency(
    locale: Intl.getCurrentLocale(), name: currencyCode).format(cents / 100);

  @override Widget build(BuildContext context) {
    final unitPrice = (double.tryParse(unitPriceCtrl.text.replaceAll(',', '.')) ?? 0.0);
    final qty       = int.tryParse(quantityCtrl.text) ?? 0;
    final eachTotal = (unitPrice * 100).round() * qty;

    final ppk   = (double.tryParse(ppkCtrl.text.replaceAll(',', '.')) ?? 0.0);
    final kg    = (double.tryParse(weightCtrl.text.replaceAll(',', '.')) ?? 0.0);
    final grams = (kg * 1000).round();
    final perKgTotal = ((ppk * 100).round() * grams) ~/ 1000;

    return Scaffold(
      appBar: AppBar(title: const Text('Currency & Units Demo')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(children: [
          const Text('Bulk (per unit)', style: TextStyle(fontWeight: FontWeight.bold)),
          TextField(controller: unitPriceCtrl, decoration: const InputDecoration(labelText: 'Unit price')),
          TextField(controller: quantityCtrl,  decoration: const InputDecoration(labelText: 'Quantity')),
          Text('Line total: '),
          const Divider(),
          const Text('Weight-based (per kg)', style: TextStyle(fontWeight: FontWeight.bold)),
          TextField(controller: ppkCtrl,    decoration: const InputDecoration(labelText: 'Price per kg')),
          TextField(controller: weightCtrl, decoration: const InputDecoration(labelText: 'Weight (kg)')),
          Text('Line total: '),
          const Divider(),
          const Text('Currency:'),
          Wrap(spacing: 8, children: [
            ChoiceChip(label: const Text('ZAR'), selected: currencyCode=='ZAR', onSelected: (_) => setState(()=>currencyCode='ZAR')),
            ChoiceChip(label: const Text('USD'), selected: currencyCode=='USD', onSelected: (_) => setState(()=>currencyCode='USD')),
            ChoiceChip(label: const Text('EUR'), selected: currencyCode=='EUR', onSelected: (_) => setState(()=>currencyCode='EUR')),
          ]),
        ]),
      ),
    );
  }
}
