Firmware for a pair of Raspberry Pi Pico W boards that engages the manual close switch on an Ash dome to force it closed if it does not receive a regular heartbeat ping from the connected control computer. Based on (and uses a slightly extended protocol from) the [dome heartbeat monitor](https://github.com/rockit-astro/dome-heartbeat-monitor) for Astrohaven domes.

The "dome" Pico is mounted in the shutter control box, attached to a [relay](https://cpc.farnell.com/sb-components/sku21277/single-channel-relay-hat-pi-pico/dp/SC19102) that is connected in parallel with the close switch. It is powered from the dome mains supply via a [5v power supply](https://cpc.farnell.com/mean-well/mdr-10-5/power-supply-ac-dc-5v-2a/dp/PW05422).

The "TCS" Pico does not require any additional hardware, and connects to the dome Pico via Bluetooth to forward heartbeat pings and report the status from the dome Pico.

The PC activates the monitor by sending a byte value between `1` (1 seconds) and `240` (240 seconds) to the TCS Pico via USB, and can disable the monitor by sending the byte value `0`.

The unit reports its status back to the PC via USB every second.  The status is either `0` (disabled), `252` (searching for dome Pico), `253` (connecting to dome Pico) `254` (actively closing dome), `255` (closed dome and now inactive), or the number of seconds left until the timer expires. The `255` state is sticky, and must be reset by sending `0` before the heartbeat timeout can be re-enabled.

When changing the Pico hardware, the bluetooth addresses in `tcs_pico.c` and `dome_pico.c` must be changed to match.