import 'package:flutter/material.dart';
import '../../domain/models/models.dart';

class ShoppingListCard extends StatelessWidget {
  final ShoppingList shoppingList;
  final VoidCallback onTap;
  final VoidCallback? onLongPress;
  final VoidCallback? onEditPressed;
  final VoidCallback? onDeletePressed;

  const ShoppingListCard({
    Key? key,
    required this.shoppingList,
    required this.onTap,
    this.onLongPress,
    this.onEditPressed,
    this.onDeletePressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final completedItems = shoppingList.items.where((item) => item.isCompleted).length;
    final totalItems = shoppingList.items.length;
    final progress = totalItems > 0 ? completedItems / totalItems : 0.0;

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      child: InkWell(
        onTap: onTap,
        onLongPress: onLongPress,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      shoppingList.name,
                      style: theme.textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  Row(
                    children: [
                      if (onEditPressed != null)
                        IconButton(
                          icon: const Icon(Icons.edit),
                          onPressed: onEditPressed,
                          tooltip: "Edit",
                          constraints: const BoxConstraints(),
                          padding: const EdgeInsets.all(8),
                        ),
                      if (onDeletePressed != null)
                        IconButton(
                          icon: const Icon(Icons.delete),
                          onPressed: onDeletePressed,
                          tooltip: "Delete",
                          constraints: const BoxConstraints(),
                          padding: const EdgeInsets.all(8),
                        ),
                    ],
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                shoppingList.description ?? "",
                style: theme.textTheme.bodyMedium,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    "$completedItems of $totalItems items",
                    style: theme.textTheme.bodySmall,
                  ),
                  Text(
                    "Created: ${_formatDate(shoppingList.createdAt)}",
                    style: theme.textTheme.bodySmall,
                  ),
                ],
              ),
              const SizedBox(height: 8),
              LinearProgressIndicator(
                value: progress,
                backgroundColor: Colors.grey[300],
                valueColor: AlwaysStoppedAnimation<Color>(
                  progress == 1.0 ? Colors.green : theme.primaryColor,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _formatDate(DateTime date) {
    return "${date.day}/${date.month}/${date.year}";
  }
}
