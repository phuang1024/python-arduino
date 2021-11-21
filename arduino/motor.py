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

    def __init__(self, board: ArduinoBoard):
        """
        Initializes the motor.

        :param board: The board to use.
        """
        self.board = board
        self.pos = 0  # Position in revolutions

    def step(self, cw: bool):
        """
        Step the motor. Define in subclasses.

        :param cw: True if clockwise, False if counter-clockwise.
        """
        ...
