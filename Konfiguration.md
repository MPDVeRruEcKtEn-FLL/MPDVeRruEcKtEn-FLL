# Konfiguration der DriveBase

[🏠 Home](Home) | [Next: Motorinteraktionen →](Einfache-Motorinteraktionen)

---

## DriveBase.configure()  

Konfiguriert die DriveBase mit den Hardware-Ports und mechanischen Eigenschaften des Roboters.  

### Parameter  

- **motor_right_port** (typ: int; default: 0)  
  > Der Port des rechten Antriebsmotors am LEGO Hub (Port A-F, als Zahl 0-5).  

- **motor_left_port** (typ: int; default: 4)  
  > Der Port des linken Antriebsmotors am LEGO Hub (Port A-F, als Zahl 0-5).  

- **addition_port** (typ: int; default: 3)  
  > Der Port des Zusatzmotors für Anbauteile oder Werkzeuge.  

- **action_port** (typ: int; default: 5)  
  > Der Port des Aktionsmotors für spezielle Aufgaben (z.B. Greifer, Klappe).  

- **color_sensor_port** (typ: int; default: 2)  
  > Der Port des Farbsensors zur Linien- und Farberkennung.  

- **motor_pair_id** (typ: int; default: 0)  
  > Die eindeutige ID des Hauptmotorpaares für synchrone Steuerung (0-2).  

- **wheel_circumference** (typ: float; default: 17.6) [cm]  
  > Der Umfang der Antriebsräder in Zentimetern. Wird für die Distanzberechnung verwendet. Berechnung: π × Durchmesser.

---

### Beispiel

```python
from DriveBase import DriveBase

robot = DriveBase()
robot.configure(
    motor_right_port=0,      # Port A
    motor_left_port=4,       # Port E
    color_sensor_port=2,     # Port C
    wheel_circumference=17.6 # für 5,6cm Durchmesser
)
```

---

[🏠 Home](Home) | [Next: Motorinteraktionen →](Einfache-Motorinteraktionen)
