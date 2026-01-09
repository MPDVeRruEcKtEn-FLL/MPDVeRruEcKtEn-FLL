# Gyro Sensor Functions

[← Back: turn_to_angle()](Gyro-turn-to-angle-EN) | [🏠 Home](Home) | [Next: Tips →](Gyro-Tips-EN)

---

## Overview

The sensor functions combine precise movement with color sensor feedback. They enable the robot to react to environmental conditions and navigate flexibly.

---

## 📋 Contents

1. **[turn_till_color()](#turn_till_color)** - Turn until color detected
2. **[turn_till_reflect()](#turn_till_reflect)** - Turn until reflection detected
3. **[till_color()](#till_color)** - Drive until color detected
4. **[till_collide()](#till_collide)** - Drive until collision

---

## turn_till_color()

Turns the robot until the color sensor detects a specific color.

### Parameters

#### direction (int, default: 1)
Turn direction:
- **1:** Right turn (clockwise)
- **-1:** Left turn (counterclockwise)

#### speed (int, default: 250) [°/s]
Turn speed. Slower speeds are more precise.

#### color_type (int, default: 0)
Type of color detection:
- **0:** Reflected Light (reflection, 0-100%)
- **1:** RGB (Red value, 0-1024)
- **2:** RGB (Green value, 0-1024)
- **3:** RGB (Blue value, 0-1024)
- **4:** Color ID (0-10: specific colors)

#### color_gate (int, default: 50)
Threshold for detection:
- For **color_type=0 (Reflected):** Brightness (e.g., 50 = 50%)
- For **color_type=1-3 (RGB):** Color intensity (0-1024)
- For **color_type=4 (Color ID):** Color ID (0=black, 3=blue, 5=red, etc.)

#### mode (str, default: "greater")
Comparison mode:
- **"greater":** Stop when value > color_gate (e.g., line gets brighter)
- **"lower":** Stop when value < color_gate (e.g., line gets darker)

#### timeout (int, default: 5000) [ms]
Maximum time for the turn.

#### timestep (int, default: 50) [ms]
Time interval between sensor queries.

### Usage Examples

#### Turn to Black Line (Reflection)
```python
# Turn right until black line detected (dark = low reflection)
robot.turn_till_color(
    direction=1,         # Turn right
    speed=250,
    color_type=0,        # Reflection
    color_gate=25,       # Threshold
    mode="lower"         # Stop when darker than 25%
)
```

#### Turn to White Line (Reflection)
```python
# Turn left until white line detected (bright = high reflection)
robot.turn_till_color(
    direction=-1,        # Turn left
    speed=250,
    color_type=0,        # Reflection
    color_gate=75,       # Threshold
    mode="greater"       # Stop when brighter than 75%
)
```

#### Turn to Red Zone (Color ID)
```python
# Turn until red color detected
robot.turn_till_color(
    direction=1,
    speed=200,
    color_type=4,        # Color ID
    color_gate=5,        # 5 = Red
    mode="greater"       # Stop when color ID >= 5
)
```

#### Turn to Blue Component (RGB)
```python
# Turn until lots of blue detected
robot.turn_till_color(
    direction=-1,
    speed=250,
    color_type=3,        # Blue value
    color_gate=300,      # Threshold
    mode="greater"       # Stop when blue > 300
)
```

---

## turn_till_reflect()

Simplified version of `turn_till_color()` specifically for reflection values. Particularly useful for line detection.

### Parameters

#### direction (int, default: 1)
Turn direction (1=right, -1=left)

#### speed (int, default: 250) [°/s]
Turn speed

#### reflect_gate (int, default: 50) [%]
Reflection threshold (0-100%)

#### mode (str, default: "greater")
Comparison mode ("greater" or "lower")

#### timeout (int, default: 5000) [ms]
Maximum time

#### timestep (int, default: 50) [ms]
Time interval

### Usage Examples

#### Simple Line Detection
```python
# Turn to black line
robot.turn_till_reflect(
    direction=1,
    reflect_gate=25,     # Dark = < 25%
    mode="lower"
)
```

#### Search White Marker
```python
# Turn to bright marker
robot.turn_till_reflect(
    direction=-1,
    reflect_gate=80,
    mode="greater"
)
```

---

## till_color()

Drives straight until the color sensor detects a specific color.

### Parameters

#### speed (int, default: 400) [°/s]
Drive speed

#### color_type (int, default: 0)
Type of color detection (same as turn_till_color)

#### color_gate (int, default: 50)
Threshold (same as turn_till_color)

#### mode (str, default: "greater")
Comparison mode (same as turn_till_color)

#### timeout (int, default: 5000) [ms]
Maximum drive time

#### timestep (int, default: 50) [ms]
Time interval

### Usage Examples

#### Drive to Black Line
```python
# Drive forward until black line detected
robot.till_color(
    speed=400,
    color_type=0,        # Reflection
    color_gate=25,       # Dark
    mode="lower"
)
```

#### Drive to White Zone
```python
# Drive until bright zone
robot.till_color(
    speed=400,
    color_type=0,
    color_gate=75,
    mode="greater"
)
```

#### Drive to Blue Zone (Color ID)
```python
# Drive until blue color
robot.till_color(
    speed=300,
    color_type=4,        # Color ID
    color_gate=3,        # 3 = Blue
    mode="greater"
)
```

#### Backward to Line
```python
# Drive backward to line
robot.till_color(
    speed=-400,          # Negative = backward
    color_type=0,
    color_gate=25,
    mode="lower"
)
```

---

## till_collide()

Drives straight until the force sensor detects a collision.

### Parameters

#### speed (int, default: 400) [°/s]
Drive speed

#### force_gate (int, default: 5) [N]
Force threshold for collision detection (Newton)

#### timeout (int, default: 5000) [ms]
Maximum drive time

#### timestep (int, default: 50) [ms]
Time interval

### Usage Examples

#### Drive to Wall
```python
# Drive gently to wall
robot.till_collide(
    speed=300,
    force_gate=3         # Low force = gentle
)
```

#### Fast Positioning
```python
# Drive fast to wall
robot.till_collide(
    speed=600,
    force_gate=8,        # Higher force OK at speed
    timeout=3000
)
```

#### Backward to Wall
```python
# Position backward
robot.till_collide(
    speed=-400,          # Backward
    force_gate=5
)
```

---

## Combination Examples

### Complex Navigation with Sensors

#### Example 1: Find and Follow Line
```python
# 1. Drive forward to line
robot.drive_distance(distance=40, mainspeed=600)

# 2. Turn to line (if not perfectly aligned)
robot.turn_till_reflect(direction=1, reflect_gate=25, mode="lower")

# 3. Drive along the line
robot.till_color(speed=400, color_type=0, color_gate=25, mode="lower")
```

#### Example 2: Precise Positioning
```python
# 1. Drive to wall
robot.till_collide(speed=400, force_gate=5)

# 2. Back up 3cm
robot.drive_distance(distance=-3, mainspeed=400)

# 3. Turn to precise angle
robot.turn_to_angle(target_angle=90)

# 4. Drive to color marker
robot.till_color(speed=300, color_type=4, color_gate=5, mode="greater")
```

#### Example 3: Color-Based Decision
```python
# Drive to first line
robot.till_color(speed=400, color_type=0, color_gate=25, mode="lower")

# Read color
color = robot.color.get()[0]

# Decide based on color
if color == 5:  # Red
    robot.turn_to_angle(target_angle=90)
elif color == 3:  # Blue
    robot.turn_to_angle(target_angle=-90)
else:  # Other
    robot.turn_to_angle(target_angle=180)

# Drive further
robot.drive_distance(distance=30, mainspeed=600)
```

---

## Tips for Sensor Functions

### ✅ Calibrate Reflection Values

Always test before competition:
```python
# Test code for reflection values
import time
from hub import light_matrix, port

color_sensor = port.A  # Adjust!

for i in range(10):
    reflected = color_sensor.device.get()[0]
    print(f"Reflection: {reflected}%")
    time.sleep(0.5)
```

### ✅ Adjust Speed

- **Slow (200-300):** Precise detection, reacts faster
- **Medium (400-500):** Good compromise
- **Fast (600+):** May overshoot target

### ✅ Choose Mode Correctly

- **"greater":** For transition from dark to bright
- **"lower":** For transition from bright to dark

### ✅ Don't Forget Timeout

Always set a realistic timeout:
```python
robot.till_color(
    speed=400,
    color_type=0,
    color_gate=25,
    mode="lower",
    timeout=3000  # Stop after 3 seconds
)
```

### ✅ Consider Sensor Position

The sensor must be close enough to the ground for reliable values:
- **Optimal:** 5-10mm distance
- **Too high:** Unreliable readings
- **Too low:** Can get stuck

---

## Color Value Reference

### Color ID Values (color_type=4)
```
0  = Black
1  = Violet
2  = Blue
3  = Cyan
4  = Green
5  = Yellow
6  = Red
7  = White
-1 = No color detected
```

### Reflection Values (color_type=0)
```
0-20%   = Black / very dark
20-40%  = Dark gray
40-60%  = Gray
60-80%  = Light gray
80-100% = White / very bright
```

---

## Troubleshooting

### Problem: Sensor doesn't detect reliably

**Solution:**
1. Check sensor position (distance to ground)
2. Check room lighting
3. Adjust threshold
4. Slower speed

### Problem: Robot drives too far over line

**Solution:**
```python
# Slower speed
robot.till_color(speed=250, ...)  # instead of 400

# Or shorter timestep
robot.till_color(speed=400, timestep=30, ...)  # instead of 50
```

### Problem: Timeout is reached

**Solution:**
1. Increase timeout
2. Check if target color actually exists
3. Adjust threshold

---

## See Also

- **[drive_distance()](Gyro-drive-distance-EN)** - Drive precise distances
- **[turn_to_angle()](Gyro-turn-to-angle-EN)** - Precise turns
- **[Tips & Best Practices](Gyro-Tips-EN)** - Optimization hints

---

[← Back: turn_to_angle()](Gyro-turn-to-angle-EN) | [🏠 Home](Home) | [Next: Tips →](Gyro-Tips-EN)
