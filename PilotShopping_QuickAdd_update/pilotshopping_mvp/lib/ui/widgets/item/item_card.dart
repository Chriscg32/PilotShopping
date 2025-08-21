import 'package:flutter/material.dart';
import '../../domain/models/models.dart';

class ItemCard extends StatelessWidget {
  final Item item;
  final VoidCallback onTap;
  final VoidCallback? onLongPress;
  final VoidCallback? onFavoritePressed;
  final VoidCallback? onAddToListPressed;

  const ItemCard({
    Key? key,
    required this.item,
    required this.onTap,
    this.onLongPress,
    this.onFavoritePressed,
    this.onAddToListPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      child: InkWell(
        onTap: onTap,
        onLongPress: onLongPress,
        child: Padding(
          padding: const EdgeInsets.all(12.0),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Item image or placeholder
              Container(
                width: 80,
                height: 80,
                decoration: BoxDecoration(
                  color: theme.colorScheme.primaryContainer,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: item.imageUrl != null && item.imageUrl!.isNotEmpty
                    ? ClipRRect(
                        borderRadius: BorderRadius.circular(8),
                        child: Image.network(
                          item.imageUrl!,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) {
                            return Center(
                              child: Text(
                                item.name.substring(0, 1).toUpperCase(),
                                style: TextStyle(
                                  color: theme.colorScheme.onPrimaryContainer,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 24,
                                ),
                              ),
                            );
                          },
                        ),
                      )
                    : Center(
                        child: Text(
                          item.name.substring(0, 1).toUpperCase(),
                          style: TextStyle(
                            color: theme.colorScheme.onPrimaryContainer,
                            fontWeight: FontWeight.bold,
                            fontSize: 24,
                          ),
                        ),
                      ),
              ),
              const SizedBox(width: 16),
              // Item details
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      item.name,
                      style: theme.textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    if (item.description != null && item.description!.isNotEmpty) ...[  
                      const SizedBox(height: 4),
                      Text(
                        item.description!,
                        style: theme.textTheme.bodyMedium,
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        if (item.barcode != null && item.barcode!.isNotEmpty) ...[  
                          Icon(
                            Icons.qr_code,
                            size: 16,
                            color: theme.colorScheme.secondary,
                          ),
                          const SizedBox(width: 4),
                          Expanded(
                            child: Text(
                              item.barcode!,
                              style: theme.textTheme.bodySmall,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ],
                    ),
                    if (item.price > 0) ...[  
                      const SizedBox(height: 4),
                      Text(
                        "\$${item.price.toStringAsFixed(2)}",
                        style: theme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                          color: theme.colorScheme.primary,
                        ),
                      ),
                    ],
                  ],
                ),
              ),
              // Action buttons
              Column(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  if (onFavoritePressed != null)
                    IconButton(
                      icon: Icon(
                        item.isFavorite ? Icons.favorite : Icons.favorite_border,
                        color: item.isFavorite ? Colors.red : null,
                      ),
                      onPressed: onFavoritePressed,
                      tooltip: "Favorite",
                      constraints: const BoxConstraints(),
                      padding: const EdgeInsets.all(8),
                    ),
                  if (onAddToListPressed != null) ...[  
                    const SizedBox(height: 8),
                    IconButton(
                      icon: const Icon(Icons.add_shopping_cart),
                      onPressed: onAddToListPressed,
                      tooltip: "Add to List",
                      constraints: const BoxConstraints(),
                      padding: const EdgeInsets.all(8),
                    ),
                  ],
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
