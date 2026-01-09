# turn_to_angle()

[← Back: drive_distance()](Gyro-drive-distance-EN) | [🏠 Home](Home) | [Next: Sensor Functions →](Gyro-Sensor-Functions-EN)

---

## Overview

The `turn_to_angle()` function turns the robot precisely to an absolute angle. It uses adaptive PID control that automatically adjusts to the turn size and implements different turn types (Tank, Left, Right).

---

## Parameters

### target_angle (int, default: 0) [°]
The absolute target angle in degrees.
- **0°:** Starting position (where the robot was initialized)
- **90°:** 90° right from starting position
- **-90°:** 90° left from starting position
- **180° / -180°:** Turn around completely

**Important:** The function always turns the shortest way to the target angle.

### speed (int, default: 300) [°/s]
The turn speed. 
- **200-400:** Slow and precise
- **400-600:** Standard speed
- **600-800:** Fast (less precise)

### type (int, default: 0)
Determines the turn type:
- **0:** Tank Turn (both wheels turn in opposite directions)
- **1:** Left fixed (only right wheel turns)
- **2:** Right fixed (only left wheel turns)

### threshold (float, default: 0.5) [°]
Accuracy threshold - how close to the target angle must the robot be?
- **0.5°:** Standard precision
- **0.1°:** Very precise (slower)
- **1.0°:** Less precise (faster)

### timeout (int, default: 5000) [ms]
Maximum time for the turn. Prevents endless oscillation.
- **3000:** Quick turns
- **5000:** Standard
- **10000:** For very precise/slow turns

### timestep (int, default: 50) [ms]
Time interval between PID calculations.
- **30-50:** Very reactive
- **50-100:** Standard
- **100-200:** Slower, more stable

---

## How It Works in Detail

### 1. Angle Calculation

```python
# Read current angle from gyro
current_angle = gyro.yaw_angle()

# Calculate error
error = target_angle - current_angle

# Find shortest path
if error > 180:
    error -= 360
elif error < -180:
    error += 360
```

**Example:**
- Current: 170°
- Target: -170°
- Naive error: -340°
- Corrected error: 20° (shortest path)

### 2. Adaptive PID Control

The function automatically adapts PID parameters to the turn size:

```python
def get_pids(error):
    if abs(error) > 45:
        # Large turn: Fast but stable
        return (4.0, 0.01, 15.0)  # (P, I, D)
    elif abs(error) > 10:
        # Medium turn: Balanced
        return (3.5, 0.02, 12.0)
    else:
        # Small turn: Precise
        return (3.0, 0.03, 10.0)
```

**PID Components:**

#### P (Proportional): Main drive
```python
P_component = error * P_gain
```
The larger the error, the faster the turn.

#### I (Integral): Long-term correction
```python
integral += error * timestep
I_component = integral * I_gain
```
Corrects small, persistent deviations.

#### D (Derivative): Damping
```python
derivative = (error - old_error) / timestep
D_component = derivative * D_gain
```
Prevents overshooting and oscillation.

**Total control:**
```python
steering = P_component + I_component + D_component
steering = max(-100, min(100, steering))  # Limit to ±100
```

### 3. Turn Types

#### Type 0: Tank Turn (Default)
```python
# Both wheels turn oppositely
left_speed = speed * (steering / 100)
right_speed = -speed * (steering / 100)
```

**Advantage:** Fast, turns in place
**Disadvantage:** Can slightly shift position

#### Type 1: Left fixed
```python
# Only right wheel turns
left_speed = 0
right_speed = speed * (steering / 100)
```

**Advantage:** Position stays constant (left side)
**Disadvantage:** Slower, larger radius

#### Type 2: Right fixed
```python
# Only left wheel turns
left_speed = speed * (steering / 100)
right_speed = 0
```

**Advantage:** Position stays constant (right side)
**Disadvantage:** Slower, larger radius

### 4. Smart Stop Mechanism

```python
# Stop when:
# 1. Within threshold AND
# 2. Speed near zero AND
# 3. Stable for at least 100ms

if abs(error) < threshold:
    if avg_speed < 5:  # Practically still
        stable_count += 1
        if stable_count >= 2:  # 2 × 50ms = 100ms
            break
```

This prevents:
- Premature stopping during overshoot
- Oscillation around target point
- Jittery behavior

### 5. Global Turn Value Update

```python
# At the end: Save actual angle
global global_turn_value
global_turn_value = gyro.yaw_angle()
```

This value is used as reference by other functions.

---

## Usage Examples

### Simple Turns
```python
# Turn 90° right
robot.turn_to_angle(target_angle=90)

# Turn 90° left
robot.turn_to_angle(target_angle=-90)

# Return to start position
robot.turn_to_angle(target_angle=0)

# Turn 180°
robot.turn_to_angle(target_angle=180)
```

### Precise Turn
```python
# Very accurately turn to 45°
robot.turn_to_angle(
    target_angle=45,
    speed=250,          # Slow
    threshold=0.2,      # Very accurate
    timeout=8000        # More time
)
```

### Fast Turn
```python
# Quickly turn to -90°
robot.turn_to_angle(
    target_angle=-90,
    speed=600,          # Fast
    threshold=1.0,      # Less accurate
    timeout=3000
)
```

### Turn with Fixed Wheel
```python
# Left wheel fixed (e.g., against wall)
robot.turn_to_angle(
    target_angle=90,
    type=1,             # Left fixed
    speed=300
)

# Right wheel fixed
robot.turn_to_angle(
    target_angle=-45,
    type=2,             # Right fixed
    speed=300
)
```

