import serial
from threading import Timer

class StopTimer:
    def __init__(self, stop_callback, delay=0.25):
        self.delay=delay
        self.timer=None
        self.stop_callback=stop_callback

    def reset(self):
        if self.timer is not None:
            self.timer.cancel()

        self.timer = Timer(self.delay, self.stop_callback)
        self.timer.start()

class Tracks:

    # max_speed and min_speed should range from 1 to 63
    def __init__(self, max_speed=55, min_speed=10):
        self.motor_port = serial.Serial('/dev/ttyTHS1', 9600)
        self.stopTimer = StopTimer(self.stop)

        # This value was extracted from experiments.
        # 0.5 input speed is close to 50cm/second
        self.speed_factor = 74

        # Experimental to have 1 turn speed equal about 60 degrees/second
        self.turn_factor = 14

        self.max_speed=min(max_speed, 63)
        self.min_speed=max(1, min_speed)

    def _map_value_speed(self, value):
        return int(self.speed_factor * value)

    def _map_value_turn(self, value):
        return int(self.turn_factor * value)

    def stop(self):
        self.motor_port.write([64, 192])

    def _get_real_speed(self, speed):
        mapped_value = self._map_value_speed(speed)
        return min(max(abs(mapped_value), self.min_speed), self.max_speed)

    def _get_real_turn(self, speed):
        mapped_value = self._map_value_turn(speed)
        return min(max(abs(mapped_value), self.min_speed), self.max_speed)

    def go_forward(self, speed=0.4):
        out = self._get_real_speed(speed)
        self.motor_port.write([64 + out, 192 + out])
        self.stopTimer.reset()

    def go_backward(self, speed=0.4):
        out = self._get_real_speed(speed)
        self.motor_port.write([64 - out, 192 - out])
        self.stopTimer.reset()

    def go_left(self, speed=0.3):
        out = self._get_real_turn(speed)
        self.motor_port.write([64 + out, 192 - out])
        self.stopTimer.reset()

    def go_right(self, speed=0.3):
        out = self._get_real_turn(speed)
        self.motor_port.write([64 - out, 192 + out])
        self.stopTimer.reset()
