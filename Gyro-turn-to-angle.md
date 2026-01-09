# turn_to_angle()

[← Zurück: drive_distance()](Gyro-drive-distance) | [🏠 Home](Home) | [Weiter: Sensorfunktionen →](Gyro-Sensorfunktionen)

---

## Überblick

Die `turn_to_angle()` Funktion dreht den Roboter präzise zu einem absoluten Winkel. Sie nutzt adaptive PID-Regelung, die sich automatisch an die Größe der Drehung anpasst, und implementiert verschiedene Drehtypen (Tank, Links, Rechts).

---

## Parameter

### target_angle (int, default: 0) [°]
Der absolute Zielwinkel in Grad.
- **0°:** Ausgangsposition (wo der Roboter gestartet wurde)
- **90°:** 90° rechts von der Ausgangsposition
- **-90°:** 90° links von der Ausgangsposition
- **180° / -180°:** Komplett umdrehen

**Wichtig:** Die Funktion dreht immer auf den kürzesten Weg zum Zielwinkel.

### speed (int, default: 300) [°/s]
Die Drehgeschwindigkeit. 
- **200-400:** Langsam und präzise
- **400-600:** Standard-Geschwindigkeit
- **600-800:** Schnell (weniger präzise)

### type (int, default: 0)
Bestimmt die Art der Drehung:
- **0:** Tank Turn (beide Räder drehen in entgegengesetzte Richtungen)
- **1:** Links fixiert (nur rechtes Rad dreht)
- **2:** Rechts fixiert (nur linkes Rad dreht)

### threshold (float, default: 0.5) [°]
Genauigkeitsschwelle - wie nah am Zielwinkel muss der Roboter sein?
- **0.5°:** Standard-Präzision
- **0.1°:** Sehr präzise (langsamer)
- **1.0°:** Weniger präzise (schneller)

### timeout (int, default: 5000) [ms]
Maximale Zeit für die Drehung. Verhindert endlose Oszillation.
- **3000:** Schnelle Drehungen
- **5000:** Standard
- **10000:** Für sehr präzise/langsame Drehungen

### timestep (int, default: 50) [ms]
Zeitintervall zwischen PID-Berechnungen.
- **30-50:** Sehr reaktiv
- **50-100:** Standard
- **100-200:** Langsamer, stabiler

---

## Funktionsweise im Detail

### 1. Winkelberechnung

```python
# Aktuellen Winkel vom Gyro lesen
current_angle = gyro.yaw_angle()

# Fehler berechnen
error = target_angle - current_angle

# Kürzesten Weg finden
if error > 180:
    error -= 360
elif error < -180:
    error += 360
```

**Beispiel:**
- Aktuell: 170°
- Ziel: -170°
- Naiver Fehler: -340°
- Korrigierter Fehler: 20° (kürzester Weg)

### 2. Adaptive PID-Regelung

Die Funktion passt die PID-Parameter automatisch an die Drehgröße an:

```python
def get_pids(error):
    if abs(error) > 45:
        # Große Drehung: Schnell aber stabil
        return (4.0, 0.01, 15.0)  # (P, I, D)
    elif abs(error) > 10:
        # Mittlere Drehung: Ausgewogen
        return (3.5, 0.02, 12.0)
    else:
        # Kleine Drehung: Präzise
        return (3.0, 0.03, 10.0)
```

**PID-Komponenten:**

#### P (Proportional): Hauptantrieb
```python
P_component = error * P_gain
```
Je größer der Fehler, desto schneller die Drehung.

#### I (Integral): Langzeit-Korrektur
```python
integral += error * timestep
I_component = integral * I_gain
```
Korrigiert kleine, dauerhafte Abweichungen.

#### D (Derivative): Dämpfung
```python
derivative = (error - old_error) / timestep
D_component = derivative * D_gain
```
Verhindert Überschwingen und Oszillation.

**Gesamtsteuerung:**
```python
steering = P_component + I_component + D_component
steering = max(-100, min(100, steering))  # Begrenzen auf ±100
```

### 3. Drehtypen

#### Type 0: Tank Turn (Standard)
```python
# Beide Räder drehen entgegengesetzt
left_speed = speed * (steering / 100)
right_speed = -speed * (steering / 100)
```

**Vorteil:** Schnell, dreht auf der Stelle
**Nachteil:** Kann Position leicht verschieben

#### Type 1: Links fixiert
```python
# Nur rechtes Rad dreht
left_speed = 0
right_speed = speed * (steering / 100)
```

**Vorteil:** Position bleibt konstant (links)
**Nachteil:** Langsamer, größerer Radius

