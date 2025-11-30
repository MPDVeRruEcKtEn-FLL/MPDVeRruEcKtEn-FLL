# Gyro-Funktionen Übersicht

[← Zurück: Berechnungen](Berechnungen) | [🏠 Home](Home)

---

Dieser Abschnitt beschreibt die Funktionen, die mit dem Gyrosensor genutzt werden.

---

## 📋 Inhalt

### Präzise Positionierung
- **[drive_distance()](Gyro-drive-distance)** - Fährt präzise Distanzen mit Gyro-Korrektur
- **[turn_to_angle()](Gyro-turn-to-angle)** - Dreht präzise auf einen Winkel

### Sensorbasierte Navigation
- **[turn_till_color()](Gyro-Sensorfunktionen#turn_till_color)** - Dreht bis Farbe erkannt
- **[turn_till_reflect()](Gyro-Sensorfunktionen#turn_till_reflect)** - Dreht bis Reflexion erkannt
- **[till_color()](Gyro-Sensorfunktionen#till_color)** - Fährt bis Farbe erkannt
- **[till_collide()](Gyro-Sensorfunktionen#till_collide)** - Fährt bis Kollision

### Tipps & Best Practices
- **[Tipps für optimale Performance](Gyro-Tipps)**

---

## Wann welche Funktion?

### ✅ Präzise Positionierung
Verwende diese Funktionen, wenn du exakte Distanzen oder Winkel benötigst:
- **drive_distance():** Für genaue Distanzen (z.B. "fahre 50cm")
- **turn_to_angle():** Für genaue Winkel (z.B. "drehe zu 90°")

### 🔍 Sensorbasierte Navigation
Verwende diese Funktionen, wenn du auf Umgebungsbedingungen reagieren möchtest:
- **till_color() / turn_till_color():** Für Farb- oder Linienerkennung
- **turn_till_reflect():** Für Hell-/Dunkel-Erkennung (besser für Linien)
- **till_collide():** Für Wanderkennung oder Positionsbestimmung

### 🔄 Kombinationen
Die Stärke liegt in der Kombination:

```python
# 1. Fahre zur Spielfeldkante
robot.drive_distance(distance=50, mainspeed=600)

# 2. Drehe dich zur Linie
robot.turn_to_angle(target_angle=90)

# 3. Fahre bis zur schwarzen Linie
robot.till_color(speed=400, color_type=3, color_gate=25)

# 4. Folge der Linie durch Drehen
robot.turn_till_color(direction=-1, color_type=0, color_gate=50)
```

---

## Detaillierte Funktionsbeschreibungen

Wähle eine Funktion für detaillierte Informationen:

### 🎯 [drive_distance()](Gyro-drive-distance)
- Funktionsweise & PID-Regelung
- Parameter-Erklärungen
- Beschleunigungs- & Bremsprofile
- Verwendungsbeispiele
- Re-Alignment

### 🔄 [turn_to_angle()](Gyro-turn-to-angle)
- Adaptive PID-Regelung
- Drehtypen (Tank, Links, Rechts)
- Parameter-Tuning Guide
- Smart Stop Mechanismus
- Global Turn Value

### 🌈 [Sensorfunktionen](Gyro-Sensorfunktionen)
- turn_till_color()
- turn_till_reflect()
- till_color()
- till_collide()

### 💡 [Tipps & Best Practices](Gyro-Tipps)
- PID-Tuning
- Geschwindigkeitswahl
- Timeout-Werte
- Sensor-Kalibrierung
- Global Turn Value Management

---

[← Zurück: Berechnungen](Berechnungen) | [🏠 Home](Home)
