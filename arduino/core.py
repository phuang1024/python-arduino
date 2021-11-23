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


class Clock:
    """
    Clock based on absolute time rather than relative.
    Can tick at a constant rate.
    """

    def __init__(self, t: float = 0):
        """
        Initialize the clock.

        :param t: The time to start the clock at. Default 0.
        """
        self.start = time.time() - t
        self.last_tick = self.time()

    def reset(self, t: float = 0):
        """
        Reset time (or set to t).
        """
        self.start = time.time() - t
        self.last_tick = self.time()

    def time(self):
        """
        Return time since elapse.
        """
        return time.time() - self.start

    def waitto(self, t):
        """
        Sleep until time is t.
        """
        # Busy but doesn't overshoot
        while self.time() < t:
            continue

    def tick(self, t):
        """
        Wait until time is t + last_tick.
        """
        self.waitto(t + self.last_tick)
        self.last_tick = self.time()
