import 'package:flutter/material.dart';

class AppTheme {
  // Light theme colors
  static const Color _lightPrimaryColor = Color(0xFF2196F3);
  static const Color _lightSecondaryColor = Color(0xFF03A9F4);
  static const Color _lightBackgroundColor = Color(0xFFF5F5F5);
  static const Color _lightSurfaceColor = Colors.white;
  static const Color _lightErrorColor = Color(0xFFB00020);

  // Dark theme colors
  static const Color _darkPrimaryColor = Color(0xFF1976D2);
  static const Color _darkSecondaryColor = Color(0xFF0288D1);
  static const Color _darkBackgroundColor = Color(0xFF121212);
  static const Color _darkSurfaceColor = Color(0xFF1E1E1E);
  static const Color _darkErrorColor = Color(0xFFCF6679);

  // Text themes
  static const TextTheme _textTheme = TextTheme(
    displayLarge: TextStyle(fontSize: 96, fontWeight: FontWeight.w300),
    displayMedium: TextStyle(fontSize: 60, fontWeight: FontWeight.w400),
    displaySmall: TextStyle(fontSize: 48, fontWeight: FontWeight.w400),
    headlineMedium: TextStyle(fontSize: 34, fontWeight: FontWeight.w400),
    headlineSmall: TextStyle(fontSize: 24, fontWeight: FontWeight.w400),
    titleLarge: TextStyle(fontSize: 20, fontWeight: FontWeight.w500),
    titleMedium: TextStyle(fontSize: 16, fontWeight: FontWeight.w400),
    titleSmall: TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
    bodyLarge: TextStyle(fontSize: 16, fontWeight: FontWeight.w400),
    bodyMedium: TextStyle(fontSize: 14, fontWeight: FontWeight.w400),
    bodySmall: TextStyle(fontSize: 12, fontWeight: FontWeight.w400),
    labelLarge: TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
  );

  // Light theme
  static final ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    colorScheme: const ColorScheme.light(
      primary: _lightPrimaryColor,
      secondary: _lightSecondaryColor,
      background: _lightBackgroundColor,
      surface: _lightSurfaceColor,
      error: _lightErrorColor,
    ),
    scaffoldBackgroundColor: _lightBackgroundColor,
    appBarTheme: const AppBarTheme(
      backgroundColor: _lightPrimaryColor,
      foregroundColor: Colors.white,
      elevation: 0,
    ),
    textTheme: _textTheme,
    inputDecorationTheme: InputDecorationTheme(
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      filled: true,
      fillColor: Colors.white,
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: _lightPrimaryColor,
        foregroundColor: Colors.white,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: _lightPrimaryColor,
        side: const BorderSide(color: _lightPrimaryColor),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
      ),
    ),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: Colors.white,
      selectedItemColor: _lightPrimaryColor,
      unselectedItemColor: Colors.grey,
    ),
    floatingActionButtonTheme: const FloatingActionButtonThemeData(
      backgroundColor: _lightPrimaryColor,
      foregroundColor: Colors.white,
    ),
  );

  // Dark theme
  static final ThemeData darkTheme = ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    colorScheme: const ColorScheme.dark(
      primary: _darkPrimaryColor,
      secondary: _darkSecondaryColor,
      background: _darkBackgroundColor,
      surface: _darkSurfaceColor,
      error: _darkErrorColor,
    ),
    scaffoldBackgroundColor: _darkBackgroundColor,
    appBarTheme: const AppBarTheme(
      backgroundColor: _darkSurfaceColor,
      foregroundColor: Colors.white,
      elevation: 0,
    ),
    textTheme: _textTheme,
    inputDecorationTheme: InputDecorationTheme(
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      filled: true,
      fillColor: _darkSurfaceColor,
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: _darkPrimaryColor,
        foregroundColor: Colors.white,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: _darkPrimaryColor,
        side: const BorderSide(color: _darkPrimaryColor),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
      ),
    ),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: _darkSurfaceColor,
      selectedItemColor: _darkPrimaryColor,
      unselectedItemColor: Colors.grey,
    ),
    floatingActionButtonTheme: const FloatingActionButtonThemeData(
      backgroundColor: _darkPrimaryColor,
      foregroundColor: Colors.white,
    ),
  );
}
