import 'dart:io';
import 'package:flutter/material.dart';
import 'package:photo_view/photo_view.dart';

class ReceiptImageViewer extends StatelessWidget {
  final String imagePath;
  final bool isNetworkImage;

  const ReceiptImageViewer({
    Key? key,
    required this.imagePath,
    this.isNetworkImage = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Receipt Image"),
        actions: [
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {
              // TODO: Implement share functionality
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text("Share functionality coming soon")),
              );
            },
          ),
        ],
      ),
      body: Container(
        color: Colors.black,
        child: Center(
          child: PhotoView(
            imageProvider: isNetworkImage
                ? NetworkImage(imagePath)
                : FileImage(File(imagePath)) as ImageProvider,
            minScale: PhotoViewComputedScale.contained,
            maxScale: PhotoViewComputedScale.covered * 2,
            backgroundDecoration: const BoxDecoration(
              color: Colors.black,
            ),
            loadingBuilder: (context, event) => Center(
              child: CircularProgressIndicator(
                value: event == null
                    ? 0
                    : event.cumulativeBytesLoaded / (event.expectedTotalBytes ?? 1),
              ),
            ),
            errorBuilder: (context, error, stackTrace) => const Center(
              child: Icon(
                Icons.broken_image,
                color: Colors.white,
                size: 50,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
