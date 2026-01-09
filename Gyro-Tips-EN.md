# Tips & Best Practices

[← Back: Sensor Functions](Gyro-Sensor-Functions-EN) | [🏠 Home](Home)

---

## Overview

This page contains tips, best practices, and optimization strategies for working with gyro functions. From PID tuning to sensor calibration.

---

## 📋 Contents

1. **[PID Tuning](#pid-tuning)** - Optimal PID parameter settings
2. **[Speed Selection](#speed-selection)** - Choosing the right speeds
3. **[Timeout Values](#timeout-values)** - Setting sensible timeouts
4. **[Sensor Calibration](#sensor-calibration)** - Calibrating sensors
5. **[Global Turn Value](#global-turn-value)** - Angle management
6. **[Battery Management](#battery-management)** - Consistent performance
7. **[Debugging](#debugging)** - Finding and solving problems

---

## PID Tuning

### What is PID?

PID stands for **Proportional-Integral-Derivative** and is a control mechanism.

#### P (Proportional)
- Reacts to **current** deviation
- **Too high:** Oscillation, overshooting
- **Too low:** Slow correction
- **Typical:** 2.0 - 5.0

#### I (Integral)
- Corrects **persistent** small errors
- **Too high:** Unstable, slow
- **Too low:** Small errors remain
- **Typical:** 0.01 - 0.05

#### D (Derivative)
- Dampens **changes** (brakes)
- **Too high:** Sluggish response
- **Too low:** Overshooting
- **Typical:** 10.0 - 20.0

### Adjusting PID Values

Edit the `get_pids()` function in `DriveBase.py`:

```python
def get_pids(self, error=0):
    """PID parameters for different scenarios"""
    
    # For drive_distance():
    if abs(error) > 45:
        return (4.0, 0.01, 15.0)  # Large deviation
    elif abs(error) > 10:
        return (3.5, 0.02, 12.0)  # Medium deviation
    else:
        return (3.0, 0.03, 10.0)  # Small deviation
```

### Step-by-Step Tuning

#### 1. Set P only
```python
# Set I and D to 0
return (3.0, 0.0, 0.0)

# Increase P until oscillation begins
# Then reduce to 70%
```

#### 2. Add D
```python
# Add D to dampen oscillation
return (3.0, 0.0, 12.0)

# Increase D until stable
```

#### 3. Optimize I
```python
# I for fine-tuning
return (3.0, 0.02, 12.0)

# Increase I until no residual errors
```

### Common PID Problems

#### Problem: Robot oscillates
```python
# Solution: Reduce P, increase D
return (2.5, 0.01, 18.0)  # More damping
```

#### Problem: Robot corrects too slowly
```python
# Solution: Increase P
return (5.0, 0.01, 15.0)  # More reactive
```

#### Problem: Residual error remains
```python
# Solution: Increase I
return (3.0, 0.05, 12.0)  # More integral
```

---

## Speed Selection

### Recommended Speeds

#### Straight Drive (drive_distance)
```python
# Slow and precise
robot.drive_distance(distance=50, mainspeed=400)

# Standard
robot.drive_distance(distance=50, mainspeed=600)

# Fast
robot.drive_distance(distance=50, mainspeed=800)

# Maximum (not recommended)
robot.drive_distance(distance=50, mainspeed=1000)
```

#### Turns (turn_to_angle)
```python
# Very precise
robot.turn_to_angle(target_angle=90, speed=200)

# Standard
robot.turn_to_angle(target_angle=90, speed=300)

# Fast
robot.turn_to_angle(target_angle=90, speed=500)
```

#### Sensor Functions
```python
# Line detection (precise)
robot.till_color(speed=300, ...)

# Standard
robot.till_color(speed=400, ...)

# Fast (may overshoot)
robot.till_color(speed=600, ...)
```

### Speed vs. Precision

| Speed | Precision | Usage |
|-------|-----------|-------|
| 200-400 | ⭐⭐⭐⭐⭐ | Precise tasks |
| 400-600 | ⭐⭐⭐⭐ | Standard navigation |
| 600-800 | ⭐⭐⭐ | Fast drives |
| 800-1000 | ⭐⭐ | Only when necessary |

### Dynamic Speed

```python
def drive_adaptive(distance):
    """Adapt speed to distance"""
    if abs(distance) > 100:
        speed = 800  # Long distance = fast
    elif abs(distance) > 50:
        speed = 600  # Medium distance
    else:
        speed = 400  # Short distance = precise
    
    robot.drive_distance(distance=distance, mainspeed=speed)
```

---

## Timeout Values

### Why Timeouts are Important

Without timeout, the robot can:
- Endlessly try to reach a goal
- Get stuck if sensor is broken
- Waste time

### Recommended Timeouts

#### drive_distance()
```python
# Short distance (< 30cm)
robot.drive_distance(distance=20, timeout=2000)  # 2 seconds

# Medium distance (30-100cm)
robot.drive_distance(distance=50, timeout=5000)  # 5 seconds

# Long distance (> 100cm)
robot.drive_distance(distance=150, timeout=10000)  # 10 seconds
```

#### turn_to_angle()
```python
# Small turn (< 45°)
robot.turn_to_angle(target_angle=30, timeout=3000)

# Medium turn (45-135°)
robot.turn_to_angle(target_angle=90, timeout=5000)

# Large turn (> 135°)
robot.turn_to_angle(target_angle=180, timeout=7000)
```

#### Sensor Functions
```python
# When sensor close to target
robot.till_color(speed=400, timeout=3000)

# When sensor far from target
robot.till_color(speed=400, timeout=8000)

# Safety timeout (very long)
robot.till_color(speed=400, timeout=15000)
```

### Calculate Timeout

```python
def calculate_timeout(distance, speed):
    """Calculate sensible timeout"""
    # Time = Distance / Speed
    # + 50% buffer
    estimated_time = (abs(distance) / speed) * 1.5 * 1000
    return max(2000, min(15000, estimated_time))

# Usage:
timeout = calculate_timeout(distance=80, speed=600)
robot.drive_distance(distance=80, mainspeed=600, timeout=timeout)
```

---

## Sensor Calibration

### Calibrate Color Sensor

#### Test Reflection Values

```python
from hub import port
import time

# Initialize sensor
color_sensor = port.A  # Adjust to your port!

print("=== SENSOR CALIBRATION ===")
print("Place sensor over different surfaces")
print()

surfaces = ["BLACK", "WHITE", "GRAY", "LINE"]

for surface in surfaces:
    input(f"Place over {surface} and press Enter...")
    
    values = []
    for i in range(10):
        reflected = color_sensor.device.get()[0]
        values.append(reflected)
        time.sleep(0.1)
    
    avg = sum(values) / len(values)
    print(f"{surface}: {avg:.1f}% (min: {min(values)}, max: {max(values)})")

print("\n=== DONE ===")
```

#### Determine Thresholds

```python
# Example output:
# BLACK: 8.5% (min: 7, max: 10)
# WHITE:  92.3% (min: 90, max: 95)
# GRAY:   45.2% (min: 42, max: 48)
# LINE:  15.7% (min: 14, max: 18)

# Derive thresholds:
black_threshold = 12   # Between black and line
white_threshold = 80   # Between gray and white
line_threshold = 22    # Between line and gray
```

### Calibrate Gyro

#### Drift Test

```python
import time

# Let robot stand still
print("Let robot stand still for 10 seconds...")
start_angle = robot.gyro.yaw_angle()
time.sleep(10)
end_angle = robot.gyro.yaw_angle()

drift = end_angle - start_angle
print(f"Gyro drift: {drift}° over 10 seconds")

if abs(drift) > 2:
    print("⚠️ Warning: Gyro has high drift!")
    print("Solution: Restart hub and keep still during startup")
else:
    print("✅ Gyro drift is OK")
```

#### Accuracy Test

```python
# Test 360° turn
robot.reset_gyro()
robot.turn_to_angle(target_angle=90)
robot.turn_to_angle(target_angle=180)
robot.turn_to_angle(target_angle=270)
robot.turn_to_angle(target_angle=0)

final_angle = robot.gyro.yaw_angle()
print(f"Final angle after 360°: {final_angle}°")
print(f"Error: {abs(final_angle)}°")

if abs(final_angle) < 2:
    print("✅ Gyro very accurate")
elif abs(final_angle) < 5:
    print("⚠️ Gyro OK but not perfect")
else:
    print("❌ Gyro inaccurate - calibration needed")
```

---

## Global Turn Value

### What is Global Turn Value?

The `global_turn_value` stores the current absolute angle of the robot.

```python
# Automatically updated by:
# - turn_to_angle()
# - drive_distance() (when re_align=True)

# Read:
current_angle = robot.global_turn_value
print(f"Current angle: {current_angle}°")

# Set manually:
robot.global_turn_value = 0  # Sets current direction as 0°
```

### Best Practices

#### 1. Initialization
```python
# At start of program
robot.reset_gyro()  # Sets global_turn_value to 0
```

#### 2. Consistent Usage
```python
# CORRECT: Use turn_to_angle for absolute angles
robot.drive_distance(distance=50, mainspeed=600)
robot.turn_to_angle(target_angle=90)  # Absolute
robot.drive_distance(distance=30, mainspeed=600)
robot.turn_to_angle(target_angle=0)   # Back to start

# WRONG: Don't mix different systems
robot.drive_distance(distance=50, mainspeed=600)
robot.motor_rotate(90)  # Not recommended - no global_turn_value update
```

#### 3. Use Re-Alignment
```python
# Re-align after each drive for precision
robot.drive_distance(
    distance=50,
    mainspeed=600,
    re_align=True  # Default - good!
)
```

#### 4. Isolated Drive for Sub-Maneuvers
```python
# Complex maneuver without changing global angle
def pick_up_object():
    robot.drive_distance(distance=10, isolated_drive=True)
    # ... pick up object ...
    robot.drive_distance(distance=-10, isolated_drive=True)
    # global_turn_value remains unchanged

# Main program
robot.turn_to_angle(target_angle=90)
pick_up_object()  # Doesn't change global_turn_value
robot.drive_distance(distance=50)  # Still uses 90° as reference
```

---

## Battery Management

### Why is This Important?

Decreasing battery voltage leads to:
- Slower motors
- Less accurate movements
- Different speeds

### Battery Check Before Competition

```python
from hub import battery

voltage = battery.voltage()
capacity = battery.capacity()

print(f"Battery: {voltage}mV, {capacity}%")

if voltage < 8000:
    print("⚠️ Warning: Battery weak!")
    print("Recommendation: Replace batteries")
elif voltage < 8500:
    print("⚠️ Battery OK but replace soon")
else:
    print("✅ Battery good")
```

### Adjust Speed to Battery

```python
def get_adjusted_speed(target_speed):
    """Adjust speed to battery voltage"""
    voltage = battery.voltage()
    
    if voltage > 8500:
        return target_speed  # Full speed
    elif voltage > 8000:
        return int(target_speed * 0.9)  # 90%
    else:
        return int(target_speed * 0.8)  # 80%

# Usage:
speed = get_adjusted_speed(600)
robot.drive_distance(distance=50, mainspeed=speed)
```

---

## Debugging

### Enable Debug Output

```python
# Show values during drive_distance
def drive_distance_debug(distance, mainspeed=600):
    """drive_distance with debug output"""
    start_angle = robot.gyro.yaw_angle()
    
    # During drive
    while True:
        current_angle = robot.gyro.yaw_angle()
        error = current_angle - start_angle
        
        # Debug output
        print(f"Angle: {current_angle}°, Error: {error}°")
        
        # ... rest of function ...
```

### Common Problems

#### Problem: Robot doesn't drive straight

**Diagnosis:**
```python
# Test both motors individually
robot.motor_rotate(500, ports=(0,))  # Left
robot.motor_rotate(500, ports=(4,))  # Right

# Compare speed and distance
```

**Solution:**
- Calibrate motors
- Adjust wheel circumference
- Tune PID values

#### Problem: Turns inaccurate

**Diagnosis:**
```python
# Test 4× 90° turns
for i in range(4):
    robot.turn_to_angle(target_angle=90*i)
    actual = robot.gyro.yaw_angle()
    print(f"Target: {90*i}°, Actual: {actual}°")
```

**Solution:**
- Recalibrate gyro
- Restart hub
- Adjust threshold

#### Problem: Timeout too early

**Diagnosis:**
```python
import time

start = time.ticks_ms()
robot.drive_distance(distance=100, mainspeed=600)
duration = time.ticks_diff(time.ticks_ms(), start)

print(f"Time needed: {duration}ms")
```

**Solution:**
- Increase timeout
- Increase speed
- Check distance

---

## Performance Checklist

### Before Each Competition

- [ ] Batteries fully charged (> 8.5V)
- [ ] Hub restarted
- [ ] Gyro calibrated (standing still)
- [ ] Color sensor calibrated
- [ ] Wheel circumference set correctly
- [ ] PID values tested
- [ ] Timeouts appropriate
- [ ] Test run successful

### During Competition

- [ ] Monitor global_turn_value
- [ ] On errors: reset gyro
- [ ] Watch battery warnings
- [ ] Check sensor position

---

## Advanced Techniques

### Adaptive PID

```python
def get_adaptive_pids(self, error, speed):
    """PID adapts to speed and error"""
    
    # Base PID
    P = 3.5
    I = 0.02
    D = 12.0
    
    # Adapt to speed
    if speed > 700:
        D *= 1.5  # More damping at high speed
    
    # Adapt to error
    if abs(error) < 5:
        P *= 1.2  # More reactive for small errors
        I *= 1.5  # More integral for fine-tuning
    
    return (P, I, D)
```

### Smart Re-Alignment

```python
def smart_re_align():
    """Re-align only when necessary"""
    current = robot.gyro.yaw_angle()
    target = robot.global_turn_value
    error = abs(current - target)
    
    if error > 2:  # Only for larger deviations
        robot.turn_to_angle(target_angle=target)
        print(f"Re-aligned: {error}° correction")
    else:
        print(f"No re-alignment needed ({error}°)")
```

### Odometry Tracking

```python
class PositionTracker:
    """Track position on field"""
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
    
    def update_position(self, distance):
        """Update after drive_distance"""
        import math
        rad = math.radians(self.angle)
        self.x += distance * math.cos(rad)
        self.y += distance * math.sin(rad)
    
    def update_angle(self, new_angle):
        """Update after turn_to_angle"""
        self.angle = new_angle
    
    def get_position(self):
        return (self.x, self.y, self.angle)

# Usage:
tracker = PositionTracker()

robot.drive_distance(distance=50, mainspeed=600)
tracker.update_position(50)

robot.turn_to_angle(target_angle=90)
tracker.update_angle(90)

print(f"Position: {tracker.get_position()}")
```

---

## See Also

- **[drive_distance()](Gyro-drive-distance-EN)** - Drive precise distances
- **[turn_to_angle()](Gyro-turn-to-angle-EN)** - Precise turns
- **[Sensor Functions](Gyro-Sensor-Functions-EN)** - Sensor-based navigation

---

[← Back: Sensor Functions](Gyro-Sensor-Functions-EN) | [🏠 Home](Home)
