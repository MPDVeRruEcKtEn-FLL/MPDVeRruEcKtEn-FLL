# Gyro Functions Overview

[← Back: Calculations](Calculations-EN) | [🏠 Home](Home)

---

This section describes the functions that are used with the gyro sensor.

---

## 📋 Contents

### Precise Positioning
- **[drive_distance()](Gyro-drive-distance-EN)** - Drives precise distances with gyro correction
- **[turn_to_angle()](Gyro-turn-to-angle-EN)** - Turns precisely to an angle

### Sensor-Based Navigation
- **[turn_till_color()](Gyro-Sensor-Functions-EN#turn_till_color)** - Rotates until color detected
- **[turn_till_reflect()](Gyro-Sensor-Functions-EN#turn_till_reflect)** - Rotates until reflection detected
- **[till_color()](Gyro-Sensor-Functions-EN#till_color)** - Drives until color detected
- **[till_collide()](Gyro-Sensor-Functions-EN#till_collide)** - Drives until collision

### Tips & Best Practices
- **[Tips for Optimal Performance](Gyro-Tips-EN)**

---

## When to Use Which Function?

### ✅ Precise Positioning
Use these functions when you need exact distances or angles:
- **drive_distance():** For precise distances (e.g., "drive 50cm")
- **turn_to_angle():** For precise angles (e.g., "turn to 90°")

### 🔍 Sensor-Based Navigation
Use these functions when you want to react to environmental conditions:
- **till_color() / turn_till_color():** For color or line detection
- **turn_till_reflect():** For light/dark detection (better for lines)
- **till_collide():** For wall detection or position determination

### 🔄 Combinations
The strength lies in the combination:

```python
# 1. Drive to playing field edge
robot.drive_distance(distance=50, mainspeed=600)

# 2. Turn towards the line
robot.turn_to_angle(target_angle=90)

# 3. Drive to black line
robot.till_color(speed=400, color_type=3, color_gate=25)

# 4. Follow line by rotating
robot.turn_till_color(direction=-1, color_type=0, color_gate=50)
```

---

## Detailed Function Descriptions

Select a function for detailed information:

### 🎯 [drive_distance()](Gyro-drive-distance-EN)
- Functionality & PID control
- Parameter explanations
- Acceleration & braking profiles
- Usage examples
- Re-alignment

### 🔄 [turn_to_angle()](Gyro-turn-to-angle-EN)
- Adaptive PID control
- Turn types (Tank, Left, Right)
- Parameter tuning guide
- Smart stop mechanism
- Global turn value

### 🌈 [Sensor Functions](Gyro-Sensor-Functions-EN)
- turn_till_color()
- turn_till_reflect()
- till_color()
- till_collide()

### 💡 [Tips & Best Practices](Gyro-Tips-EN)
- PID tuning
- Speed selection
- Timeout values
- Sensor calibration
- Global turn value management

---

[← Back: Calculations](Calculations-EN) | [🏠 Home](Home)