#### Type 2: Rechts fixiert
```python
# Nur linkes Rad dreht
left_speed = speed * (steering / 100)
right_speed = 0
```

**Vorteil:** Position bleibt konstant (rechts)
**Nachteil:** Langsamer, größerer Radius

### 4. Smart Stop Mechanismus

```python
# Stoppe wenn:
# 1. Innerhalb der Schwelle UND
# 2. Geschwindigkeit nahe Null UND
# 3. Mindestens 100ms stabil

if abs(error) < threshold:
    if avg_speed < 5:  # Praktisch still
        stable_count += 1
        if stable_count >= 2:  # 2 × 50ms = 100ms
            break
```

Dies verhindert:
- Vorzeitiges Stoppen bei Durchschwingen
- Oszillation um den Zielpunkt
- Unruhiges Verhalten

### 5. Global Turn Value Update

```python
# Am Ende: Speichere tatsächlichen Winkel
global global_turn_value
global_turn_value = gyro.yaw_angle()
```

Dieser Wert wird von anderen Funktionen als Referenz genutzt.

---

## Verwendungsbeispiele

### Einfache Drehungen
```python
# 90° nach rechts drehen
robot.turn_to_angle(target_angle=90)

# 90° nach links drehen
robot.turn_to_angle(target_angle=-90)

# Zurück zur Startposition
robot.turn_to_angle(target_angle=0)

# 180° umdrehen
robot.turn_to_angle(target_angle=180)
```

### Präzise Drehung
```python
# Sehr genau auf 45° drehen
robot.turn_to_angle(
    target_angle=45,
    speed=250,          # Langsam
    threshold=0.2,      # Sehr genau
    timeout=8000        # Mehr Zeit
)
```

### Schnelle Drehung
```python
# Schnell auf -90° drehen
robot.turn_to_angle(
    target_angle=-90,
    speed=600,          # Schnell
    threshold=1.0,      # Weniger genau
    timeout=3000
)
```

### Drehung mit fixiertem Rad
```python
# Linkes Rad fixiert (z.B. an Wand)
robot.turn_to_angle(
    target_angle=90,
    type=1,             # Links fixiert
    speed=300
)

# Rechtes Rad fixiert
robot.turn_to_angle(
    target_angle=-45,
    type=2,             # Rechts fixiert
    speed=300
)
```

### Sequentielle Navigation
```python
# Komplexe Fahrt mit mehreren Drehungen
robot.drive_distance(distance=50, mainspeed=600)
robot.turn_to_angle(target_angle=90)
robot.drive_distance(distance=30, mainspeed=600)
robot.turn_to_angle(target_angle=180)
robot.drive_distance(distance=50, mainspeed=600)
robot.turn_to_angle(target_angle=0)  # Zurück zur Start-Ausrichtung
```

### Winkel-Reset
```python
# Gyro zurücksetzen (neue 0°-Position)
robot.reset_gyro()

# Jetzt ist die aktuelle Ausrichtung 0°
robot.turn_to_angle(target_angle=90)  # Drehe 90° von HIER
```

---

## Kombination mit anderen Funktionen

### Mit drive_distance()
```python
# Fahre vorwärts, drehe, fahre weiter
robot.drive_distance(distance=40, mainspeed=600)
robot.turn_to_angle(target_angle=90)
robot.drive_distance(distance=40, mainspeed=600)
```

### Mit Sensorfunktionen
```python
# Drehe zu Winkel, fahre zur Linie
robot.turn_to_angle(target_angle=45)
robot.till_color(speed=400, color_type=3, color_gate=25)
```

### Relative Drehungen
```python
# Um einen relativen Winkel zu drehen, nutze global_turn_value:
def turn_relative(angle):
    current = robot.global_turn_value
    new_angle = (current + angle) % 360
    if new_angle > 180:
        new_angle -= 360
    robot.turn_to_angle(target_angle=new_angle)

# Beispiel: Drehe 45° nach rechts von aktueller Position
turn_relative(45)
```

---

## Winkel-System verstehen

### Koordinatensystem
```
        -90° (270°)
            ↑
            │
-180° ←─────┼─────→ 0°
   180°     │
            ↓
           90°
```

### Beispiele
```python
# Von 0° zu 90° = 90° Rechtsdrehung
# Von 90° zu -90° = 180° (kürzester Weg)
# Von 170° zu -170° = 20° Rechtsdrehung (kürzester Weg!)
```