### Sequential Navigation
```python
# Complex drive with multiple turns
robot.drive_distance(distance=50, mainspeed=600)
robot.turn_to_angle(target_angle=90)
robot.drive_distance(distance=30, mainspeed=600)
robot.turn_to_angle(target_angle=180)
robot.drive_distance(distance=50, mainspeed=600)
robot.turn_to_angle(target_angle=0)  # Back to start orientation
```

### Angle Reset
```python
# Reset gyro (new 0° position)
robot.reset_gyro()

# Now the current orientation is 0°
robot.turn_to_angle(target_angle=90)  # Turn 90° from HERE
```

---

## Combination with Other Functions

### With drive_distance()
```python
# Drive forward, turn, drive further
robot.drive_distance(distance=40, mainspeed=600)
robot.turn_to_angle(target_angle=90)
robot.drive_distance(distance=40, mainspeed=600)
```

### With Sensor Functions
```python
# Turn to angle, drive to line
robot.turn_to_angle(target_angle=45)
robot.till_color(speed=400, color_type=3, color_gate=25)
```

### Relative Turns
```python
# To turn by a relative angle, use global_turn_value:
def turn_relative(angle):
    current = robot.global_turn_value
    new_angle = (current + angle) % 360
    if new_angle > 180:
        new_angle -= 360
    robot.turn_to_angle(target_angle=new_angle)

# Example: Turn 45° right from current position
turn_relative(45)
```

---

## Understanding the Angle System

### Coordinate System
```
        -90° (270°)
            ↑
            │
-180° ←─────┼─────→ 0°
   180°     │
            ↓
           90°
```

### Examples
```python
# From 0° to 90° = 90° right turn
# From 90° to -90° = 180° (shortest path)
# From 170° to -170° = 20° right turn (shortest path!)
```

### Global Turn Value Tracking
```python
# Automatically updated after:
# - turn_to_angle()
# - drive_distance() (when re_align=True)

# Read manually:
print(robot.global_turn_value)

# Set manually:
robot.global_turn_value = 45
```

---

## Troubleshooting

### Problem: Robot oscillates around target angle

**Cause:** PID parameters too aggressive

**Solution:** Increase D value in `get_pids()`:
```python
# More damping
return (3.0, 0.02, 20.0)  # Higher D value
```

### Problem: Robot doesn't reach target angle

**Cause:** Threshold too small or timeout too short

**Solution:**
```python
robot.turn_to_angle(
    target_angle=90,
    threshold=1.0,     # Larger tolerance
    timeout=10000      # More time
)
```

### Problem: Turn too slow

**Cause:** Speed too low or P value too small

**Solution:**
```python
# Higher speed
robot.turn_to_angle(target_angle=90, speed=600)

# Or increase P value in get_pids()
return (5.0, 0.01, 15.0)  # Higher P value
```

### Problem: Doesn't turn shortest way

**Check:**
```python
# Debug code
current = robot.gyro.yaw_angle()
target = 90
error = target - current
if error > 180: error -= 360
if error < -180: error += 360
print(f"Current: {current}°, Target: {target}°, Error: {error}°")
```

### Problem: Inaccurate for small angles

**Solution:** Reduce timestep for more reactivity:
```python
robot.turn_to_angle(
    target_angle=5,
    speed=200,
    timestep=30        # More reactive
)
```

---

## Advanced Techniques

### Dynamic Speed
```python
def turn_adaptive(target_angle):
    current = robot.gyro.yaw_angle()
    error = abs(target_angle - current)
    
    if error > 180:
        error = 360 - error
    
    # Adapt speed to angle
    if error > 90:
        speed = 600
    elif error > 45:
        speed = 400
    else:
        speed = 250
    
    robot.turn_to_angle(target_angle=target_angle, speed=speed)
```

### Turn with Retry
```python
def turn_precise(target_angle, max_attempts=3):
    for attempt in range(max_attempts):
        robot.turn_to_angle(
            target_angle=target_angle,
            threshold=0.3,
            timeout=5000
        )
        
        # Check accuracy
        current = robot.gyro.yaw_angle()
        if abs(current - target_angle) < 0.5:
            return True
    
    return False  # Failed
```

### Smooth Turn with Ramp
```python
def turn_smooth(target_angle):
    current = robot.gyro.yaw_angle()
    error = target_angle - current
    
    # Normalize error
    if error > 180: error -= 360
    if error < -180: error += 360
    
    # Speed based on remaining angle
    while abs(error) > 0.5:
        speed = max(200, min(600, abs(error) * 10))
        robot.turn_to_angle(target_angle=target_angle, speed=speed, timeout=500)
        
        current = robot.gyro.yaw_angle()
        error = target_angle - current
        if error > 180: error -= 360
        if error < -180: error += 360
```

---

## Performance Tips

### ✅ Optimal Settings for Different Scenarios

**Fast Navigation:**
```python
robot.turn_to_angle(target_angle=90, speed=600, threshold=1.0)
```

**Precise Alignment:**
```python
robot.turn_to_angle(target_angle=90, speed=250, threshold=0.2, timeout=8000)
```

**Wall Alignment (fixed wheel):**
```python
robot.turn_to_angle(target_angle=90, type=1, speed=300)
```

**Battery Saving:**
```python
robot.turn_to_angle(target_angle=90, speed=300, threshold=0.8)
```

---

## See Also

- **[drive_distance()](Gyro-drive-distance-EN)** - Drive precise distances
- **[Sensor Functions](Gyro-Sensor-Functions-EN)** - Turns with sensor stop
- **[Tips & Best Practices](Gyro-Tips-EN)** - PID tuning and calibration

---

[← Back: drive_distance()](Gyro-drive-distance-EN) | [🏠 Home](Home) | [Next: Sensor Functions →](Gyro-Sensor-Functions-EN)
