## Ash Dome daemon

`ashdomed` communicates with the MDrive motors attached via RS422 adaptor. Control is exposed via Pyro.

`dome` is a commandline utility that interfaces with the dome daemon.

`python3-warwick-observatory-ashdome` is a python module with the common dome code.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the software architecture and instructions for developing and deploying the code.

### Configuration

Configuration is read from json files that are installed by default to `/etc/domed`.
A configuration file is specified when launching the dome server, and the `dome` frontend will search this location when launched.

```python
{
  "daemon": "warwick_dome", # Run the server as this daemon. Daemon types are registered in `warwick.observatory.common.daemons`.
  "log_name": "warwick_dome", # The name to use when writing messages to the observatory log.
  "control_machines": ["WarwickDome", "WarwickTCS"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `warwick.observatory.common.IP`.
  "serial_port": "/dev/dome", # Serial FIFO for communicating with the dome motors.
  "serial_baud": 9600, # Serial baud rate (always 9600).
  "serial_timeout": 3, # Serial communication timeout.
  "latitude": 52.376861, # Site latitude in degrees.
  "longitude": -1.583861, # Site longitude in degrees.
  "altitude": 94, # Site altitude in metres.
  "steps_per_rotation": 21947454, # Number of motor steps in a full rotation. Calibrate using measure_steps_per_rotation.py.
  "home_azimuth": 110, # The angle relative to north of the dome slit at the home position.
  "tracking_max_separation": 5, # The maximum allowed difference between the telescope and dome azimuth when tracking a target.
  "idle_loop_delay": 10, # Status refresh rate in seconds when the dome is not moving.
  "moving_loop_delay": 1, # Status refresh rate in seconds when the dome azimuth or shutter is moving.
  "azimuth_move_timeout": 180, # Maximum movement time between any two azimuth positions (including homing).
  "shutter_move_timeout": 180 # Maximum movement time to fully open or clsoe the shutter.
}
```

### Initial Installation

To install and configure on a Raspberry Pi running Raspberry Pi OS 11 (bullseye)
1. Set static IP by editing `/etc/dhcpcd.conf` to contain:
   ```
   interface eth0
   static ip_address=172.19.0.161
   static routers=172.19.0.129
   static domain_name_servers=137.205.205.80 137.205.205.100 137.205.205.129
   ```
   
   If the static IP changes it must also be updated in [`warwick-observatory-common`](https://github.com/warwick-one-metre/warwick-observatory-common).
2. Install dependencies:
   ```
   sudo apt install git python3-astropy python3-jsonschema python3-pyro4 python3-serial
   ```
3. Clone and install the [`warwick-observatory-common`](https://github.com/warwick-one-metre/warwick-observatory-common) python package:
   ```
   git clone https://github.com/warwick-one-metre/warwick-observatory-common
   cd warwick-observatory-common
   sudo make install
   ```
4. Clone `ashdomed` and install:
   ```
   git clone https://github.com/warwick-one-metre/ashdomed
   cd ashdomed
   sudo make install
   ```
6. Enable the systemd service:
   ```
   sudo systemctl enable --now ashdomed@warwick
   ```

### Testing Locally

The dome server and client can be run directly from a git clone:
```
./ashdomed warwick.json
DOMED_CONFIG_PATH=./warwick.json ./dome status
```
