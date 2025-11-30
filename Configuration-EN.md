# Configuration

[🏠 Home](Home) | [Next: Motor Interactions →](Simple-Motor-Interactions-EN)

---

## DriveBase.configure()  

Configures the DriveBase with the hardware ports and mechanical characteristics of the robot.  

### Parameters  

- **motor_right_port** (type: int; default: 0)  
  > The port of the right drive motor on the LEGO Hub (Port A-F, as number 0-5).  

- **motor_left_port** (type: int; default: 4)  
  > The port of the left drive motor on the LEGO Hub (Port A-F, as number 0-5).  

- **addition_port** (type: int; default: 3)  
  > The port of the additional motor for attachments or tools.  

- **action_port** (type: int; default: 5)  
  > The port of the action motor for special tasks (e.g., gripper, flap).  

- **color_sensor_port** (type: int; default: 2)  
  > The port of the color sensor for line and color detection.  

- **motor_pair_id** (type: int; default: 0)  
  > The unique ID of the main motor pair for synchronous control (0-2).  

- **wheel_circumference** (type: float; default: 17.6) [cm]  
  > The circumference of the drive wheels in centimeters. Used for distance calculation. Formula: π × diameter.

---

### Example

```python
from DriveBase import DriveBase

robot = DriveBase()
robot.configure(
    motor_right_port=0,      # Port A
    motor_left_port=4,       # Port E
    color_sensor_port=2,     # Port C
    wheel_circumference=17.6 # for 5.6cm diameter
)
```

---

[🏠 Home](Home) | [Next: Motor Interactions →](Simple-Motor-Interactions-EN)
