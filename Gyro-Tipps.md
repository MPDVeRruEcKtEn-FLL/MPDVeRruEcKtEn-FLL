# Tipps & Best Practices

[← Zurück: Sensorfunktionen](Gyro-Sensorfunktionen) | [🏠 Home](Home)

---

## Überblick

Diese Seite enthält Tipps, Best Practices und Optimierungsstrategien für die Arbeit mit den Gyro-Funktionen. Von PID-Tuning bis zur Sensor-Kalibrierung.

---

## 📋 Inhalt

1. **[PID-Tuning](#pid-tuning)** - PID-Parameter optimal einstellen
2. **[Geschwindigkeitswahl](#geschwindigkeitswahl)** - Richtige Geschwindigkeiten wählen
3. **[Timeout-Werte](#timeout-werte)** - Timeouts sinnvoll setzen
4. **[Sensor-Kalibrierung](#sensor-kalibrierung)** - Sensoren kalibrieren
5. **[Global Turn Value](#global-turn-value)** - Winkel-Management
6. **[Batterie-Management](#batterie-management)** - Konsistente Performance
7. **[Debugging](#debugging)** - Probleme finden und lösen

---

## PID-Tuning

### Was ist PID?

PID steht für **Proportional-Integral-Derivative** und ist ein Regelungsmechanismus.

#### P (Proportional)
- Reagiert auf **aktuelle** Abweichung
- **Zu hoch:** Oszillation, Überschwingen
- **Zu niedrig:** Langsame Korrektur
- **Typisch:** 2.0 - 5.0

#### I (Integral)
- Korrigiert **dauerhafte** kleine Fehler
- **Zu hoch:** Instabil, langsam
- **Zu niedrig:** Kleine Fehler bleiben
- **Typisch:** 0.01 - 0.05

#### D (Derivative)
- Dämpft **Änderungen** (Bremst ab)
- **Zu hoch:** Träge Reaktion
- **Zu niedrig:** Überschwingen
- **Typisch:** 10.0 - 20.0

### PID-Werte anpassen

In `DriveBase.py` die `get_pids()` Funktion bearbeiten:

```python
def get_pids(self, error=0):
    """PID-Parameter für verschiedene Szenarien"""
    
    # Für drive_distance():
    if abs(error) > 45:
        return (4.0, 0.01, 15.0)  # Große Abweichung
    elif abs(error) > 10:
        return (3.5, 0.02, 12.0)  # Mittlere Abweichung
    else:
        return (3.0, 0.03, 10.0)  # Kleine Abweichung
```

### Schritt-für-Schritt Tuning

#### 1. Nur P einstellen
```python
# I und D auf 0 setzen
return (3.0, 0.0, 0.0)

# P erhöhen bis Oszillation beginnt
# Dann auf 70% reduzieren
```

#### 2. D hinzufügen
```python
# D hinzufügen um Oszillation zu dämpfen
return (3.0, 0.0, 12.0)

# D erhöhen bis stabil
```

#### 3. I optimieren
```python
# I für Feinabstimmung
return (3.0, 0.02, 12.0)

# I erhöhen bis keine Restfehler mehr
```

### Häufige PID-Probleme

#### Problem: Roboter oszilliert
```python
# Lösung: P reduzieren, D erhöhen
return (2.5, 0.01, 18.0)  # Mehr Dämpfung
```

#### Problem: Roboter korrigiert zu langsam
```python
# Lösung: P erhöhen
return (5.0, 0.01, 15.0)  # Reaktiver
```

#### Problem: Restfehler bleibt
```python
# Lösung: I erhöhen
return (3.0, 0.05, 12.0)  # Mehr Integral
```

---

## Geschwindigkeitswahl

### Empfohlene Geschwindigkeiten

#### Geradeausfahrt (drive_distance)
```python
# Langsam und präzise
robot.drive_distance(distance=50, mainspeed=400)

# Standard
robot.drive_distance(distance=50, mainspeed=600)

# Schnell
robot.drive_distance(distance=50, mainspeed=800)

# Maximum (nicht empfohlen)
robot.drive_distance(distance=50, mainspeed=1000)
```

#### Drehungen (turn_to_angle)
```python
# Sehr präzise
robot.turn_to_angle(target_angle=90, speed=200)

# Standard
robot.turn_to_angle(target_angle=90, speed=300)

# Schnell
robot.turn_to_angle(target_angle=90, speed=500)
```

#### Sensorfunktionen
```python
# Linienerkennung (präzise)
robot.till_color(speed=300, ...)

# Standard
robot.till_color(speed=400, ...)

# Schnell (kann überschießen)
robot.till_color(speed=600, ...)
```

### Geschwindigkeit vs. Präzision

| Geschwindigkeit | Präzision | Verwendung |
|----------------|-----------|------------|
| 200-400 | ⭐⭐⭐⭐⭐ | Präzise Aufgaben |
| 400-600 | ⭐⭐⭐⭐ | Standard-Navigation |
| 600-800 | ⭐⭐⭐ | Schnelle Fahrten |
| 800-1000 | ⭐⭐ | Nur wenn nötig |

### Dynamische Geschwindigkeit

```python
def drive_adaptive(distance):
    """Geschwindigkeit an Distanz anpassen"""
    if abs(distance) > 100:
        speed = 800  # Lange Strecke = schnell
    elif abs(distance) > 50:
        speed = 600  # Mittlere Strecke
    else:
        speed = 400  # Kurze Strecke = präzise
    
    robot.drive_distance(distance=distance, mainspeed=speed)
```

---

## Timeout-Werte

### Warum Timeouts wichtig sind

Ohne Timeout kann der Roboter:
- Endlos versuchen ein Ziel zu erreichen
- Steckenbleiben wenn Sensor defekt ist
- Zeit verschwenden

### Empfohlene Timeouts

#### drive_distance()
```python
# Kurze Distanz (< 30cm)
robot.drive_distance(distance=20, timeout=2000)  # 2 Sekunden

# Mittlere Distanz (30-100cm)
robot.drive_distance(distance=50, timeout=5000)  # 5 Sekunden

# Lange Distanz (> 100cm)
robot.drive_distance(distance=150, timeout=10000)  # 10 Sekunden
```

#### turn_to_angle()
```python
# Kleine Drehung (< 45°)
robot.turn_to_angle(target_angle=30, timeout=3000)

# Mittlere Drehung (45-135°)
robot.turn_to_angle(target_angle=90, timeout=5000)

# Große Drehung (> 135°)
robot.turn_to_angle(target_angle=180, timeout=7000)
```

#### Sensorfunktionen
```python
# Wenn Sensor nah am Ziel
robot.till_color(speed=400, timeout=3000)

# Wenn Sensor weit vom Ziel
robot.till_color(speed=400, timeout=8000)

# Sicherheits-Timeout (sehr lang)
robot.till_color(speed=400, timeout=15000)
```

### Timeout berechnen

```python
def calculate_timeout(distance, speed):
    """Berechne sinnvollen Timeout"""
    # Zeit = Distanz / Geschwindigkeit
    # + 50% Puffer
    estimated_time = (abs(distance) / speed) * 1.5 * 1000
    return max(2000, min(15000, estimated_time))

# Verwendung:
timeout = calculate_timeout(distance=80, speed=600)
robot.drive_distance(distance=80, mainspeed=600, timeout=timeout)
```

---

## Sensor-Kalibrierung

### Farbsensor kalibrieren

#### Reflexionswerte testen

```python
from hub import port
import time

# Sensor initialisieren
color_sensor = port.A  # Anpassen an deinen Port!

print("=== SENSOR KALIBRIERUNG ===")
print("Platziere Sensor über verschiedene Oberflächen")
print()

surfaces = ["SCHWARZ", "WEISS", "GRAU", "LINIE"]

for surface in surfaces:
    input(f"Platziere über {surface} und drücke Enter...")
    
    values = []
    for i in range(10):
        reflected = color_sensor.device.get()[0]
        values.append(reflected)
        time.sleep(0.1)
    
    avg = sum(values) / len(values)
    print(f"{surface}: {avg:.1f}% (min: {min(values)}, max: {max(values)})")

print("\n=== FERTIG ===")
```

#### Schwellenwerte bestimmen

```python
# Beispiel-Ausgabe:
# SCHWARZ: 8.5% (min: 7, max: 10)
# WEISS:  92.3% (min: 90, max: 95)
# GRAU:   45.2% (min: 42, max: 48)
# LINIE:  15.7% (min: 14, max: 18)

# Schwellenwerte ableiten:
black_threshold = 12   # Zwischen Schwarz und Linie
white_threshold = 80   # Zwischen Grau und Weiß
line_threshold = 22    # Zwischen Linie und Grau
```

### Gyro kalibrieren

#### Drift-Test

```python
import time

# Roboter still stehen lassen
print("Lasse Roboter 10 Sekunden still stehen...")
start_angle = robot.gyro.yaw_angle()
time.sleep(10)
end_angle = robot.gyro.yaw_angle()

drift = end_angle - start_angle
print(f"Gyro-Drift: {drift}° über 10 Sekunden")

if abs(drift) > 2:
    print("⚠️ Warnung: Gyro hat hohen Drift!")
    print("Lösung: Hub neu starten und stillhalten während Start")
else:
    print("✅ Gyro-Drift ist OK")
```

#### Genauigkeits-Test

```python
# Teste 360° Drehung
robot.reset_gyro()
robot.turn_to_angle(target_angle=90)
robot.turn_to_angle(target_angle=180)
robot.turn_to_angle(target_angle=270)
robot.turn_to_angle(target_angle=0)

final_angle = robot.gyro.yaw_angle()
print(f"Endwinkel nach 360°: {final_angle}°")
print(f"Fehler: {abs(final_angle)}°")

if abs(final_angle) < 2:
    print("✅ Gyro sehr genau")
elif abs(final_angle) < 5:
    print("⚠️ Gyro OK, aber nicht perfekt")
else:
    print("❌ Gyro ungenau - Kalibrierung nötig")
```

---

## Global Turn Value

### Was ist der Global Turn Value?

Der `global_turn_value` speichert den aktuellen absoluten Winkel des Roboters.

```python
# Wird automatisch aktualisiert von:
# - turn_to_angle()
# - drive_distance() (wenn re_align=True)

# Auslesen:
current_angle = robot.global_turn_value
print(f"Aktueller Winkel: {current_angle}°")

# Manuell setzen:
robot.global_turn_value = 0  # Setzt aktuelle Richtung als 0°
```

### Best Practices

#### 1. Initialisierung
```python
# Am Anfang des Programms
robot.reset_gyro()  # Setzt global_turn_value auf 0
```

#### 2. Konsistente Verwendung
```python
# RICHTIG: Nutze turn_to_angle für absolute Winkel
robot.drive_distance(distance=50, mainspeed=600)
robot.turn_to_angle(target_angle=90)  # Absolut
robot.drive_distance(distance=30, mainspeed=600)
robot.turn_to_angle(target_angle=0)   # Zurück zu Start

# FALSCH: Mische nicht verschiedene Systeme
robot.drive_distance(distance=50, mainspeed=600)
robot.motor_rotate(90)  # Nicht empfohlen - kein global_turn_value update
```

#### 3. Re-Alignment nutzen
```python
# Nach jeder Fahrt re-alignen für Präzision
robot.drive_distance(
    distance=50,
    mainspeed=600,
    re_align=True  # Default - gut!
)
```

#### 4. Isolated Drive für Teilmanöver
```python
# Komplexes Manöver ohne globalen Winkel zu ändern
def pick_up_object():
    robot.drive_distance(distance=10, isolated_drive=True)
    # ... Objekt aufnehmen ...
    robot.drive_distance(distance=-10, isolated_drive=True)
    # global_turn_value bleibt unverändert

# Hauptprogramm
robot.turn_to_angle(target_angle=90)
pick_up_object()  # Ändert global_turn_value nicht
robot.drive_distance(distance=50)  # Nutzt noch immer 90° als Referenz
```

---

## Batterie-Management

### Warum ist das wichtig?

Sinkende Batteriespannung führt zu:
- Langsameren Motoren
- Ungenaueren Bewegungen
- Unterschiedlichen Geschwindigkeiten

### Batterie-Check vor Wettkampf

```python
from hub import battery

voltage = battery.voltage()
capacity = battery.capacity()

print(f"Batterie: {voltage}mV, {capacity}%")

if voltage < 8000:
    print("⚠️ Warnung: Batterie schwach!")
    print("Empfehlung: Batterien wechseln")
elif voltage < 8500:
    print("⚠️ Batterie OK, aber bald wechseln")
else:
    print("✅ Batterie gut")
```

### Geschwindigkeit an Batterie anpassen

```python
def get_adjusted_speed(target_speed):
    """Passt Geschwindigkeit an Batteriespannung an"""
    voltage = battery.voltage()
    
    if voltage > 8500:
        return target_speed  # Volle Geschwindigkeit
    elif voltage > 8000:
        return int(target_speed * 0.9)  # 90%
    else:
        return int(target_speed * 0.8)  # 80%

# Verwendung:
speed = get_adjusted_speed(600)
robot.drive_distance(distance=50, mainspeed=speed)
```

---

## Debugging

### Debug-Ausgaben aktivieren

```python
# Zeige Werte während drive_distance
def drive_distance_debug(distance, mainspeed=600):
    """drive_distance mit Debug-Ausgabe"""
    start_angle = robot.gyro.yaw_angle()
    
    # Während der Fahrt
    while True:
        current_angle = robot.gyro.yaw_angle()
        error = current_angle - start_angle
        
        # Debug-Ausgabe
        print(f"Angle: {current_angle}°, Error: {error}°")
        
        # ... rest der Funktion ...
```

### Häufige Probleme

#### Problem: Roboter fährt nicht gerade

**Diagnose:**
```python
# Teste beide Motoren einzeln
robot.motor_rotate(500, ports=(0,))  # Links
robot.motor_rotate(500, ports=(4,))  # Rechts

# Vergleiche Geschwindigkeit und Distanz
```

**Lösung:**
- Motoren kalibrieren
- Radumfang anpassen
- PID-Werte tunen

#### Problem: Drehungen ungenau

**Diagnose:**
```python
# Teste 4× 90° Drehungen
for i in range(4):
    robot.turn_to_angle(target_angle=90*i)
    actual = robot.gyro.yaw_angle()
    print(f"Soll: {90*i}°, Ist: {actual}°")
```

**Lösung:**
- Gyro neu kalibrieren
- Hub neu starten
- Threshold anpassen

#### Problem: Timeout zu früh

**Diagnose:**
```python
import time

start = time.ticks_ms()
robot.drive_distance(distance=100, mainspeed=600)
duration = time.ticks_diff(time.ticks_ms(), start)

print(f"Benötigte Zeit: {duration}ms")
```

**Lösung:**
- Timeout erhöhen
- Geschwindigkeit erhöhen
- Distanz überprüfen

---

## Performance-Checkliste

### Vor jedem Wettkampf

- [ ] Batterien voll geladen (> 8.5V)
- [ ] Hub neu gestartet
- [ ] Gyro kalibriert (stillstehend)
- [ ] Farbsensor kalibriert
- [ ] Radumfang korrekt eingestellt
- [ ] PID-Werte getestet
- [ ] Timeouts angemessen
- [ ] Test-Lauf erfolgreich

### Während des Wettkampfs

- [ ] global_turn_value im Auge behalten
- [ ] Bei Fehlern: Gyro reset
- [ ] Batterie-Warnung beachten
- [ ] Sensor-Position prüfen

---

## Erweiterte Techniken

### Adaptives PID

```python
def get_adaptive_pids(self, error, speed):
    """PID passt sich an Geschwindigkeit und Fehler an"""
    
    # Basis-PID
    P = 3.5
    I = 0.02
    D = 12.0
    
    # Anpassung an Geschwindigkeit
    if speed > 700:
        D *= 1.5  # Mehr Dämpfung bei hoher Geschwindigkeit
    
    # Anpassung an Fehler
    if abs(error) < 5:
        P *= 1.2  # Reaktiver bei kleinen Fehlern
        I *= 1.5  # Mehr Integral für Feinabstimmung
    
    return (P, I, D)
```

### Smart Re-Alignment

```python
def smart_re_align():
    """Re-Alignment nur wenn nötig"""
    current = robot.gyro.yaw_angle()
    target = robot.global_turn_value
    error = abs(current - target)
    
    if error > 2:  # Nur bei größeren Abweichungen
        robot.turn_to_angle(target_angle=target)
        print(f"Re-aligned: {error}° Korrektur")
    else:
        print(f"Keine Re-Alignment nötig ({error}°)")
```

### Odometrie-Tracking

```python
class PositionTracker:
    """Verfolge Position auf dem Spielfeld"""
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
    
    def update_position(self, distance):
        """Update nach drive_distance"""
        import math
        rad = math.radians(self.angle)
        self.x += distance * math.cos(rad)
        self.y += distance * math.sin(rad)
    
    def update_angle(self, new_angle):
        """Update nach turn_to_angle"""
        self.angle = new_angle
    
    def get_position(self):
        return (self.x, self.y, self.angle)

# Verwendung:
tracker = PositionTracker()

robot.drive_distance(distance=50, mainspeed=600)
tracker.update_position(50)

robot.turn_to_angle(target_angle=90)
tracker.update_angle(90)

print(f"Position: {tracker.get_position()}")
```

---

## Siehe auch

- **[drive_distance()](Gyro-drive-distance)** - Präzise Distanzen fahren
- **[turn_to_angle()](Gyro-turn-to-angle)** - Präzise Drehungen
- **[Sensorfunktionen](Gyro-Sensorfunktionen)** - Sensor-basierte Navigation

---

[← Zurück: Sensorfunktionen](Gyro-Sensorfunktionen) | [🏠 Home](Home)
