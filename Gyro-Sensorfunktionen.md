# Gyro-Sensorfunktionen

[← Zurück: turn_to_angle()](Gyro-turn-to-angle) | [🏠 Home](Home) | [Weiter: Tipps →](Gyro-Tipps)

---

## Überblick

Die Sensorfunktionen kombinieren präzise Bewegung mit Farbsensor-Feedback. Sie ermöglichen es dem Roboter, auf Umgebungsbedingungen zu reagieren und flexibel zu navigieren.

---

## 📋 Inhalt

1. **[turn_till_color()](#turn_till_color)** - Dreht bis Farbe erkannt
2. **[turn_till_reflect()](#turn_till_reflect)** - Dreht bis Reflexion erkannt
3. **[till_color()](#till_color)** - Fährt bis Farbe erkannt
4. **[till_collide()](#till_collide)** - Fährt bis Kollision

---

## turn_till_color()

Dreht den Roboter, bis der Farbsensor eine bestimmte Farbe erkennt.

### Parameter

#### direction (int, default: 1)
Drehrichtung:
- **1:** Rechtsdrehung (im Uhrzeigersinn)
- **-1:** Linksdrehung (gegen Uhrzeigersinn)

#### speed (int, default: 250) [°/s]
Drehgeschwindigkeit. Langsamere Geschwindigkeiten sind präziser.

#### color_type (int, default: 0)
Art der Farberkennung:
- **0:** Reflected Light (Reflexion, 0-100%)
- **1:** RGB (Red value, 0-1024)
- **2:** RGB (Green value, 0-1024)
- **3:** RGB (Blue value, 0-1024)
- **4:** Color ID (0-10: specific colors)

#### color_gate (int, default: 50)
Schwellenwert für Erkennung:
- Bei **color_type=0 (Reflected):** Helligkeit (z.B. 50 = 50%)
- Bei **color_type=1-3 (RGB):** Farbintensität (0-1024)
- Bei **color_type=4 (Color ID):** Farb-ID (0=schwarz, 3=blau, 5=rot, etc.)

#### mode (str, default: "greater")
Vergleichsmodus:
- **"greater":** Stopp wenn Wert > color_gate (z.B. Linie wird heller)
- **"lower":** Stopp wenn Wert < color_gate (z.B. Linie wird dunkler)

#### timeout (int, default: 5000) [ms]
Maximale Zeit für die Drehung.

#### timestep (int, default: 50) [ms]
Zeitintervall zwischen Sensor-Abfragen.

### Verwendungsbeispiele

#### Drehe zur schwarzen Linie (Reflexion)
```python
# Drehe rechts, bis schwarze Linie erkannt (dunkel = niedrige Reflexion)
robot.turn_till_color(
    direction=1,         # Rechts drehen
    speed=250,
    color_type=0,        # Reflexion
    color_gate=25,       # Schwellenwert
    mode="lower"         # Stopp wenn dunkler als 25%
)
```

#### Drehe zur weißen Linie (Reflexion)
```python
# Drehe links, bis weiße Linie erkannt (hell = hohe Reflexion)
robot.turn_till_color(
    direction=-1,        # Links drehen
    speed=250,
    color_type=0,        # Reflexion
    color_gate=75,       # Schwellenwert
    mode="greater"       # Stopp wenn heller als 75%
)
```

#### Drehe zur roten Zone (Color ID)
```python
# Drehe bis rote Farbe erkannt
robot.turn_till_color(
    direction=1,
    speed=200,
    color_type=4,        # Color ID
    color_gate=5,        # 5 = Rot
    mode="greater"       # Stopp wenn Farb-ID >= 5
)
```

#### Drehe zur blauen Komponente (RGB)
```python
# Drehe bis viel Blau erkannt
robot.turn_till_color(
    direction=-1,
    speed=250,
    color_type=3,        # Blau-Wert
    color_gate=300,      # Schwellenwert
    mode="greater"       # Stopp wenn Blau > 300
)
```

---

## turn_till_reflect()

Vereinfachte Version von `turn_till_color()` speziell für Reflexionswerte. Besonders nützlich für Linienerkennung.

### Parameter

#### direction (int, default: 1)
Drehrichtung (1=rechts, -1=links)

#### speed (int, default: 250) [°/s]
Drehgeschwindigkeit

#### reflect_gate (int, default: 50) [%]
Reflexions-Schwellenwert (0-100%)

#### mode (str, default: "greater")
Vergleichsmodus ("greater" oder "lower")

#### timeout (int, default: 5000) [ms]
Maximale Zeit

#### timestep (int, default: 50) [ms]
Zeitintervall

### Verwendungsbeispiele

#### Einfache Linienerkennung
```python
# Drehe zur schwarzen Linie
robot.turn_till_reflect(
    direction=1,
    reflect_gate=25,     # Dunkel = < 25%
    mode="lower"
)
```

#### Suche weiße Markierung
```python
# Drehe zur hellen Markierung
robot.turn_till_reflect(
    direction=-1,
    reflect_gate=80,
    mode="greater"
)
```

---

## till_color()

Fährt geradeaus, bis der Farbsensor eine bestimmte Farbe erkennt.

### Parameter

#### speed (int, default: 400) [°/s]
Fahrgeschwindigkeit

#### color_type (int, default: 0)
Art der Farberkennung (wie bei turn_till_color)

#### color_gate (int, default: 50)
Schwellenwert (wie bei turn_till_color)

#### mode (str, default: "greater")
Vergleichsmodus (wie bei turn_till_color)

#### timeout (int, default: 5000) [ms]
Maximale Fahrzeit

#### timestep (int, default: 50) [ms]
Zeitintervall

### Verwendungsbeispiele

#### Fahre zur schwarzen Linie
```python
# Fahre vorwärts bis schwarze Linie erkannt
robot.till_color(
    speed=400,
    color_type=0,        # Reflexion
    color_gate=25,       # Dunkel
    mode="lower"
)
```

#### Fahre zur weißen Zone
```python
# Fahre bis helle Zone
robot.till_color(
    speed=400,
    color_type=0,
    color_gate=75,
    mode="greater"
)
```

#### Fahre zur blauen Zone (Color ID)
```python
# Fahre bis blaue Farbe
robot.till_color(
    speed=300,
    color_type=4,        # Color ID
    color_gate=3,        # 3 = Blau
    mode="greater"
)
```

#### Rückwärts zur Linie
```python
# Fahre rückwärts bis zur Linie
robot.till_color(
    speed=-400,          # Negativ = rückwärts
    color_type=0,
    color_gate=25,
    mode="lower"
)
```

---

## till_collide()

Fährt geradeaus, bis der Kraftsensor eine Kollision erkennt.

### Parameter

#### speed (int, default: 400) [°/s]
Fahrgeschwindigkeit

#### force_gate (int, default: 5) [N]
Kraft-Schwellenwert für Kollisionserkennung (Newton)

#### timeout (int, default: 5000) [ms]
Maximale Fahrzeit

#### timestep (int, default: 50) [ms]
Zeitintervall

### Verwendungsbeispiele

#### Fahre zur Wand
```python
# Fahre sanft zur Wand
robot.till_collide(
    speed=300,
    force_gate=3         # Niedrige Kraft = sanft
)
```

#### Schnelle Positionierung
```python
# Fahre schnell zur Wand
robot.till_collide(
    speed=600,
    force_gate=8,        # Höhere Kraft OK bei Geschwindigkeit
    timeout=3000
)
```

#### Rückwärts zur Wand
```python
# Rückwärts positionieren
robot.till_collide(
    speed=-400,          # Rückwärts
    force_gate=5
)
```

---

## Kombinations-Beispiele

### Komplexe Navigation mit Sensoren

#### Beispiel 1: Linie finden und folgen
```python
# 1. Fahre vorwärts zur Linie
robot.drive_distance(distance=40, mainspeed=600)

# 2. Drehe zur Linie (falls nicht perfekt ausgerichtet)
robot.turn_till_reflect(direction=1, reflect_gate=25, mode="lower")

# 3. Fahre entlang der Linie
robot.till_color(speed=400, color_type=0, color_gate=25, mode="lower")
```

#### Beispiel 2: Präzise Positionierung
```python
# 1. Fahre zur Wand
robot.till_collide(speed=400, force_gate=5)

# 2. Zurücksetzen um 3cm
robot.drive_distance(distance=-3, mainspeed=400)

# 3. Drehe zu präzisem Winkel
robot.turn_to_angle(target_angle=90)

# 4. Fahre zur Farbmarkierung
robot.till_color(speed=300, color_type=4, color_gate=5, mode="greater")
```

#### Beispiel 3: Farb-basierte Entscheidung
```python
# Fahre zur ersten Linie
robot.till_color(speed=400, color_type=0, color_gate=25, mode="lower")

# Lese Farbe
color = robot.color.get()[0]

# Entscheide basierend auf Farbe
if color == 5:  # Rot
    robot.turn_to_angle(target_angle=90)
elif color == 3:  # Blau
    robot.turn_to_angle(target_angle=-90)
else:  # Andere
    robot.turn_to_angle(target_angle=180)

# Fahre weiter
robot.drive_distance(distance=30, mainspeed=600)
```

---

## Tipps für Sensorfunktionen

### ✅ Reflexionswerte kalibrieren

Immer vor dem Wettkampf testen:
```python
# Test-Code für Reflexionswerte
import time
from hub import light_matrix, port

color_sensor = port.A  # Anpassen!

for i in range(10):
    reflected = color_sensor.device.get()[0]
    print(f"Reflexion: {reflected}%")
    time.sleep(0.5)
```

### ✅ Geschwindigkeit anpassen

- **Langsam (200-300):** Präzise Erkennung, reagiert schneller
- **Mittel (400-500):** Guter Kompromiss
- **Schnell (600+):** Kann über Ziel hinausschießen

### ✅ Mode richtig wählen

- **"greater":** Für Übergang von dunkel zu hell
- **"lower":** Für Übergang von hell zu dunkel

### ✅ Timeout nicht vergessen

Immer einen realistischen Timeout setzen:
```python
robot.till_color(
    speed=400,
    color_type=0,
    color_gate=25,
    mode="lower",
    timeout=3000  # Stopp nach 3 Sekunden
)
```

### ✅ Sensor-Position beachten

Der Sensor muss nah genug am Boden sein für zuverlässige Werte:
- **Optimal:** 5-10mm Abstand
- **Zu hoch:** Unreliable readings
- **Zu niedrig:** Kann hängen bleiben

---

## Farbwerte-Referenz

### Color ID Werte (color_type=4)
```
0  = Schwarz
1  = Violett
2  = Blau
3  = Cyan
4  = Grün
5  = Gelb
6  = Rot
7  = Weiß
-1 = Keine Farbe erkannt
```

### Reflexionswerte (color_type=0)
```
0-20%   = Schwarz / sehr dunkel
20-40%  = Dunkelgrau
40-60%  = Grau
60-80%  = Hellgrau
80-100% = Weiß / sehr hell
```

---

## Problemlösung

### Problem: Sensor erkennt nicht zuverlässig

**Lösung:**
1. Sensor-Position überprüfen (Abstand zum Boden)
2. Beleuchtung im Raum prüfen
3. Schwellenwert anpassen
4. Langsamere Geschwindigkeit

### Problem: Roboter fährt zu weit über Linie

**Lösung:**
```python
# Langsamere Geschwindigkeit
robot.till_color(speed=250, ...)  # statt 400

# Oder kürzerer timestep
robot.till_color(speed=400, timestep=30, ...)  # statt 50
```

### Problem: Timeout wird erreicht

**Lösung:**
1. Timeout erhöhen
2. Prüfen ob Zielfarbe überhaupt vorhanden
3. Schwellenwert anpassen

---

## Siehe auch

- **[drive_distance()](Gyro-drive-distance)** - Präzise Distanzen fahren
- **[turn_to_angle()](Gyro-turn-to-angle)** - Präzise Drehungen
- **[Tipps & Best Practices](Gyro-Tipps)** - Optimierungshinweise

---

[← Zurück: turn_to_angle()](Gyro-turn-to-angle) | [🏠 Home](Home) | [Weiter: Tipps →](Gyro-Tipps)
