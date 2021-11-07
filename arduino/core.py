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

import pyfirmata


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
