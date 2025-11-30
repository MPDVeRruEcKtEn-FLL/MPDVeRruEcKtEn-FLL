# Berechnungen

[← Zurück: Motorinteraktionen](Einfache-Motorinteraktionen) | [🏠 Home](Home) | [Weiter: Gyro-Funktionen →](Gyro-Funktionen)

---

Dieser Abschnitt beinhaltet alle Funktionen zur Berechnung/Ausgabe bestimmter Informationen.

---

## DriveBase.get_addition_state()  

Prüft die Position des Zusatzmotors und gibt an, ob das Anbauteil befestigt oder gelöst ist.  

### Rückgabewert

- **True**: Wenn `abs_pos zwischen 80° und 100°`  
  > Das Anbauteil ist fest verbunden/verriegelt.  

- **False**: Wenn `abs_pos zwischen -10° und 10°` oder `zwischen 170° und 190°`  
  > Das Anbauteil ist gelöst/entriegelt.

### Beispiel
```python
if robot.get_addition_state():
    print("Anbauteil ist befestigt")
else:
    print("Anbauteil ist gelöst")
```

---

## DriveBase.speed_calculation()  

Berechnet die optimale Geschwindigkeit mit automatischer Beschleunigung und Verzögerung.  
Wird intern für sanfte Geschwindigkeitsprofile verwendet.  

### Parameter  

- **speed** (typ: int)  
  > Die aktuell gefahrene Geschwindigkeit des Roboters.  

- **decelerate_distance** (typ: float)  
  > Die Strecke in cm, ab der der Bremsvorgang beginnt.  

- **brake_start_value** (typ: float)  
  > Prozentwert (0.0-1.0), ab wann gebremst wird. Z.B. 0.7 = bei 70% der Strecke.  

- **driven** (typ: int)  
  > Die aktuell vom Roboter zurückgelegte Strecke in Grad (Motorumdrehungen).  

- **old_driven** (typ: int)  
  > Die Strecke beim letzten Funktionsaufruf, um die Beschleunigung zu berechnen.  

- **mode** (typ: int; default: 0)  
  > Fahrmodus: **0** = Drehung (turn), **1** = Vorwärtsfahrt (drive).  

- **rotate_mode** (typ: int; default: 0)  
  > Drehmodus: **0** = normale Drehung, **1** = Tank-Drehung (beide Räder gegenläufig).  

- **mainspeed** (typ: int; default: 300)  
  > Die maximale Zielgeschwindigkeit während der Fahrt.  

- **stopspeed** (typ: int; default: 300)  
  > Die minimale Geschwindigkeit am Ende (verhindert ruckartiges Stoppen).

> ⚠️ **Hinweis:** Diese Funktion wird normalerweise intern verwendet.

---

## DriveBase.get_pids()  

Berechnet optimale PID-Parameter (Proportional, Integral, Derivative) basierend auf der Fahrgeschwindigkeit.  
Höhere Geschwindigkeiten benötigen andere PID-Werte für stabile Regelung.  

### Rückgabewert

- **tuple[float, float, float]**  
  > Die optimierten PID-Werte als Tupel: `(P-Regler, I-Regler, D-Regler)`  
  > Beispiel: `(5.0, 0.1, 1.0)` bedeutet P=5.0, I=0.1, D=1.0

### Beispiel
```python
p, i, d = robot.get_pids()
print(f"PID-Werte: P={p}, I={i}, D={d}")
```

---

## DriveBase.auto_detect_device()  

Scannt alle Ports (A-F) und findet automatisch angeschlossene Geräte eines bestimmten Typs.  
Nützlich für dynamische Hardware-Erkennung oder zum Finden von Sensoren.  

### Parameter  

- **device_type** (typ: int)  
  > Der zu suchende Gerätetyp:  
  > - **TYPEMOTOR (0)**: Findet alle angeschlossenen Motoren  
  > - **TYPECOLORSENS (1)**: Findet alle angeschlossenen Farbsensoren  

### Rückgabewert

- **list[int]**  
  > Eine Liste aller Port-Nummern (0-5), an denen das gesuchte Gerät gefunden wurde.  
  > Beispiel: `[0, 4]` bedeutet Geräte an Port A und E.  
  > Leere Liste `[]`, wenn kein Gerät gefunden wurde.  

### Beispiel
```python
# Finde alle Motoren
motors = robot.auto_detect_device(robot.TYPEMOTOR)
print(f"Motoren gefunden an Ports: {motors}")

# Finde Farbsensoren
sensors = robot.auto_detect_device(robot.TYPECOLORSENS)
print(f"Farbsensoren gefunden an Ports: {sensors}")
```

---

## DriveBase.collided()  

Prüft, ob eine Kollision durch Vergleich der Motorlast (Duty Cycle) erkannt wurde.  
Wird von `till_collide()` verwendet.  

### Parameter  

- **cycl** (typ: float)  
  > Der aktuelle Duty-Cycle-Wert (Motorlast in Prozent, typisch 0-10000).  

- **start_cycl** (typ: float)  
  > Der Duty-Cycle-Wert zu Beginn der Fahrt als Referenz.  

- **gate** (typ: int; default: 300)  
  > Der Schwellenwert für die Laständerung. Bei Überschreitung wird Kollision erkannt.  
  > Beispiel: `gate=300` bedeutet ≥300% Lasterhöhung = Kollision.  

### Rückgabewert

- **bool**  
  > **True**: Kollision erkannt (Lastunterschied > gate)  
  > **False**: Keine Kollision (normale Fahrt)  

---

## DriveBase.convert_abs()  

Normalisiert einen beliebigen Winkelwert in den standardisierten Bereich von 0-360 Grad.  
Nützlich für Winkelberechnungen, die über 360° oder unter 0° gehen.  

### Parameter  

- **abs_pos** (typ: int; default: 0) [Grad]  
  > Die zu konvertierende absolute Position (kann auch negativ oder >360° sein).  
  > Beispiele: -45° → 315°, 450° → 90°, 720° → 0°  

### Rückgabewert

- **int** [Grad]  
  > Der normalisierte Winkel im Bereich 0-360 Grad.  
  > Der Wert ist immer ≥0 und <360.  

### Beispiel
```python
angle = robot.convert_abs(-45)  # Ergebnis: 315
print(f"Normalisierter Winkel: {angle}°")
```

---

## DriveBase.around_kollision()  

**[INTERNE HILFSFUNKTION]**  
Hilfsfunktion zur Kollisionsvermeidung während der Fahrt.  
Wird von anderen Funktionen intern aufgerufen. **Nicht direkt verwenden!**  

### Parameter  

- **timestamp** (typ: int) [Millisekunden]  
  > Der aktuelle Zeitstempel für zeitbasierte Berechnungen.  

- **power** (typ: float)  
  > Die aktuelle Motorleistung (Duty Cycle).  

- **old_power** (typ: float)  
  > Die Motorleistung vom vorherigen Durchlauf zum Vergleich.  

- **steering** (typ: int)  
  > Der aktuelle Lenkwert (-100 bis +100).  

- **speed** (typ: int) [Grad/Sekunde]  
  > Die Fahrgeschwindigkeit des Roboters.  

---

[← Zurück: Motorinteraktionen](Einfache-Motorinteraktionen) | [🏠 Home](Home) | [Weiter: Gyro-Funktionen →](Gyro-Funktionen)
