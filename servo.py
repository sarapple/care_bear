import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, servo_pin_nums):
        self.all_pins = Servo._get_all_pins(servo_pin_nums)

    @staticmethod
    def _servo_pin_setup(servo_pin_num, duty_cycle_start):
        """
            Setup the PWM pin to be used by the servo
            Servos want 50 Hz frequency output
        """
        GPIO.setup(servo_pin_num, GPIO.OUT)
        rpio_pin = GPIO.PWM(servo_pin_num, 50)
        rpio_pin.start(duty_cycle_start)

        return rpio_pin

    @staticmethod
    def _compute_duty_cycle(angle):
        """
            From the desired angle for the servo, compute the duty cycle needed to be used for PWM
        """
        if (angle > 180):
            angle = 180
        elif (angle < 0):
            angle = 0

        angle_scaled = angle / 180

        duty_cycle = 2.5 + (10 * angle_scaled)
        
        return duty_cycle

    @staticmethod
    def _get_all_pins(servo_pin_nums):
        """
            Convert pin numbers to RPi pin instances
            in addition to the original duty cycle we are starting from 0 degrees
        """
        DUTY_CYCLE_START = Servo._compute_duty_cycle(0)
        GPIO.setmode(GPIO.BCM)

        all_pins = [
            (
                Servo._servo_pin_setup( # Rpio pin instance
                    servo_pin_num,
                    DUTY_CYCLE_START
                ),
                DUTY_CYCLE_START, # Current duty cycle (angle)
            )
            for servo_pin_num in servo_pin_nums
        ]

        return all_pins

    @staticmethod
    def _turn_servo_to_angle(target_servo, target_angle, wait_time):
        """
            Take a servo and turn it to a desired angle
            TODO: Make the delay for how long to wait based on the initial angle
        """
        duty_cycle = Servo._compute_duty_cycle(target_angle)

        target_servo.ChangeDutyCycle(duty_cycle)
        time.sleep(wait_time)

    @staticmethod
    def _cleanup(all_pins):
        """Cleanup the GPIO pins and servos for the next process that uses them"""
        for (target_servo, _origin_duty_cycle) in all_pins:
            target_servo.stop()

        GPIO.cleanup()

    def turn_servo_to_angle(self, servo_pin_index, target_angle, wait_time):
        """
            Provide the servo index (based on list given to the constructor) you want to turn.
            Turn it to a desired target angle
            Provide the wait_time to allow for the transition to take place.
        """
        if servo_pin_index >= len(self.all_pins):
            print("not here")
            return

        (target_servo, _origin_duty_cycle) = self.all_pins[servo_pin_index]
        Servo._turn_servo_to_angle(target_servo, target_angle, wait_time)

    def cleanup(self):
        """Cleanup should be called when done with the servos"""
        Servo._cleanup(self.all_pins)

def run():
    servo = Servo([12, 18])
    left_hand_index = 0
    right_hand_index = 1

    for angle in range(0, 180, 10):
        servo.turn_servo_to_angle(left_hand_index, angle, 1)
    
    for angle in range(180, 0, -10):
        servo.turn_servo_to_angle(right_hand_index, angle, 1)
    
    servo.cleanup()

if __name__ == '__main__':
    run()
