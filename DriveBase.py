import hub # type: ignore
import motor  # type: ignore
import motor_pair  # type: ignore
import color_sensor  # type: ignore

import time
import math

from Logger import Logger

class DriveBase:
    """

    Every function we use to control our robot! \n
    Use this class as code to be added and used in every project. \n
    Alle Funktionen mit denen Wir unseren Roboter steuern! \n
    Diese Klasse in den Code hinzufügen und benutzen.

    """

    # CONSTANTS

    TYPEMOTOR = 0
    TYPECOLORSENS = 1

    TANKTURN = 0
    LEFTTURN = 1
    RIGHTTURN = 2
    
    PREGLER = False
    IREGLER = False
    DREGLER = False

    # CONFIGS

    MOTORR = 0
    MOTORL = 4
    ADDITION = 3
    ACTION = 5
    COLORSENS = 2

    MOTPAIR = 0

    WHEELCIRC = 17.6 / (24/8) # Übersetzung von 3 [Rad:Motor] 24:8

    def __init__(self, initial_yaw: int = 0):
        self.gyroSens = hub.motion_sensor
        self.stop = False

        self.global_turn_value = initial_yaw
        self.gyroSens.reset_yaw(initial_yaw * -10)

        motor_pair.pair(self.MOTPAIR, self.MOTORL, self.MOTORR)
        
    def configure_pid(
        self,
        p_regler: float = PREGLER,
        i_regler: float = IREGLER,
        d_regler: float = DREGLER
    ):
        """Configure PID Constants
        Configure PID Constants
        
        Konfiguriere PID Konstanten
        
        Parameters / Parameter
        -----------------

        #### p_regler: float = PREGLER
            The P-Constant
            Die P Konstante
        
        #### i_regler: float = IREGLER
            The I-Constant
            Die I Konstante
            
        #### d_regler: float = DREGLER
            The D-Constant
            Die D Konstante
        """
        
        self.PREGLER = p_regler
        self.IREGLER = i_regler
        self.DREGLER = d_regler

    def configure(
        self,
        motor_right_port: int = MOTORR,
        motor_left_port: int = MOTORL,
        addition_port: int = ADDITION,
        action_port: int = ACTION,
        color_sensor_port: int = COLORSENS,
        motor_pair_id: int = MOTPAIR,
        wheel_circumference: float = WHEELCIRC,
    ):
        """
        Configure DriveBase

        Konfiguriere DriveBase

        Parameters / Parameter
        -----------------

        #### motor_right_port: int = 0
            The port of the right motor. \n
            Der Port des rechten Motors.

        #### motor_left_port: int = 4
            The port of the left motor. \n
            Der Port des linken Motors.

        #### addition_port: int = 3
            The port of the addition motor. \n
            Der Port des Zusatzmotors.

        #### action_right_port: int = 5
            The port of the right action motor. \n
            Der Port des rechten Aktionsmotors.

        #### color_sensor_port: int = 2
            The port of the color sensor. \n
            Der Port von dem Farbsensor.

        #### motor_pair_id: int = 0
            The ID of the main motorpair. \n
            Die ID des Haupt Motorpaares.

        #### wheel_circumference: float = 17.6
            The circumference of the wheels. \n
            Der Umfang der Räder.
        """
        self.MOTORR = motor_right_port
        self.MOTORL = motor_left_port
        self.ADDITION = addition_port
        self.ACTION = action_port
        self.COLORSENS = color_sensor_port
        self.MOTPAIR = motor_pair_id
        self.WHEELCIRC = wheel_circumference

    #########################
    # Complex GyroFunctions #
    #########################

    def drive_distance(
        self,
        distance: float = 100,
        mainspeed: int = 600,
        stopspeed: int = 300,
        re_align: bool = True,
        isolated_drive: bool = False,
        stop: bool = True,
        *,
        brake_start: float = 0.7,
        timestep: int = 100,
        avoid_collision: bool = False,
        ) -> bool:
        """
        Drive a specific distance and correct unwanted changes with the gyrosensor.

        Fahre eine bestimmte Distanz und gleiche unbeabsichtigte Änderungen mit dem GyroSensor aus.

        Parameters / Parameter
        -----------------
        #### distance : int = 100
            The distance that the robot is supposed to drive. \n
            Die Distanz die der Roboter fahren soll.

        #### mainspeed: int = 600
            The maximum speed the robot reaches. \n
            Die maximale Geschwindigkeit, die der Roboter erreicht.

        #### stopspeed : float = 300
            The target speed while braking; the minimum speed at the end of the program. \n
            Die minimale Geschwindigkeit am Ende des Programms.
        
        #### re_align : bool = True
            If the robot should realign itself at the end of the driving to correct changes. \n
            Ob der Roboter sich neu ausrichten sollte, nachdem er gefahren ist, um Änderungen auszugleichen.

        #### isolated_drive : bool = False
            If the robot should drive independantly of the global turn_value. \n
            Ob der Roboter unabhängig von dem globalen Winkel fahren soll.
        
        #### stop : bool = True
            If the robot should stop at the end of the driven distance. \n
            Ob der Roboter am Ende der Distanz stoppen soll.

        ##### brake_start : int = 0.7
            Percentage of the driven distance after which the robot starts braking. \n
            Prozentsatz der zurückgelegten Strecke, nach der der Roboter mit dem Bremsen beginnt. \n
        ##### timestep : int = 100
            The timestep between every single calculation and correction to prevent to fast reactions. \n
            Der Zeitabstand zwischen jeder Berechnung und Ausgleichung, um zu schnelle Reaktionen zu verhindern. \n
        ##### avoid_collision : bool = False    ---> UNUSED
            If the robot should try to avoid every collision. \n
            Ob der Roboter versuchen sollte, Kollisionen auszuweichen.
        """
        motor.reset_relative_position(self.MOTORL, 0)
        motor.reset_relative_position(self.MOTORR, 0)
        mainspeed = -mainspeed
        stopspeed = -stopspeed

        def get_gyro_value() -> float:
            return -self.gyroSens.tilt_angles()[0] / 10

        def get_driven():
            return (
                abs(motor.relative_position(self.MOTORL))
                + abs(motor.relative_position(self.MOTORR))
            ) / 2
            
        def error() -> int:
            return int(get_gyro_value() - start_value)
                
        start_value = get_gyro_value() if isolated_drive else self.global_turn_value

        # Set starting speed of robot
        speed = mainspeed
        # Sets PID values

        old_change = 0
        integral = 0
        steering_sum = 0

        invert = 1

        # Sets values based on user inputs
        loop = True

        # Calulation of degrees the motors should turn to
        # 17.6 is wheel circumference in cm. You might need to adapt it
        rotate_distance = (distance / self.WHEELCIRC) * 360
        deccelerate_distance = rotate_distance * (1 - brake_start)

        # Inversion of target rotation value for negative values
        if speed < 0:
            invert = -1

        # Calculation of braking point
        brake_start_value = brake_start * rotate_distance
        driven_distance = get_driven()


        while loop:
            steering_sum += error()
            integral += error() - old_change
            # Calculation of driven distance and PID values
            old_driven_distance = driven_distance
            driven_distance = get_driven()
            
            p_regler, i_regler, d_regler = self.get_pids(speed)
            # yaw angle used due to orientation of the hub
            curren_steering = (
                error() * p_regler
                + integral * i_regler
                + d_regler * (error() - old_change)
            )
            
            old_change = error()

            curren_steering = max(-100, min(curren_steering, 100))

            # Calculation of speed based on acceleration and braking, calculation of steering value for robot to drive perfectly straight
            if distance <= 0:
                speed = mainspeed
            else:
                speed = self.speed_calculation(
                    speed,
                    deccelerate_distance,
                    brake_start_value,
                    int(driven_distance),
                    int(old_driven_distance),
                    mainspeed=mainspeed,
                    stopspeed=stopspeed,
                )
                braking = True if driven_distance > brake_start_value else False
                curren_steering = 0 if braking else curren_steering

            motor_pair.move(
                self.MOTPAIR, invert * -int(curren_steering), velocity=int(speed)
            )

            if distance <= 0:
                if self.stop:
                    loop = False
                    motor_pair.stop(self.MOTPAIR)
                    self.stop = False
            elif rotate_distance < driven_distance and stop:
                loop = False
                motor_pair.stop(self.MOTPAIR)
            elif rotate_distance < driven_distance:
                loop = False
            time.sleep(0.1)
        if re_align:
            # Removed isolated turn because not needed
            self.turn_to_angle(self.global_turn_value)
        time.sleep_ms(timestep)
        return True

    def turn_to_angle(
        self,
        target_angle: float = 90,
        turn_type: int = TANKTURN,
        minspeed: int = 60,
        maxspeed: int = 500,
        isolated_turn: bool = False,
        smart_stop: bool = True,
        *,
        pGain: float = 5,
        iGain: float = 0,
        dGain: float = 0.4,
        powerExp: float = 6,
        tolerance: float = 0.5,
        timestep: int = 10
        ):
        """
        Turn to a specific angle and correct overturning with the gyrosensor.

        Drehe den Roboter auf einen bestimmten Winkel und korrigiere Überdrehen mit dem GyroSensor.

        Parameters / Parameter:
        -----------------------

        #### target_angle : float = 90
            The angle the robot should turn to. \n
            Der Winkel auf die sich der Roboter drehen soll.
        
        #### turn_type : int = DriveBase.TANKTURN
            The type of how the robot should turn. \n
            Wie der Roboter sich drehen soll. \n
                -> TANKTURN Turn both wheels / Drehe um beide Räder \n
                -> LEFTTURN Turn over the left wheel / Drehe über das linke Rad \n
                -> RIGHTTURN Turn over the right wheel / Drehe über das rechte Rad

        #### minspeed : int = 60
            The minimal speed, which the robot never falls below. \n
            Die minimale Geschwindigkeit, welche der Roboter niemals unterschreitet.
        
        #### maxspeed : int = 500
            The maximum speed, which the robot never exceeds. \n
            Die maximale Geschwindigkeit, welche der Roboter niemals überschreitet.

        #### isolated_turn : bool = False
            If the robot should turn independently of the global turn_value. \n
            Ob der Roboter sich unabhängig von dem globalen Winkle drehen soll.
        
        #### smart_stop : bool = True
            If the robot should stop at the end. \n
            Ob der Roboter am Ende stoppen soll.

        ##### pGain : float = 5
            The proporional gain of the pid-turn. \n
            Die Proportionale von dem PID-Turn. \n
        ##### iGain : float = 0
            The integral gain of the pid-turn. \n
            Die Integral von dem PID-Turn. \n
        ##### dGain : float = 0.4
            The derivative gain of the pid-turn. \n
            Die Derivative von dem PID-Turn. \n
        ##### power_exp : float = 6
            The power gain. \n
            Die Verstärkung der Leistung. \n
        ##### tolerance : float = 0.5
            The tolerance of the output value. \n
            Die Toleranz beim Output. \n
        ##### timestep : int = 10
            The timestep between every single calculation and correction to prevent to fast reactions. \n
            Der Zeitabstand zwischen jeder Berechnung und Ausgleichung, um zu schnelle Reaktionen zu verhindern.
        """

        def get_gyro_value():
            return self.gyroSens.tilt_angles()[0] / 10

        def error() -> float:
            raw_error = target_angle - get_gyro_value()
            if raw_error > 180:
                raw_error -= 360
            elif raw_error < -180:
                raw_error += 360
            return raw_error

        def calc_power():
            return (
                abs(motor.get_duty_cycle(self.MOTORL))
                + abs(motor.get_duty_cycle(self.MOTORR))
            ) / 2
            

        integral = 0
        power = 0
        prev_error = 0
        invert = 1

        if not isolated_turn:
            self.global_turn_value = target_angle

        while True:
            integral += error() * (timestep / 1000)
            derivative = (error() - prev_error) / (timestep / 1000)
            prev_error = error()
            power = calc_power()

            output = (pGain * error()) + (iGain * integral) + \
                (dGain * derivative) * (1 - (power / 10000) ** powerExp)
            if output < 0:
                invert = -1
            else:
                invert = 1
            output = int(max(minspeed, min(abs(output), maxspeed)))

            if abs(error()) <= tolerance:
                output = 0

            # Set motor speeds based on output
            if turn_type == self.TANKTURN:
                motor_pair.move(self.MOTPAIR, 100, velocity=invert * output)

            elif turn_type == self.LEFTTURN:
                motor.run(self.MOTORR, invert * -output)

            elif turn_type == self.RIGHTTURN:
                motor.run(self.MOTORL, invert * -output)

            # Stop when close to the target angle
            if abs(error()) <= tolerance and smart_stop:
                motor_pair.stop(self.MOTPAIR)
                time.sleep_ms(90)
                if abs(error()) <= tolerance:
                    Logger.debug(
                        "Successful Turn: {}/{} offset: {}".format(target_angle, -int(get_gyro_value()), error()))
                    break

            time.sleep_ms(timestep)
        motor_pair.stop(self.MOTPAIR)

    def turn_till_color(self, direction: int = 1, speed: int = 360, color_type: int = 0, color_gate: int = 700, timeout: int = -1):
        """

            direction (either -1 or 1 idk which is which, ig -1 is left and 1 is right)

        """

        self.auto_detect_device(self.TYPECOLORSENS)
        if timeout > 0:
            motor_pair.move_for_time(
                self.MOTPAIR, timeout, direction * 100, velocity=speed)
        else:
            motor_pair.move(self.MOTPAIR, direction * 100, velocity=speed)

        start_time = time.ticks_ms()

        while True:
            color_val = color_sensor.rgbi(self.COLORSENS)[color_type]

            if color_val <= color_gate:
                break
            elif (time.ticks_ms() - start_time) / 1000 > timeout:
                Logger.debug((time.ticks_ms() - start_time) / 1000)
                break
            else:
                time.sleep_ms(50)
        motor.stop(self.MOTPAIR)

    def turn_till_reflect(self, direction: int = 1, speed: int = 360, reflection_gate: int = 700, smaller_than: int = True, timeout: int = -1):
        """

            direction (either -1 or 1 idk which is which, ig -1 is left and 1 is right)

        """

        self.auto_detect_device(self.TYPECOLORSENS)
        motor_pair.move(self.MOTPAIR, direction * 100, velocity=speed)

        start_time = time.ticks_ms()

        while True:
            reflection_val = color_sensor.reflection(self.COLORSENS)

            if smaller_than and reflection_val <= reflection_gate:
                break
            elif not smaller_than and reflection_val >= reflection_gate:
                break
            elif (time.ticks_ms() - start_time) / 1000 > timeout:
                Logger.debug((time.ticks_ms() - start_time) / 1000)
                break
            else:
                time.sleep_ms(50)
        print("Finish")
        motor.stop(self.MOTPAIR)

    def till_collide(self, speed, gate: int = 300, timeout: int = -1) -> float:
        def cycl() -> float:
            return (
                abs(motor.get_duty_cycle(self.MOTORL))
                + abs(motor.get_duty_cycle(self.MOTORR))
            ) / 2

        def get_driven() -> float:
            return (
                abs(motor.relative_position(self.MOTORL))
                + abs(motor.relative_position(self.MOTORR))
            ) / 2
        start_dist = get_driven()

        motor_pair.move(self.MOTPAIR, 0, velocity=speed)
        time.sleep(0.5)
        start_cycl = cycl()
        start_time = time.ticks_ms()
        while True:
            if self.collided(cycl(), start_cycl, gate):
                print(cycl())
                break
            elif (time.ticks_ms() - start_time) / 1000 > timeout and timeout > 0:
                Logger.debug(
                    abs(time.ticks_diff(start_time, time.ticks_ms)) / 1000)
                break
            else:
                time.sleep_ms(50)
        motor_pair.stop(self.MOTPAIR)

        distance = ((get_driven() - start_dist) * self.WHEELCIRC) / 360
        return distance

    def till_color(self, speed: int, color_type: int = 0, color_gate: int = 700, timeout: int = -1):
        self.auto_detect_device(self.TYPECOLORSENS)
        # if timeout > 0:
        #     motor_pair.move_for_time(self.MOTPAIR, timeout, 0, velocity = speed)
        # else:
        motor_pair.move(self.MOTPAIR, 0, velocity=speed)

        start_time = time.ticks_ms()

        loop = True

        while loop:
            color_val = color_sensor.rgbi(self.COLORSENS)[color_type]

            if color_val <= color_gate:
                loop = False
                break
            elif (time.ticks_ms() - start_time) / 1000 > timeout:
                loop = False
                break
            else:
                time.sleep_ms(50)
            if not loop:
                print("IDK what happens")
        print("Finish")
        motor.stop(self.MOTPAIR)

    def around_kollision(self, timestamp, power, old_power, steering, speed):
        # Logger.debug((timestamp, power, old_power))
        motor_pair.move(self.MOTPAIR, steering, velocity=speed)

    #######################
    # Simple Interactions #
    #######################

    def run_motor_duration(
        self, 
        speed: int = 500, 
        duration: float = 5, 
        *ports: int
        ) -> bool:
        """Run the given Motor

        Start the given ports for a specified time duration.
        If the duration is <= 0 do not stop.

        Starte die gegebenen ports für eine angegebene Zeit.
        Wenn die Zeit <= 0 ist, stoppt der Motor nicht.

        Parameters / Parameter
        -----------------

        #### speed: int = 500
            How fast the motor should turn. \n
            Wie schnell sich der Motor drehen soll. \n
        #### duration: float = 5
            How long the motor should run, if <= 0 no stopping. \n
            Wie lange der Motor sich drehen soll, wenn <= 0 stoppt er nicht. \n
        #### ports: int
            The ports which will be controlled, needs to be specified, otherwise throws Error. \n
            Die Ports die gesteuert werden sollen, muss angegeben sein, sonst kommt ein Fehler. \n
        """
        if len(ports) == 0:
            Logger.exception(40, "Please give ports")
            return False
        ports_list = list(ports)

        try:
            for port in ports_list:
                motor.run(port, speed)
            if duration > 0:
                time.sleep(duration)
                for port in ports_list:
                    motor.stop(port, stop=motor.SMART_COAST)
            return True
        except:
            Logger.exception(
                421, "Given unavailable port {}".format(str(ports)))
            return False

    def run_motor_degree(
        self, 
        speed: int = 500, 
        degree: float = 90, 
        *ports: int, 
        tolerance: float = 5
        ) -> bool:
        """Run the given Motor

        Start the given ports for a specified angle.

        Starte die gegebenen ports für einen angegebenen Winkel.

        Parameters / Parameter
        -----------------
        #### speed: int = 500 [degree/second]
            How fast the motor should turn. \n
            Wie schnell sich der Motor drehen soll. \n
        #### angle: float = 5 [degree]
            How much the motor should turn. \n
            Wie viel sich der Motor drehen soll. \n
        #### ports: int
            The ports which will be controlled, needs to be specified, otherwise throws Error. \n
            Die Ports die gesteuert werden sollen, muss angegeben sein, sonst kommt ein Fehler. \n
        ##### tolerance: float = 5
            The tolerance the motor checks for between the given and measured angle. \n
            Die Toleranz der Motor überprüft zwischen dem gegebenen und gemessenen Winkel. \n
        """

        def reached() -> bool:
            if abs(current_pos - target_pos) <= tolerance:
                return True
            else:
                return False

        try:
            if degree > 0:
                invert = 1
            else:
                invert = -1

            ports_list = [port for port in ports]
            if len(ports) == 0:
                Logger.exception(40, "Please give ports")
                return False

            target_pos = degree

            for port in ports_list:
                start_pos = motor.relative_position(
                    port)  # Startposition speichern
                motor.run(port, invert * speed)  # Motor starten
                # Zielposition berechnen
                target_pos = start_pos + degree

            while True:
                for port in ports_list:
                    current_pos = motor.relative_position(port)
                    if reached():
                        ports_list.remove(port)
                        motor.stop(port, stop=motor.SMART_COAST)
                if len(ports_list) == 0:
                    break
            return True
        except Exception as e:
            Logger.exception(
                421, "Error with motor port(s) {}: {}".format(str(ports), e)
            )
            return False

    def run_action_duration(self, speed: int = 360, duration: float = 5) -> bool:
        """Run the action/ability motor for time.

        Run the action motor with given speed, for the given time.

        Drehe den Motor mit dem gegebenen Speed, die gegebene Zeit.

        Parameters / Parameter
        --------------

        #### speed: float = 700 [degree/second]
            The given speed, with which the motor turns. \n
            Der gegebene Speed mit dem der Motor sich dreht. \n
        #### time: float = 5 [seconds]
            The given time, for which the motor should turn. \n
            Die gegebene Zeit, die sich der Motor drehen soll.
        """
        return self.run_motor_duration(speed, duration, self.ACTION)

    def run_action_degree(self, speed: int = 700, degree: float = 90) -> bool:
        """Run the action/ability motor for degree

        Run the action motor until it has turned the given degree. (not a turn to-, but a turn for-action)

        Drehe den Motor mit gegebener Geschwindigkeit bis er sich um den gegebenen Winkel dreht. (Kein drehen bis auf Position, aber ein drehen um Grad)

        Parameters / Parameter
        --------------

        #### speed: int = 700 [degree / second]
            The given speed, with which the motor turns. \n
            Der gegebene Speed mit dem der Motor sich dreht. \n
        #### degree: float = 90 [degree]
            The given angle, for which the motor should turn. \n
            Den gegebenen Winkel, um die sich der Motor drehen soll.
        """
        return self.run_motor_degree(speed, degree, self.ACTION)

    def run_to_absolute_position(
        self, position: int = 0, speed: int = 500, *ports: int
    ) -> bool:
        """Run motor(s) to given absolute position

        Run the given motors to the position, waits until position is reached

        Drehe die Motoren auf die Position, wartet bis die Position erreicht ist

        Parameters / Parameter
        ------------

        position: int = 0 [degree]
            Where the robot should turn to. \n
            Auf welchen Wert sich der Roboter drehen soll. \n
        speed: int = 500 [degree / second]
            With which speed the robot should turn. \n
            Mit welcher Geschwindigkeit der Roboter sich drehen soll. \n
        ports: tuple[int, ...]
            Which port should be used. \n
            Welche Ports angesteuert werden sollen.

        """

        def reached(port: int) -> bool:
            """
            Return whether the distance is reached
            """
            pos = (motor.absolute_position(port) + 360) % 360
            # print(pos, position)
            if position < 0 and pos <= position:
                motor.stop(port)
                return True
            elif position > 0 and pos >= position:
                motor.stop(port)
                return True
            elif position == 0 and abs(pos) >= 340:
                motor.stop(port)
                return True
            else:
                return False

        def invert(port: int) -> int:
            """
            Return whether the speed should be inverted for this port
            """
            current_pos = self.convert_abs(motor.absolute_position(port))
            if (position - current_pos) > 0:
                Logger.debug(-1)
                return -1
            else:
                Logger.debug(1)
                return 1

        ports_list = [port for port in ports]
        if len(ports) == 0:
            Logger.exception(40, "Please give ports")
            return False
        try:
            for port in ports_list:
                motor.run(port, invert(port) * speed)
        except Exception as e:
            Logger.exception(
                12, "run to absolute position had following error: {}".format(
                    e)
            )
            return False
        while True:
            for port in ports_list:
                pos = (motor.absolute_position(port) + 360) % 360
                if position < 0 and pos <= position:
                    motor.stop(port)
                    ports_list.remove(port)
                elif position > 0 and pos >= position:
                    motor.stop(port)
                    ports_list.remove(port)
                elif position == 0 and pos in range(position, position + 5):
                    print(
                        "finish {}".format(
                            (motor.absolute_position(port) + 360) % 360)
                    )
                    motor.stop(port)
                    print(
                        "finish {}".format(
                            (motor.absolute_position(port) + 360) % 360)
                    )
                    ports_list.remove(port)
            if len(ports_list) == 0:
                break
        return True

    def run_to_relative_position(
        self, position: int = 0, speed: int = 500, *ports: int
    ) -> bool:
        """Run motor(s) to given relative position

        Run the given motors to the position, waits until position is reached

        Drehe die Motoren auf die Position, wartet bis die Position erreicht ist

        Parameters / Parameter
        ------------

        position: int = 0 [degree]
            Where the robot should turn to. \n
            Auf welchen Wert sich der Roboter drehen soll. \n
        speed: int = 500 [degree / second]
            With which speed the robot should turn. \n
            Mit welcher Geschwindigkeit der Roboter sich drehen soll. \n
        ports: tuple[int, ...]
            Which port should be used. \n
            Welche Ports angesteuert werden sollen.

        """

        def reached() -> bool:
            """
            Return whether the distance is reached
            """
            if position > 0 and current_pos >= position:
                return True
            elif position < 0 and current_pos <= position:
                return True
            else:
                return False

        def invert(port) -> int:
            """
            Return whether the speed should be inverted for this port
            """
            current_pos = motor.relative_position(port)
            if (position - current_pos) > 0:
                return -1
            else:
                return 1

        ports_list = [port for port in ports]
        if len(ports) == 0:
            Logger.exception(40, "Please give ports")
            return False
        try:
            for port in ports_list:
                motor.run(port, invert(port) * speed)
                pass
        except Exception as e:
            Logger.exception(
                12, "run to relative position had following error: {}".format(
                    e)
            )
            return False
        while True:
            for port in ports_list:
                current_pos = motor.relative_position(port)
                if reached():
                    ports_list.remove(port)
                    motor.stop(port, stop=motor.SMART_COAST)
            if len(ports_list) == 0:
                break
        return True

    def attach_addition(self, attach: bool = True) -> bool:
        """Attach/Detach the addition.

        Attach or detach the addition of the robot.

        Befestige oder Löse Aufsatz vom Roboter.

        Parameters/Parameter
        --------
        attach: bool
            In which state the addition should be set. \n
            In welchen Zustand der Aufsatz gesetzt werden soll.
        """
        old_state = self.get_addition_state()
        if attach and not old_state:
            motor.run_to_absolute_position(
                3, 95, 1000, direction=motor.SHORTEST_PATH)
            return True
        elif not attach and old_state:
            motor.run_to_absolute_position(
                3, 0, 1000, direction=motor.SHORTEST_PATH)
            return True
        else:
            return False

    def reset_null(self, *ports: int):
        """Reset given motor to zero

        Reset the position of a given motor to absolute position zero.

        Setze die Position von einem gegebenen Motor auf die absolute Position Null.

        Parameters
        ------

        ports: tuple[int]
        """
        for port in ports:
            motor.reset_relative_position(port, 0)
            while True:
                current_pos = motor.relative_position(port)
                if abs(current_pos) == 0:
                    break

    def stop_motor(self, *ports) -> bool:
        """Stop given motor

        Stop the motor(s) with given port(s)

        ports: tuple[int]
        """
        try:
            for port in ports:
                motor.stop(port)
            return True
        except OSError:
            Logger.exception(
                621, "Given unavailable port(s) {}".format(str(ports)))
            return False

    #########################
    # Calculating Functions #
    #########################

    def auto_detect_device(self, device_type: int) -> list[int]:
        devices = []
        for i in range(6):
            try:
                if device_type == self.TYPEMOTOR:
                    motor.relative_position(i)
                elif device_type == self.TYPECOLORSENS:
                    color_sensor.rgbi(i)
                else:
                    Logger.exception(
                        404, "Please specify a correct device_type: 0/1")
                    continue
            except:
                continue
            devices.append(i)
        if device_type == self.TYPECOLORSENS:
            self.COLORSENS = devices[0]
        return devices

    def detect_all_devices(self) -> dict[int, str]:
        """Detect all connected devices on all ports

        Scan all ports and identify which type of device is connected to each port.

        Scanne alle Ports und identifiziere, welche Art von Gerät an jedem Port angeschlossen ist.

        Returns / Ausgabe
        -----
        dict[int, str]
            A dictionary mapping port numbers to device types ('motor', 'color_sensor', or 'none'). \n
            Ein Dictionary, das Portnummern zu Gerätetypen zuordnet ('motor', 'color_sensor' oder 'none').
        """
        devices = {}
        for port in range(6):
            device_type = 'none'
            
            # Check for motor
            try:
                motor.relative_position(port)
                device_type = 'motor'
            except:
                pass
            
            # Check for color sensor
            if device_type == 'none':
                try:
                    color_sensor.rgbi(port)
                    device_type = 'color_sensor'
                except:
                    pass
            
            devices[port] = device_type
        
        Logger.debug("Device scan: {}".format(devices))
        return devices

    def get_addition_state(self) -> bool:
        """
        Return the state of the addition. \n
        Gib den Zustand des Aufsatzes aus.

        Returns / Ausgabe:
        ----------
        True: abs_pos == 80 - 100
            Addition is connected. \n
            Aufsatz ist verbunden. \n
        False: abs_pos == -10 - 10 or 170 - 190
            Addition is not connected. \n
            Aufsatz ist gelöst.
        """
        if motor.absolute_position(3) in range(80, 100, 1):
            self.addition_state = True
            return True
        elif motor.absolute_position(3) in range(-10, 10, 1):
            self.addition_state = False
            return False
        elif motor.absolute_position(3) in range(170, 190, 1):
            return False
        else:
            motor.run_to_absolute_position(
                3, 0, 1000, direction=motor.SHORTEST_PATH)
            Logger.debug(
                "State {}° inbetweeen, open completely".format(
                    motor.absolute_position(3)
                )
            )
            self.addition_state = False
            return False

    def speed_calculation(
        self,
        speed: int,
        deccelerate_distance: float,
        brake_start_value: float,
        driven: int,
        old_driven: int,
        mode: int = 0,
        rotate_mode: int = 0,
        mainspeed: int = 300,
        stopspeed: int = 300,
    ):
        """Calculating the speed depending on all given parameters

        Used to calculate all the speeds in our programs.
        Executed separately to reduce redundancy.

        Wird verwendet, um alle Geschwindigkeiten in unseren Programmen zu berechnen.
        Wird separat ausgeführt, um Redundanz zu reduzieren.

        Parameters / Parameter
        ----------------------
        #### speed : int
            The current speed of the robot. \n
            Die aktuelle Geschwindigkeit des Roboters. \n
        #### deccelerate_distance: float
            The distance at which the robot starts to deccelerate. \n
            Die Distanz, ab welcher der Roboter anfängt zu bremsen. \n
        #### brakeStartValue : float
            Percentage of the driven distance after which the robot starts braking. \n
            Prozentsatz der zurückgelegten Strecke, nach dem der Roboter mit dem Bremsen beginnt. \n
        #### driven : int
            Distance the robot has currently traveled. \n
            Strecke, die der Roboter aktuell zurückgelegt hat. \n
        #### old_driven : int
            Distance the robot traveled during the last function call. \n
            Strecke, die der Roboter beim letzten Aufruf zurückgelegt hat. \n
        #### mode : int = 0
            The mode the robot operates in: turn[0] or drive[1]. \n
            Der Modus, in dem der Roboter arbeitet: turn[0] oder drive[1]. \n
        #### rotate_mode : int = 0
            The turning mode: normal_turn[0] or tank_turn[1]. \n
            Der Drehmodus: normal_turn[0] oder tank_turn[1]. \n
        #### mainspeed : int = 300
            The maximum speed the robot reaches. \n
            Die maximale Geschwindigkeit, die der Roboter erreicht. \n
        #### stopspeed : int = 300
            The target speed while braking; the minimum speed at the end of the program. \n
            Die Zielgeschwindigkeit beim Bremsen; die minimale Geschwindigkeit am Ende des Programms. \n
        """

        if rotate_mode == 1:
            if mainspeed in range(-300, 300):
                return mainspeed
            else:
                return int(math.copysign(1, mainspeed)) * 300

        if mode == 0:
            deccelerate_distance = max(deccelerate_distance, 1)
            sub_speed_per_degree = (
                mainspeed - stopspeed) / deccelerate_distance

            subtraction = (
                abs(driven) - abs(old_driven)
                if abs(driven) - abs(old_driven) >= 1
                else 1
            ) * sub_speed_per_degree

            if abs(driven) > abs(brake_start_value):

                if abs(speed) > abs(stopspeed):
                    speed = int(speed - subtraction)

            return speed
        else:
            deccelerate_distance = max(deccelerate_distance, 1)
            sub_speed_per_degree = (
                mainspeed - stopspeed) / deccelerate_distance

            subtraction = (
                abs(driven) - abs(old_driven)
                if abs(driven) - abs(old_driven) >= 1
                else 1
            ) * sub_speed_per_degree

            if abs(driven) > abs(brake_start_value):
                if abs(speed) > abs(stopspeed):
                    speed = int(speed - subtraction)
            return speed

    def get_pids(self, speed: float) -> tuple[float, float, float]:
        """Calculation of PID Values.

        Return the PID Values depending on the given speed. \n
        Gib die PID-Werte aus, abhängig davon, wie schnell der Roboter fährt

        Returns / Ausgabe
        -----
        (pRegler, iRegler, dRegler=1)

        """

        speed = abs(speed)

        def pRegler():
            return (
                14.59
                - 0.177132762 * speed
                + 0.000920045989 * speed**2
                - 2.34879006e-6 * speed**3
                + 3.15365919e-9 * speed**4
                - 2.15176282e-12 * speed**5
                + 5.90277778e-16 * speed**6
            )

        def iRegler():
            return (
                4.30433333
                - 0.0374442063 * speed
                + 0.00018870942 * speed**2
                - 5.52917468e-7 * speed**3
                + 8.790625e-10 * speed**4
                - 6.96201923e-13 * speed**5
                + 2.14583333e-16 * speed**6
            )

        if not self.PREGLER:
            p_regler = pRegler()
        else:
            p_regler = self.PREGLER
            
        if not self.IREGLER:
            i_regler = iRegler()
        else:
            i_regler = self.IREGLER
            
        if not self.DREGLER:
            d_regler = 1
        else:
            d_regler = self.DREGLER
        

        return (p_regler, i_regler, d_regler)

    def collided(self, cycl, start_cycl, gate: int = 300):
        diff = cycl - start_cycl
        if diff > gate:
            return True
        else:
            return False

    def convert_abs(self, abs_pos: int = 0) -> int:
        return (abs_pos + 360) % 360