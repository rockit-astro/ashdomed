#
# This file is part of the Robotic Observatory Control Kit (rockit)
#
# rockit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rockit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rockit.  If not, see <http://www.gnu.org/licenses/>.

"""Constants and status codes used by ashdomed"""


class CommandStatus:
    """Numeric return codes"""
    # General error codes
    Succeeded = 0
    Failed = 1
    Blocked = 2
    InvalidControlIP = 3

    NotConnected = 7
    NotDisconnected = 8
    NotHomed = 9

    HeartbeatTimedOut = 13
    HeartbeatCloseInProgress = 14
    HeartbeatInvalidTimeout = 16
    EngineeringModeRequiresHeartbeatDisabled = 17
    EngineeringModeActive = 18
    FollowModeActive = 19

    _messages = {
        # General error codes
        1: 'error: command failed',
        2: 'error: another command is already running',
        3: 'error: command not accepted from this IP',
        7: 'error: dome is not connected',
        8: 'error: dome is already connected',
        9: 'error: dome has not been homed',

        # dome specific codes
        13: 'error: heartbeat has tripped',
        14: 'error: heartbeat is closing the dome',
        16: 'error: heartbeat timeout must be less than 120s',
        17: 'error: heartbeat must be disabled before enabling engineering mode',
        18: 'error: dome is in engineering mode',
        19: 'error: dome azimuth is controlled by the telescope',

        -100: 'error: terminated by user',
        -101: 'error: unable to communicate with dome daemon'
    }

    @classmethod
    def message(cls, error_code):
        """Returns a human readable string describing an error code"""
        if error_code in cls._messages:
            return cls._messages[error_code]
        return f'error: Unknown error code {error_code}'


class AzimuthStatus:
    """Status of the dome rotation"""
    Disconnected, NotHomed, Idle, Moving, Homing = range(5)

    _labels = {
        0: 'DISCONNECTED',
        1: 'NOT HOMED',
        2: 'IDLE',
        3: 'MOVING',
        4: 'HOMING'
    }

    _colors = {
        0: 'red',
        1: 'red',
        2: 'default',
        3: 'yellow',
        4: 'yellow'
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._labels and status in cls._colors:
                return f'[b][{cls._colors[status]}]{cls._labels[status]}[/{cls._colors[status]}][/b]'
            return '[b][red]UNKNOWN[/red][/b]'

        if status in cls._labels:
            return cls._labels[status]
        return 'UNKNOWN'


class ShutterStatus:
    """Status of the dome shutter"""
    Disconnected, Closed, Open, PartiallyOpen, Opening, Closing, HeartbeatMonitorForceClosing = range(7)

    _labels = {
        0: 'DISCONNECTED',
        1: 'CLOSED',
        2: 'OPEN',
        3: 'PARTIALLY OPEN',
        4: 'OPENING',
        5: 'CLOSING',
        6: 'FORCE CLOSING',
    }

    _colors = {
        0: 'red',
        1: 'red',
        2: 'green',
        3: 'cyan',
        4: 'yellow',
        5: 'yellow',
        6: 'red',
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._labels and status in cls._colors:
                return f'[b][{cls._colors[status]}]{cls._labels[status]}[/{cls._colors[status]}][/b]'
            return '[b][red]UNKNOWN[/red][/b]'

        if status in cls._labels:
            return cls._labels[status]
        return 'UNKNOWN'


class HeartbeatStatus:
    """Status of the dome heartbeat monitoring"""
    Disabled, Active, TrippedClosing, TrippedIdle = range(4)

    _labels = {
        0: 'DISABLED',
        1: 'ACTIVE',
        2: 'CLOSING DOME',
        3: 'TRIPPED'
    }

    _colors = {
        0: 'default',
        1: 'green',
        2: 'red',
        3: 'red'
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._labels and status in cls._colors:
                return f'[b][{cls._colors[status]}]{cls._labels[status]}[/{cls._colors[status]}][/b]'
            return '[b][red]UNKNOWN[/red][/b]'

        if status in cls._labels:
            return cls._labels[status]
        return 'UNKNOWN'
