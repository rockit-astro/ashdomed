#!/usr/bin/env python3
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

import argparse
import time
import serial


def send_command(port, command, has_response=False, ignore_error=False):
    """
    Sends a motor control command and validates that it was processed correctly.
    Optionally returns the motor response if has_response is True.
    Throws exceptions on error.
    """
    if port.write(('\n' + command + '\n').encode('ascii')) != len(command) + 2:
        raise serial.SerialException('Failed to send command')

    echo = port.readline().decode('ascii').strip()
    if echo != command:
        cb = command.encode('ascii').hex()
        eb = echo.encode('ascii').hex()
        raise serial.SerialException(f'echo mismatch `{command}` != `{echo}`; {cb} != {eb}')

    if has_response:
        response = port.readline().decode('ascii').strip()
        # print(f'{command}: {response}')
    else:
        # print(f'{command}')
        response = None

    prompt = port.read(1).decode('ascii')
    if ignore_error and prompt == '?':
        send_command(port, f'{command[0]}ER 0')
    elif prompt != '>':
        raise serial.SerialException(f'prompt `{prompt}` is not `>`')

    return response


def wait_until_stationary(port):
    while True:
        response = send_command(port, 'APR MV', has_response=True)
        if response == '0':
            return
        time.sleep(5)


def run(path, baud, timeout):
    # Connect and reboot
    port = serial.Serial(path, baud, timeout=timeout)
    port.flushInput()
    port.flushOutput()
    if port.write(b'\x03') != 1:
        raise serial.SerialException('Failed to send reboot command')
    time.sleep(5)

    # Nudge away from the limit
    send_command(port, 'AMR 500000')
    wait_until_stationary(port)

    # Find home
    send_command(port, 'AHM 1')
    wait_until_stationary(port)
    send_command(port, 'AP=0')

    # Force a full rotation
    send_command(port, 'AHM 3')
    wait_until_stationary(port)

    # Run past the home switch
    send_command(port, 'AMR 500000')
    wait_until_stationary(port)

    # Return to home from the same direction we started
    send_command(port, 'AHM 1')
    wait_until_stationary(port)

    response = send_command(port, 'APR P', has_response=True)
    print(f'Steps per full rotation: {response}')

    port.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dome daemon')
    parser.add_argument('port')
    parser.add_argument('--baud', type=int, default=9600)
    parser.add_argument('--timeout', type=int, default=3)
    args = parser.parse_args()
    run(args.port, args.baud, args.timeout)
