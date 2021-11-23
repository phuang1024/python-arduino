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
from .motor import Stepper


def stepper_max_speed(motor: Stepper, base_spd: float, inc_spd: float, angle: float = 180,
        margin: float = 0.05, verbose: bool = True) -> float:
    """
    Calculate the maximum speed for a stepper motor.

    :param motor: Stepper motor object.
    :param base_spd: Base speed. Testing starts at this speed.
    :param inc_spd: Speed increment. Speed is incremented by this amount.
    :param angle: Angle to move each test.
    :param margin: If time difference exceeds this, max speed reached.
    :return: Maximum speed.
    """
    if verbose:
        print("Stepper motor max speed test:")

    s = time.time()
    motor.rotate(angle, base_spd)
    base_time = time.time() - s

    spd = base_spd
    while True:
        print(f"  Testing speed {spd}: ", end="")

        s = time.time()
        motor.rotate(angle, spd)
        elapse = time.time() - s

        expected = base_time / spd * base_spd
        diff = abs(elapse - expected)

        print(f"{elapse:.2f}s, expected {expected:.2f}s, diff {diff:.2f}s")

        if diff > margin:
            break

        spd += inc_spd

    return spd
