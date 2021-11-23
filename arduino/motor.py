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

from pyfirmata import Board
from .core import Clock


class Stepper:
    """
    Base stepper motor class.
    Extend from this to create a specific motor.
    """

    clock: Clock
    """
    Motor's clock.
    Set at init so no overhead for creating the object.
    """

    spr: int
    """
    Steps per revolution.
    """

    _real_pos: int
    """
    Real position in steps.
    """

    def __init__(self, board: Board, spr: int):
        """
        Initializes the motor. You may take additional arguments in the subclass.
        Call super().__init__(board, spr) in the subclass.

        :param board: The board to use.
        :param spr: Steps per revolution.
        """
        self.clock = Clock()
        self._real_pos = 0

        self.board = board
        self.spr = spr

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
        self.rotate_for(deg, abs(deg)/360 / rpm * 60)

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
        """
        Define in subclass.
        """
        raise NotImplementedError("Define Stepper._step in a subclass.")


class Stepper_DirPul(Stepper):
    """
    Stepper motor with direction and pulse pins.
    Pulse pul e.g. switch between 0 and 1 to rotate.
    """

    dir_pin: int
    pul_pin: int

    def __init__(self, board: Board, spr: int, dir_pin: int, pul_pin: int):
        """
        Initializes the motor.

        :param board: The board to use.
        :param spr: Steps per revolution.
        :param dir_pin: Pin for direction.
        :param pul_pin: Pin for pulse.
        """
        super().__init__(board, spr)

        self.dir_pin = dir_pin
        self.pul_pin = pul_pin

    def _step(self, cw: bool, t: float):
        pause = t / 2
        self.clock.reset()

        self.board.digital[self.dir_pin].write(cw)

        self.board.digital[self.pul_pin].write(1)
        self.clock.tick(pause)
        self.board.digital[self.pul_pin].write(0)
        self.clock.tick(pause)
