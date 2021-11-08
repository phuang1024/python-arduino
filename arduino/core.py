#
#  Arduino
#  An API for controlling Arduino boards.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import time
import pyfirmata


class Clock:
    """
    Clock based on absolute time.
    Sleep is more precise than time.sleep()
    """

    def __init__(self, t=0):
        """
        Initialize the clock.

        :param t: The time to start the clock at. Default 0.
        """
        self.start = time.time() - t
        self.last_tick = self.time()

    def reset(self, t=0):
        """
        Reset time (or set to t).
        """
        self.start = time.time() - t

    def time(self):
        """
        Return time since elapse.
        """
        return time.time() - self.start

    def waitto(self, t):
        """
        Sleep until time is t.
        """
        while self.time() < t:
            time.sleep(0.0005)

    def tick(self, t):
        """
        Wait until time is t + last_tick.
        """
        self.waitto(t + self.last_tick)
        self.last_tick = self.time()


class ArduinoBoard:
    """
    Wrapper for ``pyfirmata.Arduino`` with type hinting and docs.
    """

    def __init__(self, path: str):
        """
        Initialize the board.

        :param path: Path to the Arduino board. See docs for more info.
        """
        self.board = pyfirmata.Arduino(path)

    def write_digital(self, pin: int, value: int):
        """
        Write a value to a digital pin.

        :param pin: Pin index.
        :param value: Value to write.
        """
        self.board.digital[pin].write(value)
