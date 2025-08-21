import 'package:flutter/material.dart';
import '../../domain/models/models.dart';

class ShoppingListItemWidget extends StatelessWidget {
  final Item item;
  final bool isSelected;
  final VoidCallback onTap;
  final VoidCallback? onLongPress;
  final bool showCheckbox;
  final Function(bool?)? onCheckChanged;

  const ShoppingListItemWidget({
    Key? key,
    required this.item,
    this.isSelected = false,
    required this.onTap,
    this.onLongPress,
    this.showCheckbox = false,
    this.onCheckChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: isSelected ? 4 : 1,
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      color: isSelected ? Theme.of(context).colorScheme.primaryContainer : null,
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        leading: item.imageUrl != null && item.imageUrl!.isNotEmpty
            ? CircleAvatar(
                backgroundImage: NetworkImage(item.imageUrl!),
                radius: 24,
              )
            : CircleAvatar(
                backgroundColor: Theme.of(context).primaryColor,
                radius: 24,
                child: Text(
                  item.name.substring(0, 1).toUpperCase(),
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
        title: Text(
          item.name,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            decoration: item.isCompleted ? TextDecoration.lineThrough : null,
          ),
        ),
        subtitle: item.description != null && item.description!.isNotEmpty
            ? Text(
                item.description!,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              )
            : null,
        trailing: showCheckbox
            ? Checkbox(
                value: item.isCompleted,
                onChanged: onCheckChanged,
              )
            : item.price > 0
                ? Text(
                    "\$${item.price.toStringAsFixed(2)}",
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                    ),
                  )
                : null,
        onTap: onTap,
        onLongPress: onLongPress,
      ),
    );
  }
}
