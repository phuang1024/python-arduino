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
from typing import Tuple
from .core import ArduinoBoard, Clock


class Stepper_28BYJ48:
    """
    Control a 28BYJ-48 stepper motor.
    """

    board: ArduinoBoard
    pins: Tuple[int, int, int, int]
    spr: int

    pos: float
    """
    Position in revolutions.
    """

    _rotate_keys = (
        "1100",
        "0110",
        "0011",
        "1001",
    )

    def __init__(self, board: ArduinoBoard, pins: Tuple[int, int, int, int], spr=512):
        """
        Initialize the motor controller.

        :param board: The Arduino board.
        :param pins: Indices of the digital pins that control the motor in
            left to right order (e.g. ``(8, 9, 10, 11)``)
        :param spr: Steps per rotation.
        """
        self.board = board
        self.pins = pins
        self.spr = spr

        self.pos = 0

    def write_pins(self, key: str):
        """
        Write values to each of the four pins.

        :param key: Length 4 string of ``"0"`` or ``"1"`` corresponding to
            the values of the four pins.
        """
        for i in range(4):
            self.board.write_digital(self.pins[i], int(key[i]))

    def step(self, cw: bool, pause: float = 0):
        """
        Rotate one step.

        :param cw: Whether to rotate clockwise.
        :param pause: Total seconds the step takes.
        """
        keys = reversed(self._rotate_keys) if cw else self._rotate_keys
        clock = Clock()
        for key in keys:
            self.write_pins(key)
            clock.tick(pause/4)

        if cw:
            self.pos += 1 / self.spr
        else:
            self.pos -= 1 / self.spr

    def steps(self, cw: bool, steps: int, total_time: float):
        """
        Rotate steps, taking a total of total_time.
        """
        step_time = total_time / steps
        clock = Clock()
        for _ in range(steps):
            self.step(cw, step_time * 0.9)  # 0.9 to avoid overshoot
            clock.tick(step_time)

    def rotate(self, rounds: float, speed: float):
        """
        Rotate the motor.

        :param rounds: Number of revolutions to rotate. Negative values for ccw.
        :param speed: RPM speed.
        """
        cw = rounds > 0
        rounds = abs(rounds)

        total_time = rounds / (speed/60)
        steps = int(rounds * self.spr)
        self.steps(cw, steps, total_time)

    def rotate_to(self, pos: float, speed: float):
        """
        Rotate to a position.

        :param pos: Position in revolutions.
        :param speed: RPM speed.
        """
        rounds = pos - self.pos
        self.rotate(rounds, speed)
