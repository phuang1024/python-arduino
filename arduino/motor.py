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

from .core import ArduinoBoard, Clock


class Stepper:
    """
    Base stepper motor class.
    Extend from this to create a specific motor.

    This module has some pre-defined stepper classes.
    """

    spr: int
    """
    Steps per revolution.
    """

    _real_pos: int
    """
    Real position in steps.
    """

    def __init__(self, board: ArduinoBoard):
        """
        Initializes the motor.

        :param board: The board to use.
        """
        self.board = board
        self._real_pos = 0

    @property
    def pos(self) -> float:
        """
        The current position in degrees.
        """
        return self._real_pos / self.spr * 360

    def step(self, cw: bool, t: float):
        """
        Step the motor.
        Calls ``self._step(cw, t)``. Define in a subclass.

        :param cw: True if clockwise, False if counter-clockwise.
        :param t: Total step time.
        """
        self._step(cw, t)
        if cw:
            self._real_pos += 1
        else:
            self._real_pos -= 1

    def rotate(self, deg: float, rpm: float):
        """
        Rotate the motor.

        :param deg: The angle to rotate in degrees.
        :param rpm: Speed in revolutions per minute.
        """
        self.rotate_for(deg, deg/360 / rpm * 60)

    def rotate_for(self, deg: float, t: float):
        """
        Rotate ``deg`` for ``t`` seconds.
        """
        steps = int(abs(deg) / 360 * self.spr)
        step_time = t / steps
        cw = deg > 0

        for _ in range(steps):
            self.step(cw, step_time)

    def rotate_to(self, deg: float, rpm: float):
        """
        Rotate to ``deg`` at ``rpm`` rotations per minute.
        """
        self.rotate(deg - self.pos, rpm)

    def rotate_to_for(self, deg: float, t: float):
        """
        Rotate to ``deg`` for ``t`` seconds.
        """
        self.rotate_for(deg - self.pos, t)

    def _step(self, cw: bool, t: float):
        ...
