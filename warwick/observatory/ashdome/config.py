#
# This file is part of ashdomed.
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

"""Helper function to validate and parse the json config file"""

# pylint: disable=too-many-instance-attributes

import json
from warwick.observatory.common import daemons, IP, validation

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'daemon', 'log_name', 'control_machines', 'serial_port', 'serial_baud', 'serial_timeout',
        'latitude', 'longitude', 'altitude', 'steps_per_rotation', 'dome_radius_cm', 'telescope_offset_x_cm',
        'home_azimuth', 'tracking_max_separation', 'idle_loop_delay', 'moving_loop_delay',
        'azimuth_move_timeout', 'shutter_move_timeout'
    ],
    'properties': {
        'daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'log_name': {
            'type': 'string'
        },
        'control_machines': {
            'type': 'array',
            'items': {
                'type': 'string',
                'machine_name': True
            }
        },
        'serial_port': {
            'type': 'string'
        },
        'serial_baud': {
            'type': 'integer',
            'minimum': 0
        },
        'serial_timeout': {
            'type': 'number',
            'minimum': 0
        },
        'latitude': {
            'type': 'number',
            'minimum': -90,
            'maximum': 90
        },
        'longitude': {
            'type': 'number',
            'minimum': -180,
            'maximum': 180
        },
        'altitude': {
            'type': 'number',
            'minimum': 0
        },
        'steps_per_rotation': {
            'type': 'number',
            'minimum': 0
        },
        'dome_radius_cm': {
            'type': 'integer'
        },
        'telescope_offset_x_cm': {
            'type': 'integer',
            'minimum': -100,
            'maximum': 100
        },
        'home_azimuth': {
            'type': 'number',
            'minimum': 0
        },
        'tracking_max_separation': {
            'type': 'number',
            'minimum': 0
        },
        'idle_loop_delay': {
            'type': 'number',
            'min': 0
        },
        'moving_loop_delay': {
            'type': 'number',
            'min': 0
        },
        'azimuth_move_timeout': {
            'type': 'number',
            'min': 0
        },
        'shutter_move_timeout': {
            'type': 'number',
            'min': 0
        }
    }
}


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r', encoding='utf-8') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validation.validate_config(config_json, CONFIG_SCHEMA, {
            'daemon_name': validation.daemon_name_validator,
            'directory_path': validation.directory_path_validator,
        })

        self.daemon = getattr(daemons, config_json['daemon'])
        self.log_name = config_json['log_name']
        self.control_ips = [getattr(IP, machine) for machine in config_json['control_machines']]
        self.serial_port = config_json['serial_port']
        self.serial_baud = config_json['serial_baud']
        self.serial_timeout = config_json['serial_timeout']
        self.steps_per_rotation = config_json['steps_per_rotation']
        self.dome_radius_cm = config_json['dome_radius_cm']
        self.telescope_offset_x_cm = config_json['telescope_offset_x_cm']
        self.home_azimuth = config_json['home_azimuth']
        self.tracking_max_separation = config_json['tracking_max_separation']
        self.idle_loop_delay = int(config_json['idle_loop_delay'])
        self.moving_loop_delay = int(config_json['moving_loop_delay'])
        self.azimuth_move_timeout = int(config_json['azimuth_move_timeout'])
        self.shutter_move_timeout = int(config_json['shutter_move_timeout'])
        self.latitude = float(config_json['latitude'])
        self.longitude = float(config_json['longitude'])
        self.altitude = float(config_json['altitude'])
