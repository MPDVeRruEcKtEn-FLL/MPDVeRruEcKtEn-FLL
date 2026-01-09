# Calculations

[← Back: Motor Interactions](Simple-Motor-Interactions-EN) | [🏠 Home](Home) | [Next: Gyro Functions →](Gyro-Functions-EN)

---

This section contains all functions for calculating/outputting specific information.

---

## DriveBase.get_addition_state()  

Checks the position of the additional motor and indicates whether the attachment is attached or detached.  

### Return Value

- **True**: If `abs_pos between 80° and 100°`  
  > The attachment is firmly connected/locked.  

- **False**: If `abs_pos between -10° and 10°` or `between 170° and 190°`  
  > The attachment is detached/unlocked.

### Example
```python
if robot.get_addition_state():
    print("Attachment is attached")
else:
    print("Attachment is detached")
```

---

## DriveBase.speed_calculation()  

Calculates the optimal speed with automatic acceleration and deceleration.  
Used internally for smooth speed profiles.  

### Parameters  

- **speed** (type: int)  
  > The currently driven speed of the robot.  

- **decelerate_distance** (type: float)  
  > The distance in cm where braking begins.  

- **brake_start_value** (type: float)  
  > Percentage value (0.0-1.0) when braking starts. E.g., 0.7 = at 70% of distance.  

- **driven** (type: int)  
  > The distance currently traveled by the robot in degrees (motor rotations).  

- **old_driven** (type: int)  
  > The distance at the last function call to calculate acceleration.  

- **mode** (type: int; default: 0)  
  > Driving mode: **0** = rotation (turn), **1** = forward drive (drive).  

- **rotate_mode** (type: int; default: 0)  
  > Rotation mode: **0** = normal rotation, **1** = tank rotation (both wheels counter-rotating).  

- **mainspeed** (type: int; default: 300)  
  > The maximum target speed during travel.  

- **stopspeed** (type: int; default: 300)  
  > The minimum speed at the end (prevents abrupt stopping).

> ⚠️ **Note:** This function is normally used internally.

---

## DriveBase.get_pids()  

Calculates optimal PID parameters (Proportional, Integral, Derivative) based on driving speed.  
Higher speeds require different PID values for stable control.  

### Return Value

- **tuple[float, float, float]**  
  > The optimized PID values as a tuple: `(P-controller, I-controller, D-controller)`  
  > Example: `(5.0, 0.1, 1.0)` means P=5.0, I=0.1, D=1.0

### Example
```python
p, i, d = robot.get_pids()
print(f"PID values: P={p}, I={i}, D={d}")
```

---

## DriveBase.auto_detect_device()  

Scans all ports (A-F) and automatically finds connected devices of a specific type.  
Useful for dynamic hardware detection or finding sensors.  

### Parameters  

- **device_type** (type: int)  
  > The device type to search for:  
  > - **TYPEMOTOR (0)**: Finds all connected motors  
  > - **TYPECOLORSENS (1)**: Finds all connected color sensors  

### Return Value

- **list[int]**  
  > A list of all port numbers (0-5) where the searched device was found.  
  > Example: `[0, 4]` means devices on ports A and E.  
  > Empty list `[]` if no device was found.  

### Example
```python
# Find all motors
motors = robot.auto_detect_device(robot.TYPEMOTOR)
print(f"Motors found on ports: {motors}")

# Find color sensors
sensors = robot.auto_detect_device(robot.TYPECOLORSENS)
print(f"Color sensors found on ports: {sensors}")
```

---

## DriveBase.collided()  

Checks if a collision was detected by comparing motor load (duty cycle).  
Used by `till_collide()`.  

### Parameters  

- **cycl** (type: float)  
  > The current duty cycle value (motor load in percent, typically 0-10000).  

- **start_cycl** (type: float)  
  > The duty cycle value at the start of travel as reference.  

- **gate** (type: int; default: 300)  
  > The threshold value for load change. Collision detected when exceeded.  
  > Example: `gate=300` means ≥300% load increase = collision.  

### Return Value

- **bool**  
  > **True**: Collision detected (load difference > gate)  
  > **False**: No collision (normal travel)  

---

## DriveBase.convert_abs()  

Normalizes any angle value to the standardized range of 0-360 degrees.  
Useful for angle calculations that go beyond 360° or below 0°.  

### Parameters  

- **abs_pos** (type: int; default: 0) [degrees]  
  > The absolute position to convert (can also be negative or >360°).  
  > Examples: -45° → 315°, 450° → 90°, 720° → 0°  

### Return Value

- **int** [degrees]  
  > The normalized angle in the range 0-360 degrees.  
  > The value is always ≥0 and <360.  

### Example
```python
angle = robot.convert_abs(-45)  # Result: 315
print(f"Normalized angle: {angle}°")
```

---

## DriveBase.around_kollision()  

**[INTERNAL HELPER FUNCTION]**  
Helper function for collision avoidance during travel.  
Called internally by other functions. **Do not use directly!**  

### Parameters  

- **timestamp** (type: int) [milliseconds]  
  > The current timestamp for time-based calculations.  

- **power** (type: float)  
  > The current motor power (duty cycle).  

- **old_power** (type: float)  
  > The motor power from the previous iteration for comparison.  

- **steering** (type: int)  
  > The current steering value (-100 to +100).  

- **speed** (type: int) [degrees/second]  
  > The driving speed of the robot.  

---

[← Back: Motor Interactions](Simple-Motor-Interactions-EN) | [🏠 Home](Home) | [Next: Gyro Functions →](Gyro-Functions-EN)