### Global Turn Value Tracking
```python
# Wird automatisch aktualisiert nach:
# - turn_to_angle()
# - drive_distance() (wenn re_align=True)

# Manuell auslesen:
print(robot.global_turn_value)

# Manuell setzen:
robot.global_turn_value = 45
```

---

## Problemlösung

### Problem: Roboter oszilliert um Zielwinkel

**Ursache:** PID-Parameter zu aggressiv

**Lösung:** D-Wert erhöhen in `get_pids()`:
```python
# Mehr Dämpfung
return (3.0, 0.02, 20.0)  # Höherer D-Wert
```

### Problem: Roboter erreicht Zielwinkel nicht

**Ursache:** Threshold zu klein oder Timeout zu kurz

**Lösung:**
```python
robot.turn_to_angle(
    target_angle=90,
    threshold=1.0,     # Größere Toleranz
    timeout=10000      # Mehr Zeit
)
```

### Problem: Drehung zu langsam

**Ursache:** Geschwindigkeit zu niedrig oder P-Wert zu klein

**Lösung:**
```python
# Höhere Geschwindigkeit
robot.turn_to_angle(target_angle=90, speed=600)

# Oder P-Wert erhöhen in get_pids()
return (5.0, 0.01, 15.0)  # Höherer P-Wert
```

### Problem: Dreht nicht auf kürzestem Weg

**Überprüfung:**
```python
# Debug-Code
current = robot.gyro.yaw_angle()
target = 90
error = target - current
if error > 180: error -= 360
if error < -180: error += 360
print(f"Aktuell: {current}°, Ziel: {target}°, Fehler: {error}°")
```

### Problem: Ungenau bei kleinen Winkeln

**Lösung:** Timestep verkleinern für mehr Reaktivität:
```python
robot.turn_to_angle(
    target_angle=5,
    speed=200,
    timestep=30        # Reaktiver
)
```

---

## Erweiterte Techniken

### Dynamische Geschwindigkeit
```python
def turn_adaptive(target_angle):
    current = robot.gyro.yaw_angle()
    error = abs(target_angle - current)
    
    if error > 180:
        error = 360 - error
    
    # Geschwindigkeit an Winkel anpassen
    if error > 90:
        speed = 600
    elif error > 45:
        speed = 400
    else:
        speed = 250
    
    robot.turn_to_angle(target_angle=target_angle, speed=speed)
```

### Drehung mit Wiederholung
```python
def turn_precise(target_angle, max_attempts=3):
    for attempt in range(max_attempts):
        robot.turn_to_angle(
            target_angle=target_angle,
            threshold=0.3,
            timeout=5000
        )
        
        # Prüfe Genauigkeit
        current = robot.gyro.yaw_angle()
        if abs(current - target_angle) < 0.5:
            return True
    
    return False  # Fehlgeschlagen
```

### Sanfte Drehung mit Rampe
```python
def turn_smooth(target_angle):
    current = robot.gyro.yaw_angle()
    error = target_angle - current
    
    # Normalisiere Fehler
    if error > 180: error -= 360
    if error < -180: error += 360
    
    # Geschwindigkeit basierend auf verbleibendem Winkel
    while abs(error) > 0.5:
        speed = max(200, min(600, abs(error) * 10))
        robot.turn_to_angle(target_angle=target_angle, speed=speed, timeout=500)
        
        current = robot.gyro.yaw_angle()
        error = target_angle - current
        if error > 180: error -= 360
        if error < -180: error += 360
```

---

## Performance-Tipps

### ✅ Optimale Einstellungen für verschiedene Szenarien

**Schnelle Navigation:**
```python
robot.turn_to_angle(target_angle=90, speed=600, threshold=1.0)
```

**Präzise Ausrichtung:**
```python
robot.turn_to_angle(target_angle=90, speed=250, threshold=0.2, timeout=8000)
```

**Ausrichtung an Wand (fixiertes Rad):**
```python
robot.turn_to_angle(target_angle=90, type=1, speed=300)
```

**Batterieschonend:**
```python
robot.turn_to_angle(target_angle=90, speed=300, threshold=0.8)
```

---

## Siehe auch

- **[drive_distance()](Gyro-drive-distance)** - Präzise Distanzen fahren
- **[Sensorfunktionen](Gyro-Sensorfunktionen)** - Drehungen mit Sensor-Stop
- **[Tipps & Best Practices](Gyro-Tipps)** - PID-Tuning und Kalibrierung

---

[← Zurück: drive_distance()](Gyro-drive-distance) | [🏠 Home](Home) | [Weiter: Sensorfunktionen →](Gyro-Sensorfunktionen)
