# drive_distance()

[← Zurück: Gyro-Funktionen](Gyro-Funktionen) | [🏠 Home](Home) | [Weiter: turn_to_angle() →](Gyro-turn-to-angle)

---

## Überblick

Die `drive_distance()` Funktion ermöglicht es dem Roboter, eine präzise Distanz zu fahren, während der Gyrosensor kontinuierlich die Ausrichtung korrigiert. Die Funktion verwendet PID-Regelung für die Richtungskorrektur und implementiert intelligente Beschleunigungs- und Bremsprofile.

---

## Parameter

### distance (int, default: 100) [cm]
Die zu fahrende Distanz in Zentimetern. 
- **Positiv:** Vorwärts fahren
- **Negativ:** Rückwärts fahren
- **-1:** Endlos fahren (bis manueller Stopp)

### mainspeed (int, default: 600) [°/s]
Die maximale Geschwindigkeit während der Fahrt. Wird sanft durch Beschleunigung erreicht.

### stopspeed (float, default: 300) [°/s]
Die Zielgeschwindigkeit am Ende der Strecke. Verhindert abruptes Stoppen.

### re_align (bool, default: True)
- **True:** Roboter dreht sich nach der Fahrt zurück zum exakten Ausgangswinkel
- **False:** Kleine Winkelabweichungen werden akzeptiert

### isolated_drive (bool, default: False)
- **True:** Fährt unabhängig vom globalen Referenzwinkel (für Teilmanöver)
- **False:** Nutzt den global gespeicherten Winkel als Referenz

### stop (bool, default: True)
- **True:** Roboter stoppt am Ende automatisch
- **False:** Motoren laufen weiter (für fließende Übergänge)

### brake_start (float, default: 0.7)
Prozentwert (0.0-1.0), ab wann der Bremsvorgang beginnt.
- **0.7:** Bei 70% der Strecke beginnt das Bremsen
- **0.9:** Spätes Bremsen (schneller, weniger sanft)
- **0.5:** Frühes Bremsen (langsamer, sehr sanft)

### timestep (int, default: 100) [ms]
Zeitintervall zwischen PID-Berechnungen.
- **Kleinere Werte:** Reaktiver, aber instabiler
- **Größere Werte:** Stabiler, aber träger

### avoid_collision (bool, default: False)
⚠️ **NOCH NICHT IMPLEMENTIERT** - Geplant für automatische Kollisionserkennung

---

## Funktionsweise im Detail

### 1. Initialisierung
```python
# Motoren auf 0 setzen
motor.reset_relative_position(motor_right, 0)
motor.reset_relative_position(motor_left, 0)

# Startwinkel bestimmen
start_angle = gyro.yaw_angle() if isolated_drive else global_turn_value

# Zieldrehung berechnen
rotate_distance = (distance / wheel_circumference) * 360

# Bremspunkt berechnen
brake_point = rotate_distance * brake_start
```

### 2. PID-Regelung

**Fehlerberechnung:**
```python
error = current_gyro - start_angle
```

**PID-Komponenten:**
- **P (Proportional):** Reagiert auf aktuelle Abweichung
- **I (Integral):** Korrigiert kumulative Fehler
- **D (Derivative):** Dämpft Schwingungen

**Lenkungsberechnung:**
```python
steering = (error * P) + (integral * I) + ((error - old_error) * D)
steering = max(-100, min(100, steering))  # Begrenzen
```

### 3. Geschwindigkeitsprofil

Die Funktion durchläuft drei Phasen:

#### Phase 1: Beschleunigung
```
Speed
  ▲
  │     ┌─────────────
  │    ╱  Konstant
  │   ╱
  │  ╱  Beschleunigung
  │ ╱
  └─────────────────────► Distance
```

#### Phase 2: Konstante Geschwindigkeit
Fährt mit `mainspeed`

#### Phase 3: Bremsen (ab brake_start)
```python
if driven >= brake_point:
    steering = 0  # Kein Lenken während Bremsen
    speed = decelerate_to(stopspeed)
```

### 4. Re-Alignment

Falls `re_align=True`:
```python
# Nach Fahrt: Korrigiere Winkelabweichung
current_angle = gyro.yaw_angle()
if abs(current_angle - global_turn_value) > 0.5:
    turn_to_angle(global_turn_value)
```

---

## Verwendungsbeispiele

### Einfache Fahrt
```python
# Fahre 50cm vorwärts mit Standardeinstellungen
robot.drive_distance(distance=50, mainspeed=600)
```

### Präzise Fahrt mit langsamem Stopp
```python
robot.drive_distance(
    distance=100, 
    mainspeed=800,      # Schnell fahren
    stopspeed=200,      # Langsam stoppen
    brake_start=0.8     # Bremst über die letzten 20%
)
```

### Rückwärtsfahrt
```python
# 30cm rückwärts
robot.drive_distance(
    distance=-30,
    mainspeed=500
)
```

### Isolierte Fahrt ohne globale Ausrichtung
```python
# Für komplexe Manöver ohne globale Winkel-Aktualisierung
robot.drive_distance(
    distance=50,
    isolated_drive=True,  # Ignoriert global_turn_value
    re_align=False        # Keine Neuausrichtung am Ende
)
```

### Endlose Fahrt (bis manueller Stopp)
```python
# Nützlich für manuelle Steuerung
robot.drive_distance(
    distance=-1,      # Fährt endlos
    mainspeed=500,
    stop=False        # Stoppt nicht automatisch
)

# Später manuell stoppen:
robot.stop_motor(ports=(0, 4))
```

### Sehr sanfte Fahrt
```python
robot.drive_distance(
    distance=80,
    mainspeed=400,
    stopspeed=150,
    brake_start=0.5    # Bremst über die letzten 50%
)
```

---

## Problemlösung

### Problem: Roboter schlingert

**Lösung:** PID-Werte anpassen
```python
# In DriveBase.py die get_pids() Funktion anpassen
# P und D reduzieren für stabilere Fahrt
```

### Problem: Roboter korrigiert zu langsam

**Lösung:** P-Wert erhöhen oder timestep verkleinern
```python
robot.drive_distance(distance=50, timestep=50)  # Reaktiver
```

### Problem: Roboter erreicht Ziel nicht genau

**Lösung:** Radumfang kalibrieren
```python
# Miss tatsächliche Distanz und passe an:
robot.configure(wheel_circumference=17.8)  # Standard: 17.6
```

---

## Siehe auch

- **[turn_to_angle()](Gyro-turn-to-angle)** - Präzise Drehungen
- **[Tipps & Best Practices](Gyro-Tipps)** - Optimierungshinweise
- **[till_color()](Gyro-Sensorfunktionen#till_color)** - Fahren bis Farbe erkannt

---

[← Zurück: Gyro-Funktionen](Gyro-Funktionen) | [🏠 Home](Home) | [Weiter: turn_to_angle() →](Gyro-turn-to-angle)
