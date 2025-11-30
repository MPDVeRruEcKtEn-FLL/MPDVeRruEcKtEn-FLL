# Einfache Motorinteraktionen

[← Zurück: Konfiguration](Konfiguration) | [🏠 Home](Home) | [Weiter: Berechnungen →](Berechnungen)

---

Dieser Abschnitt erklärt die simplen Funktionen zum Steuern der Motoren.

---

## DriveBase.run_motor_duration()  

Startet einen oder mehrere Motoren für eine bestimmte Zeitdauer.  
Bei Zeit ≤ 0 läuft der Motor dauerhaft, bis er manuell gestoppt wird.  

### Parameter  

- **speed** (typ: int; default: 500) [Grad/Sekunde]
  > Die Drehgeschwindigkeit des Motors. Positive Werte = vorwärts, negative Werte = rückwärts.  

- **duration** (typ: float; default: 5) [Sekunden]
  > Die Laufzeit des Motors. Bei ≤ 0 läuft der Motor endlos weiter.  

- **ports** (typ: int) **[ERFORDERLICH]**  
  > Die Port-Nummer(n) der zu steuernden Motoren. Muss zwingend angegeben werden.  

### Beispiel
```python
# Motor an Port 3 für 2 Sekunden mit 300°/s
robot.run_motor_duration(speed=300, duration=2, ports=3)
```

---

## DriveBase.run_motor_degree()  

Dreht einen oder mehrere Motoren um einen bestimmten Winkel und wartet, bis die Position erreicht ist.  

### Parameter  

- **speed** (typ: int; default: 500) [Grad/Sekunde]
  > Die Drehgeschwindigkeit des Motors. Höhere Werte = schneller, aber weniger präzise.  

- **degree** (typ: float; default: 90) [Grad]
  > Der Drehwinkel relativ zur aktuellen Position. Positiv = eine Richtung, negativ = entgegengesetzt.

- **ports** (typ: int) **[ERFORDERLICH]**  
  > Die Port-Nummer(n) der zu steuernden Motoren. Muss zwingend angegeben werden.  

- **tolerance** (typ: float; default: 5) [Grad]  
  > Die zulässige Abweichung zwischen Soll- und Ist-Position. Kleinere Werte = präziser, aber langsamer.  

### Beispiel
```python
# Drehe Motor um 180° mit hoher Präzision
robot.run_motor_degree(speed=400, degree=180, ports=5, tolerance=2)
```

---

## DriveBase.run_action_duration()  

Dreht den Aktionsmotor (z.B. für Greifer oder Werkzeuge) für eine bestimmte Zeit.  

### Parameter  

- **speed** (typ: float; default: 360) [Grad/Sekunde]  
  > Die Drehgeschwindigkeit des Aktionsmotors. Kann positiv oder negativ sein.  

- **duration** (typ: float; default: 5) [Sekunden]  
  > Die Laufzeit des Aktionsmotors. Nach Ablauf stoppt der Motor automatisch.  

### Beispiel
```python
# Greifer 1.5 Sekunden öffnen
robot.run_action_duration(speed=500, duration=1.5)
```

---

## DriveBase.run_action_degree()  

Dreht den Aktionsmotor um einen relativen Winkel (nicht zu einer absoluten Position).  
Beispiel: Wenn der Motor bei 45° steht und degree=90, dreht er zu 135°.  

### Parameter  

- **speed** (typ: int; default: 700) [Grad/Sekunde]  
  > Die Drehgeschwindigkeit des Aktionsmotors während der Bewegung.  

- **degree** (typ: float; default: 90) [Grad]  
  > Der relative Drehwinkel. Die Drehung erfolgt von der aktuellen Position aus.  

### Beispiel
```python
# Klappe um 120° öffnen
robot.run_action_degree(speed=600, degree=120)
```

---

## DriveBase.run_to_absolute_position()  

Dreht Motoren zu einer absoluten Position (nicht relativ zur aktuellen Position).  
Die Position ist der tatsächliche Winkelwert des Motorencoders.  

### Parameter  

- **position** (typ: int; default: 0) [Grad]  
  > Die absolute Zielposition des Motors (z.B. 0° = Nullpunkt, 360° = eine volle Umdrehung).  

- **speed** (typ: int; default: 500) [Grad/Sekunde]  
  > Die Geschwindigkeit der Bewegung zur Zielposition.  

- **ports** (typ: tuple[int, ...])  
  > Ein Tupel der Port-Nummern, die gesteuert werden sollen, z.B. (0, 4) für beide Antriebsmotoren.

### Beispiel
```python
# Beide Räder auf Position 0 (Nullpunkt)
robot.run_to_absolute_position(position=0, speed=400, ports=(0, 4))
```

---

## DriveBase.run_to_relative_position()  

Dreht Motoren um eine relative Position ausgehend von der aktuellen Position.  
Beispiel: Aktuell bei 100°, position=50 → dreht zu 150°.  

### Parameter  

- **position** (typ: int; default: 0) [Grad]  
  > Die relative Drehung ausgehend von der aktuellen Position. Kann positiv oder negativ sein.  

- **speed** (typ: int; default: 500) [Grad/Sekunde]  
  > Die Geschwindigkeit der relativen Bewegung.  

- **ports** (typ: tuple[int, ...])  
  > Ein Tupel der Port-Nummern, z.B. (3,) für nur den Zusatzmotor oder (0, 4) für beide Räder.

### Beispiel
```python
# Zusatzmotor 90° weiterdrehen
robot.run_to_relative_position(position=90, speed=300, ports=(3,))
```

---

## DriveBase.attach_addition()  

Steuert den Zusatzmotor, um ein Anbauteil am Roboter zu befestigen oder zu lösen.  
Nützlich für Werkzeuge, die während der Mission gewechselt werden.  

### Parameter  

- **attach** (typ: bool; default: True)  
  > **True**: Anbauteil befestigen (Motor dreht in Befestigungsposition).  
  > **False**: Anbauteil lösen (Motor dreht in Löseposition).

### Beispiel
```python
# Anbauteil befestigen
robot.attach_addition(attach=True)

# Später: Anbauteil lösen
robot.attach_addition(attach=False)
```

---

## DriveBase.reset_null()  

Setzt die Encoder-Position eines oder mehrerer Motoren auf Null zurück.  
Nützlich zum Kalibrieren oder zum Festlegen eines neuen Referenzpunkts.  

### Parameter  

- **ports** (typ: tuple[int])  
  > Ein Tupel der Port-Nummern, deren Position auf 0° gesetzt werden soll, z.B. (0, 4).

### Beispiel
```python
# Beide Antriebsmotoren auf 0 setzen
robot.reset_null(ports=(0, 4))
```

---

## DriveBase.stop_motor()  

Stoppt sofort einen oder mehrere Motoren und hält sie in der aktuellen Position.  

### Parameter  

- **ports** (typ: tuple[int])  
  > Ein Tupel der Port-Nummern, die gestoppt werden sollen, z.B. (0,) oder (0, 4, 5).

### Beispiel
```python
# Alle Motoren stoppen
robot.stop_motor(ports=(0, 3, 4, 5))
```

---

[← Zurück: Konfiguration](Konfiguration) | [🏠 Home](Home) | [Weiter: Berechnungen →](Berechnungen)
