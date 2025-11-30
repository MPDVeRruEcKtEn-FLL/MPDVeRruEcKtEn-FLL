# Simple Motor Interactions

[← Back: Configuration](Configuration-EN) | [🏠 Home](Home) | [Next: Calculations →](Calculations-EN)

---

This section explains the simple functions for controlling motors.

---

## DriveBase.run_motor_duration()  

Starts one or more motors for a specific duration.  
If time ≤ 0, the motor runs continuously until manually stopped.  

### Parameters  

- **speed** (type: int; default: 500) [degrees/second]
  > The rotation speed of the motor. Positive values = forward, negative values = backward.  

- **duration** (type: float; default: 5) [seconds]
  > The runtime of the motor. If ≤ 0, the motor runs indefinitely.  

- **ports** (type: int) **[REQUIRED]**  
  > The port number(s) of the motors to control. Must be specified.  

### Example
```python
# Motor on port 3 for 2 seconds at 300°/s
robot.run_motor_duration(speed=300, duration=2, ports=3)
```

---

## DriveBase.run_motor_degree()  

Rotates one or more motors by a specific angle and waits until the position is reached.  

### Parameters  

- **speed** (type: int; default: 500) [degrees/second]
  > The rotation speed of the motor. Higher values = faster, but less precise.  

- **degree** (type: float; default: 90) [degrees]
  > The rotation angle relative to the current position. Positive = one direction, negative = opposite.

- **ports** (type: int) **[REQUIRED]**  
  > The port number(s) of the motors to control. Must be specified.  

- **tolerance** (type: float; default: 5) [degrees]  
  > The allowed deviation between target and actual position. Smaller values = more precise, but slower.  

### Example
```python
# Rotate motor 180° with high precision
robot.run_motor_degree(speed=400, degree=180, ports=5, tolerance=2)
```

---

## DriveBase.run_action_duration()  

Rotates the action motor (e.g., for gripper or tools) for a specific time.  

### Parameters  

- **speed** (type: float; default: 360) [degrees/second]  
  > The rotation speed of the action motor. Can be positive or negative.  

- **duration** (type: float; default: 5) [seconds]  
  > The runtime of the action motor. Stops automatically after expiration.  

### Example
```python
# Open gripper for 1.5 seconds
robot.run_action_duration(speed=500, duration=1.5)
```

---

## DriveBase.run_action_degree()  

Rotates the action motor by a relative angle (not to an absolute position).  
Example: If motor is at 45° and degree=90, it rotates to 135°.  

### Parameters  

- **speed** (type: int; default: 700) [degrees/second]  
  > The rotation speed of the action motor during movement.  

- **degree** (type: float; default: 90) [degrees]  
  > The relative rotation angle. Rotation occurs from the current position.  

### Example
```python
# Open flap by 120°
robot.run_action_degree(speed=600, degree=120)
```

---

## DriveBase.run_to_absolute_position()  

Rotates motors to an absolute position (not relative to current position).  
The position is the actual angle value of the motor encoder.  

### Parameters  

- **position** (type: int; default: 0) [degrees]  
  > The absolute target position of the motor (e.g., 0° = zero point, 360° = one full rotation).  

- **speed** (type: int; default: 500) [degrees/second]  
  > The speed of movement to the target position.  

- **ports** (type: tuple[int, ...])  
  > A tuple of port numbers to control, e.g., (0, 4) for both drive motors.

### Example
```python
# Both wheels to position 0 (zero point)
robot.run_to_absolute_position(position=0, speed=400, ports=(0, 4))
```

---

## DriveBase.run_to_relative_position()  

Rotates motors by a relative position from the current position.  
Example: Currently at 100°, position=50 → rotates to 150°.  

### Parameters  

- **position** (type: int; default: 0) [degrees]  
  > The relative rotation from the current position. Can be positive or negative.  

- **speed** (type: int; default: 500) [degrees/second]  
  > The speed of the relative movement.  

- **ports** (type: tuple[int, ...])  
  > A tuple of port numbers, e.g., (3,) for only the additional motor or (0, 4) for both wheels.

### Example
```python
# Additional motor rotate 90° further
robot.run_to_relative_position(position=90, speed=300, ports=(3,))
```

---

## DriveBase.attach_addition()  

Controls the additional motor to attach or detach an attachment from the robot.  
Useful for tools that are changed during the mission.  

### Parameters  

- **attach** (type: bool; default: True)  
  > **True**: Attach the attachment (motor rotates to attachment position).  
  > **False**: Detach the attachment (motor rotates to detachment position).

### Example
```python
# Attach attachment
robot.attach_addition(attach=True)

# Later: Detach attachment
robot.attach_addition(attach=False)
```

---

## DriveBase.reset_null()  

Resets the encoder position of one or more motors to zero.  
Useful for calibration or establishing a new reference point.  

### Parameters  

- **ports** (type: tuple[int])  
  > A tuple of port numbers whose position should be set to 0°, e.g., (0, 4).

### Example
```python
# Set both drive motors to 0
robot.reset_null(ports=(0, 4))
```

---

## DriveBase.stop_motor()  

Immediately stops one or more motors and holds them in the current position.  

### Parameters  

- **ports** (type: tuple[int])  
  > A tuple of port numbers to stop, e.g., (0,) or (0, 4, 5).

### Example
```python
# Stop all motors
robot.stop_motor(ports=(0, 3, 4, 5))
```

---

[← Back: Configuration](Configuration-EN) | [🏠 Home](Home) | [Next: Calculations →](Calculations-EN)
