# DriveBase Dokumentation / Documentation

Willkommen zur DriveBase Dokumentation für LEGO SPIKE Prime / Robot Inventor!

Welcome to the DriveBase documentation for LEGO SPIKE Prime / Robot Inventor!

---

## 🇩🇪 Deutsche Dokumentation

### Hauptkapitel

1. **[Konfiguration](Konfiguration)** - DriveBase einrichten und konfigurieren
2. **[Einfache Motorinteraktionen](Einfache-Motorinteraktionen)** - Grundlegende Motorfunktionen
3. **[Berechnungen](Berechnungen)** - Hilfsfunktionen und Berechnungen
4. **[Gyro-Funktionen](Gyro-Funktionen)** - Erweiterte Navigation mit Gyrosensor
   - [drive_distance()](Gyro-drive-distance)
   - [turn_to_angle()](Gyro-turn-to-angle)
   - [Sensorfunktionen](Gyro-Sensorfunktionen)
   - [Tipps & Best Practices](Gyro-Tipps)

---

## 🇬🇧 English Documentation

### Main Chapters

1. **[Configuration](Configuration-EN)** - Set up and configure DriveBase
2. **[Simple Motor Interactions](Simple-Motor-Interactions-EN)** - Basic motor functions
3. **[Calculations](Calculations-EN)** - Helper functions and calculations
4. **[Gyro Functions](Gyro-Functions-EN)** - Advanced navigation with gyro sensor
   - [drive_distance()](Gyro-drive-distance-EN)
   - [turn_to_angle()](Gyro-turn-to-angle-EN)
   - [Sensor Functions](Gyro-Sensor-Functions-EN)
   - [Tips & Best Practices](Gyro-Tips-EN)

---

## 📦 Repository Info

- **Repository:** [MPDVeRruEcKtEn-FirstLegoLeague](https://github.com/Leolion2023/MPDVeRruEcKtEn-FirstLegoLeague)
- **Lizenz / License:** Siehe / See [LICENSE](https://github.com/Leolion2023/MPDVeRruEcKtEn-FirstLegoLeague/blob/main/LICENSE)
- **Code of Conduct:** [CODE_OF_CONDUCT.md](https://github.com/Leolion2023/MPDVeRruEcKtEn-FirstLegoLeague/blob/main/CODE_OF_CONDUCT.md)

---

## 🚀 Schnellstart / Quick Start

**Deutsch:**
```python
from DriveBase import DriveBase

# Roboter initialisieren
robot = DriveBase()

# 50cm vorwärts fahren
robot.drive_distance(distance=50, mainspeed=600)

# 90° nach rechts drehen
robot.turn_to_angle(target_angle=90)
```

**English:**
```python
from DriveBase import DriveBase

# Initialize robot
robot = DriveBase()

# Drive 50cm forward
robot.drive_distance(distance=50, mainspeed=600)

# Turn 90° to the right
robot.turn_to_angle(target_angle=90)
```
