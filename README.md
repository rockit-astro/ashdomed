## Ash Dome daemon

`ashdomed` communicates with the MDrive motors attached via RS422 adaptor. Control is exposed via Pyro.

`dome` is a commandline utility that interfaces with the dome daemon.

`python3-rockit-ashdome` is a python module with the common dome code.

### Configuration

Configuration is read from json files that are installed by default to `/etc/domed`.
A configuration file is specified when launching the dome server, and the `dome` frontend will search this location when launched.

```python
{
  "daemon": "warwick_dome", # Run the server as this daemon. Daemon types are registered in `rockit.common.daemons`.
  "log_name": "warwick_dome", # The name to use when writing messages to the observatory log.
  "control_machines": ["WarwickDome", "WarwickTCS"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `rockit.common.IP`.
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

`ashdomed` requires the MDrive communications parameters to be changed from the default and saved to NVRAM for both axes:

 * `BD=48`
 * `CK=2`
 * `EM=1`


### Testing Locally

The dome server and client can be run directly from a git clone:
```
./ashdomed warwick.json
DOMED_CONFIG_PATH=./warwick.json ./dome status
```
