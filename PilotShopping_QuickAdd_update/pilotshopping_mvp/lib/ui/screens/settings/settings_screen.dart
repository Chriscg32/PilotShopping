import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../data/repositories/settings_repository.dart';
import '../../widgets/common/custom_app_bar.dart';
import '../../widgets/common/custom_button.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);
    final settingsRepository = Provider.of<SettingsRepository>(context);
    final settings = settingsRepository.getSettings();

    return Scaffold(
      appBar: const CustomAppBar(title: 'Settings'),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          // Theme settings
          _buildSectionHeader(context, 'Appearance'),
          SwitchListTile(
            title: const Text('Dark Mode'),
            value: themeProvider.themeMode == ThemeMode.dark,
            onChanged: (value) {
              themeProvider.toggleThemeMode();
            },
          ),
          const Divider(),

          // Currency settings
          _buildSectionHeader(context, 'General'),
          ListTile(
            title: const Text('Currency'),
            subtitle: Text(settings.defaultCurrency),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
              // TODO: Implement currency selection
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Currency selection coming soon!')),
              );
            },
          ),
          SwitchListTile(
            title: const Text('Show Price History'),
            subtitle: const Text('Display price history for items'),
            value: settings.showPriceHistory,
            onChanged: (value) async {
              final newSettings = settings.copyWith(showPriceHistory: value);
              await settingsRepository.saveSettings(newSettings);
              // Force rebuild
              if (context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Settings updated')),
                );
              }
            },
          ),
          const Divider(),

          // About section
          _buildSectionHeader(context, 'About'),
          ListTile(
            title: const Text('Version'),
            subtitle: const Text('1.0.0'),
          ),
          ListTile(
            title: const Text('Terms of Service'),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
              // TODO: Navigate to terms of service
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Terms of Service coming soon!')),
              );
            },
          ),
          ListTile(
            title: const Text('Privacy Policy'),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
              // TODO: Navigate to privacy policy
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Privacy Policy coming soon!')),
              );
            },
          ),
          const SizedBox(height: 24),

          // Reset settings button
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: CustomButton(
              text: 'Reset All Settings',
              onPressed: () async {
                final confirmed = await _showResetConfirmationDialog(context);
                if (confirmed == true) {
                  await settingsRepository.resetSettings();
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Settings have been reset')),
                    );
                  }
                }
              },
              isOutlined: true,
              color: Colors.red,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(BuildContext context, String title) {
    return Padding(
      padding: const EdgeInsets.only(top: 16.0, bottom: 8.0, left: 16.0, right: 16.0),
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.primary,
            ),
      ),
    );
  }

  Future<bool?> _showResetConfirmationDialog(BuildContext context) {
    return showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Reset Settings?'),
        content: const Text(
            'This will reset all settings to their default values. This action cannot be undone.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('CANCEL'),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(true),
            child: const Text('RESET'),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
          ),
        ],
      ),
    );
  }
}
