#
# This file is part of ashdomed
#
# ashdomed is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ashdomed is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ashdomed.  If not, see <http://www.gnu.org/licenses/>.

"""Constants and status codes used by ashdomed"""

from warwick.observatory.common import TFmt


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

    _formats = {
        0: TFmt.Red + TFmt.Bold,
        1: TFmt.Red + TFmt.Bold,
        2: TFmt.Bold,
        3: TFmt.Yellow + TFmt.Bold,
        4: TFmt.Yellow + TFmt.Bold
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._formats and status in cls._formats:
                return cls._formats[status] + cls._labels[status] + TFmt.Clear
            return TFmt.Red + TFmt.Bold + 'UNKNOWN' + TFmt.Clear

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

    _formats = {
        0: TFmt.Red + TFmt.Bold,
        1: TFmt.Red + TFmt.Bold,
        2: TFmt.Green + TFmt.Bold,
        3: TFmt.Cyan + TFmt.Bold,
        4: TFmt.Yellow + TFmt.Bold,
        5: TFmt.Yellow + TFmt.Bold,
        6: TFmt.Red + TFmt.Bold,
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._formats and status in cls._formats:
                return cls._formats[status] + cls._labels[status] + TFmt.Clear
            return TFmt.Red + TFmt.Bold + 'UNKNOWN' + TFmt.Clear

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

    _formats = {
        0: TFmt.Bold,
        1: TFmt.Green + TFmt.Bold,
        2: TFmt.Red + TFmt.Bold,
        3: TFmt.Red + TFmt.Bold
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._formats and status in cls._formats:
                return cls._formats[status] + cls._labels[status] + TFmt.Clear
            return TFmt.Red + TFmt.Bold + 'UNKNOWN' + TFmt.Clear

        if status in cls._labels:
            return cls._labels[status]
        return 'UNKNOWN'
