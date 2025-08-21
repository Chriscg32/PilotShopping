import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../domain/models/models.dart';
import '../common/common_widgets.dart';

class ReceiptCard extends StatelessWidget {
  final Receipt receipt;
  final VoidCallback? onTap;
  final VoidCallback? onDelete;
  final VoidCallback? onEdit;

  const ReceiptCard({
    Key? key,
    required this.receipt,
    this.onTap,
    this.onDelete,
    this.onEdit,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final dateFormat = DateFormat('MMM dd, yyyy');
    final currencyFormat = NumberFormat.currency(symbol: '\$');
    
    return Card(
      elevation: 2,
      margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      receipt.store ?? 'Unknown Store',
                      style: theme.textTheme.titleLarge,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  Text(
                    currencyFormat.format(receipt.total),
                    style: theme.textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: theme.colorScheme.primary,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                dateFormat.format(receipt.date),
                style: theme.textTheme.bodyMedium,
              ),
              if (receipt.notes != null && receipt.notes!.isNotEmpty) ...[  
                const SizedBox(height: 8),
                Text(
                  receipt.notes!,
                  style: theme.textTheme.bodyMedium,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  if (receipt.imageUrl != null) ...[  
                    Icon(
                      Icons.image,
                      size: 18,
                      color: theme.colorScheme.secondary,
                    ),
                    const SizedBox(width: 8),
                  ],
                  if (onEdit != null) ...[  
                    IconButton(
                      icon: Icon(
                        Icons.edit,
                        color: theme.colorScheme.primary,
                      ),
                      onPressed: onEdit,
                      constraints: const BoxConstraints(),
                      padding: const EdgeInsets.all(8),
                    ),
                  ],
                  if (onDelete != null) ...[  
                    IconButton(
                      icon: Icon(
                        Icons.delete,
                        color: theme.colorScheme.error,
                      ),
                      onPressed: () {
                        ConfirmationDialog.show(
                          context,
                          title: 'Delete Receipt',
                          message: 'Are you sure you want to delete this receipt?',
                          confirmText: 'Delete',
                          onConfirm: onDelete,
                          confirmColor: theme.colorScheme.error,
                        );
                      },
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
