# drive_distance()

[← Back: Gyro Functions](Gyro-Functions-EN) | [🏠 Home](Home) | [Next: turn_to_angle() →](Gyro-turn-to-angle-EN)

---

## Overview

The `drive_distance()` function enables the robot to drive a precise distance while the gyro sensor continuously corrects the orientation. The function uses PID control for direction correction and implements intelligent acceleration and braking profiles.

---

## Parameters

### distance (int, default: 100) [cm]
The distance to drive in centimeters. 
- **Positive:** Drive forward
- **Negative:** Drive backward
- **-1:** Drive endlessly (until manual stop)

### mainspeed (int, default: 600) [°/s]
The maximum speed during the drive. Reached smoothly through acceleration.

### stopspeed (float, default: 300) [°/s]
The target speed at the end of the distance. Prevents abrupt stopping.

### re_align (bool, default: True)
- **True:** Robot turns back to exact starting angle after drive
- **False:** Small angle deviations are accepted

### isolated_drive (bool, default: False)
- **True:** Drives independent of global reference angle (for sub-maneuvers)
- **False:** Uses globally stored angle as reference

### stop (bool, default: True)
- **True:** Robot stops automatically at the end
- **False:** Motors keep running (for smooth transitions)

### brake_start (float, default: 0.7)
Percentage value (0.0-1.0) when braking begins.
- **0.7:** Braking starts at 70% of distance
- **0.9:** Late braking (faster, less smooth)
- **0.5:** Early braking (slower, very smooth)

### timestep (int, default: 100) [ms]
Time interval between PID calculations.
- **Smaller values:** More reactive but unstable
- **Larger values:** More stable but sluggish

### avoid_collision (bool, default: False)
⚠️ **NOT YET IMPLEMENTED** - Planned for automatic collision detection

---

## How It Works in Detail

### 1. Initialization
```python
# Reset motors to 0
motor.reset_relative_position(motor_right, 0)
motor.reset_relative_position(motor_left, 0)

# Determine starting angle
start_angle = gyro.yaw_angle() if isolated_drive else global_turn_value

# Calculate target rotation
rotate_distance = (distance / wheel_circumference) * 360

# Calculate brake point
brake_point = rotate_distance * brake_start
```

### 2. PID Control

**Error Calculation:**
```python
error = current_gyro - start_angle
```

**PID Components:**
- **P (Proportional):** Reacts to current deviation
- **I (Integral):** Corrects cumulative errors
- **D (Derivative):** Dampens oscillations

**Steering Calculation:**
```python
steering = (error * P) + (integral * I) + ((error - old_error) * D)
steering = max(-100, min(100, steering))  # Limit
```

### 3. Speed Profile

The function goes through three phases:

#### Phase 1: Acceleration
```
Speed
  ▲
  │     ┌─────────────
  │    ╱  Constant
  │   ╱
  │  ╱  Acceleration
  │ ╱
  └─────────────────────► Distance
```

#### Phase 2: Constant Speed
Drives at `mainspeed`

#### Phase 3: Braking (from brake_start)
```python
if driven >= brake_point:
    steering = 0  # No steering while braking
    speed = decelerate_to(stopspeed)
```

### 4. Re-Alignment

If `re_align=True`:
```python
# After drive: Correct angle deviation
current_angle = gyro.yaw_angle()
if abs(current_angle - global_turn_value) > 0.5:
    turn_to_angle(global_turn_value)
```

---

## Usage Examples

### Simple Drive
```python
# Drive 50cm forward with default settings
robot.drive_distance(distance=50, mainspeed=600)
```

### Precise Drive with Slow Stop
```python
robot.drive_distance(
    distance=100, 
    mainspeed=800,      # Drive fast
    stopspeed=200,      # Stop slowly
    brake_start=0.8     # Brake over last 20%
)
```

### Backward Drive
```python
# 30cm backward
robot.drive_distance(
    distance=-30,
    mainspeed=500
)
```

### Isolated Drive without Global Alignment
```python
# For complex maneuvers without global angle update
robot.drive_distance(
    distance=50,
    isolated_drive=True,  # Ignores global_turn_value
    re_align=False        # No realignment at end
)
```

### Endless Drive (until manual stop)
```python
# Useful for manual control
robot.drive_distance(
    distance=-1,      # Drive endlessly
    mainspeed=500,
    stop=False        # Doesn't stop automatically
)

# Later, stop manually:
robot.stop_motor(ports=(0, 4))
```

### Very Smooth Drive
```python
robot.drive_distance(
    distance=80,
    mainspeed=400,
    stopspeed=150,
    brake_start=0.5    # Brake over last 50%
)
```

---

## Troubleshooting

### Problem: Robot weaves/snakes

**Solution:** Adjust PID values
```python
# In DriveBase.py adjust the get_pids() function
# Reduce P and D for more stable drive
```

### Problem: Robot corrects too slowly

**Solution:** Increase P value or decrease timestep
```python
robot.drive_distance(distance=50, timestep=50)  # More reactive
```

### Problem: Robot doesn't reach target accurately

**Solution:** Calibrate wheel circumference
```python
# Measure actual distance and adjust:
robot.configure(wheel_circumference=17.8)  # Default: 17.6
```

---

## See Also

- **[turn_to_angle()](Gyro-turn-to-angle-EN)** - Precise turns
- **[Tips & Best Practices](Gyro-Tips-EN)** - Optimization hints
- **[till_color()](Gyro-Sensor-Functions-EN#till_color)** - Drive until color detected

---

[← Back: Gyro Functions](Gyro-Functions-EN) | [🏠 Home](Home) | [Next: turn_to_angle() →](Gyro-turn-to-angle-EN)
