/*
 * This file is part of the Robotic Observatory Control Kit (rockit)
 *
 * rockit is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * rockit is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with rockit.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "btstack_event.h"
#include "pico/cyw43_arch.h"
#include "pico/stdlib.h"
#include "btstack.h"

#define TCS_PICO_ADDR "\x28\xCD\xC1\x13\xCA\x7E"
#define RELAY_PIN 6
#define RFCOMM_SERVER_CHANNEL 1
#define HEARTBEAT_PERIOD_MS 1000
#define CLOSE_LENGTH_MS 180000

static uint8_t heartbeat = 0;

// Indicated whether the actively triggered and force-closing dome
static bool active = false;

// Sticky status for whether the heartbeat has triggered
// New heartbeat pings will be ignored if this is true
static bool triggered = false;

static btstack_timer_source_t heartbeat_timer;
static btstack_timer_source_t close_timer;

static uint8_t spp_service_buffer[150];
static uint16_t rfcomm_cid = 0;

static void close_timer_cb(struct btstack_timer_source *ts)
{
    gpio_put(RELAY_PIN, 0);
    active = false;
}

static void heartbeat_timer_cb(struct btstack_timer_source *ts)
{
    if (heartbeat != 0xFF && heartbeat != 0)
    {
        if (--heartbeat == 0)
        {
            triggered = true;
            active = true;
            gpio_put(RELAY_PIN, 1);

            btstack_run_loop_set_timer(&close_timer, CLOSE_LENGTH_MS);
            btstack_run_loop_add_timer(&close_timer);
        }
    }

    if (rfcomm_cid)
        rfcomm_request_can_send_now_event(rfcomm_cid);

    btstack_run_loop_set_timer(ts, HEARTBEAT_PERIOD_MS);
    btstack_run_loop_add_timer(ts);
}

static void packet_handler(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size)
{
	switch (packet_type)
    {
		case HCI_EVENT_PACKET:
        {
			switch (hci_event_packet_get_type(packet))
            {
                case RFCOMM_EVENT_INCOMING_CONNECTION:
                {
                    bd_addr_t addr;
                    rfcomm_event_incoming_connection_get_bd_addr(packet, addr);
                    uint16_t cid = rfcomm_event_incoming_connection_get_rfcomm_cid(packet);

                    if (!memcmp(addr, TCS_PICO_ADDR, 6))
                        rfcomm_accept_connection(cid);
                    else
                        rfcomm_decline_connection(cid);

					break;
				}

				case RFCOMM_EVENT_CHANNEL_OPENED:
                {
                    uint8_t status = rfcomm_event_channel_opened_get_status(packet);
                    if (status == 0)
                    {
                        rfcomm_cid = rfcomm_event_channel_opened_get_rfcomm_cid(packet);
                        gap_discoverable_control(0);
                        gap_connectable_control(0);
                    }

					break;
                }

                case RFCOMM_EVENT_CAN_SEND_NOW:
                {
                    uint8_t data = active ? 254 : triggered ? 255 : heartbeat;
                    rfcomm_send(rfcomm_cid, &data, 1);

                    break;
                }

                case RFCOMM_EVENT_CHANNEL_CLOSED:
                {
                    rfcomm_cid = 0;

                    gap_discoverable_control(1);
                    gap_connectable_control(1);
                    break;
                }
			}

            break;
        }

        case RFCOMM_DATA_PACKET:
        {
            for (uint16_t i = 0; i < size; i++)
            {
                if (packet[i] > 240)
                    continue;

                // Clear the sticky trigger flag when disabling the heartbeat
                // Also stops an active close
                if (packet[i] == 0)
                {
                    triggered = false;
                    active = false;

                    gpio_put(RELAY_PIN, 0);
                }

                // Update the heartbeat countdown (disabling it if 0)
                // If the heatbeat has triggered the status must be manually
                // cleared by sending a 0 byte
                if (!triggered)
                    heartbeat = packet[i];
            }

            break;
        }
	}
}

int main()
{
    stdio_init_all();
    cyw43_arch_init();

    gpio_init(RELAY_PIN);
    gpio_set_dir(RELAY_PIN, GPIO_OUT);
    gpio_put(RELAY_PIN, 0);

    close_timer.process = &close_timer_cb;
    heartbeat_timer.process = &heartbeat_timer_cb;
    btstack_run_loop_set_timer(&heartbeat_timer, HEARTBEAT_PERIOD_MS);
    btstack_run_loop_add_timer(&heartbeat_timer);

    l2cap_init();
    rfcomm_init();
    rfcomm_register_service(packet_handler, RFCOMM_SERVER_CHANNEL, 0xffff);

    sdp_init();
    memset(spp_service_buffer, 0, sizeof(spp_service_buffer));
    spp_create_sdp_record(spp_service_buffer, sdp_create_service_record_handle(), RFCOMM_SERVER_CHANNEL, "TMO Dome Heartbeat Controller");
    btstack_assert(de_get_len(spp_service_buffer) <= sizeof(spp_service_buffer));
    sdp_register_service(spp_service_buffer);

    gap_ssp_set_io_capability(SSP_IO_CAPABILITY_DISPLAY_YES_NO);
    gap_set_local_name("TMO Dome Heartbeat Controller");
    gap_set_class_of_device(0); // Miscellaneous
    gap_discoverable_control(1);

	hci_power_control(HCI_POWER_ON);

    btstack_run_loop_execute();
}