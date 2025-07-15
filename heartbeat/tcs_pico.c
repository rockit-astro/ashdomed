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

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include "pico/cyw43_arch.h"
#include "pico/stdlib.h"
#include "btstack.h"

#define DOME_PICO_ADDR "\x2C\xCF\x67\xD7\xE2\xC0"
#define SCAN_INTERVAL 5
#define STATUS_INTERVAL 1

typedef enum
{
    SCANNING,
    CONNECTING,
    CONNECTING_SDP,
    CONNECTING_RFCOMM,
    CONNECTED
} connection_state_t;

static uint8_t tx_data;
static uint8_t rx_data;

static btstack_packet_callback_registration_t event_cb_reg;
static btstack_context_callback_registration_t sdp_client_cb_reg;
static btstack_timer_source_t status_timer;

static connection_state_t connection_state;
static uint8_t rfcomm_channel;
static uint16_t rfcomm_cid;

static void status_timer_cb(struct btstack_timer_source *ts)
{
    // Status is forwarded from the Dome pico when we are connected
    if (connection_state == CONNECTED)
        putchar(rx_data);
    else
        putchar(connection_state == SCANNING ? 0xFC : 0xFD);

    btstack_run_loop_set_timer(ts, 1000 * STATUS_INTERVAL);
    btstack_run_loop_add_timer(ts);
}

static void event_cb(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size);

static void sdp_client_cb(void * context)
{
    if (connection_state != CONNECTING_SDP)
        return;

    connection_state = CONNECTING_RFCOMM;
    sdp_client_query_rfcomm_channel_and_name_for_uuid(&event_cb, DOME_PICO_ADDR, BLUETOOTH_SERVICE_CLASS_SERIAL_PORT);
}

static void event_cb(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size)
{
	switch (packet_type)
    {
		case HCI_EVENT_PACKET:
        {
			switch (hci_event_packet_get_type(packet))
            {
                case BTSTACK_EVENT_STATE:
                {
                    if (btstack_event_state_get_state(packet) != HCI_STATE_WORKING)
                        return;

                    // The connection logic is driven by events
                    // Start the process by searching for the dome pico
                    connection_state = SCANNING;
                    gap_inquiry_start(SCAN_INTERVAL);

                    break;
                }

                case SDP_EVENT_QUERY_RFCOMM_SERVICE:
                {
                    rfcomm_channel = sdp_event_query_rfcomm_service_get_rfcomm_channel(packet);

                    break;
                }

                case SDP_EVENT_QUERY_COMPLETE:
                {
                    if (!sdp_event_query_complete_get_status(packet))
                        rfcomm_create_channel(event_cb, DOME_PICO_ADDR, rfcomm_channel, NULL);
                    else
                    {
                        // Something went wrong... retry from the start
                        connection_state = SCANNING;
                        gap_inquiry_start(SCAN_INTERVAL);
                    }

                    break;
                }

                case GAP_EVENT_INQUIRY_RESULT:
                {
                    if (connection_state != SCANNING)
                        break;

                    bd_addr_t addr;
                    gap_event_inquiry_result_get_bd_addr(packet, addr);
                    if (!memcmp(addr, DOME_PICO_ADDR, 6))
                    {
                        gap_inquiry_stop();
                        connection_state = CONNECTING;
                    }

                    break;
                }

                case GAP_EVENT_INQUIRY_COMPLETE:
                {
                    switch (connection_state)
                    {
                        case SCANNING:
                        {
                            // Keep searching...
                            gap_inquiry_start(SCAN_INTERVAL);

                            break;
                        }

                        case CONNECTING:
                        {
                            connection_state = CONNECTING_SDP;
                            sdp_client_cb_reg.callback = &sdp_client_cb;
                            sdp_client_register_query_callback(&sdp_client_cb_reg);

                            break;
                        }
                    }

                    break;
                }

                case RFCOMM_EVENT_INCOMING_CONNECTION:
                {
                    if (connection_state != CONNECTING_RFCOMM)
                        return;

                    bd_addr_t addr;
                    rfcomm_event_incoming_connection_get_bd_addr(packet, addr);
                    uint16_t cid = rfcomm_event_incoming_connection_get_rfcomm_cid(packet);

                    if (!memcmp(addr, DOME_PICO_ADDR, 6))
                        rfcomm_accept_connection(cid);
                    else
                        rfcomm_decline_connection(cid);

					break;
				}

				case RFCOMM_EVENT_CHANNEL_OPENED:
                {
                    if (connection_state != CONNECTING_RFCOMM)
                        return;

					if (!rfcomm_event_channel_opened_get_status(packet))
                    {
                        rfcomm_cid = rfcomm_event_channel_opened_get_rfcomm_cid(packet);
                        connection_state = CONNECTED;
                    }
                    else
                    {
                        // Something went wrong... retry from the start
                        connection_state = SCANNING;
                        gap_inquiry_start(SCAN_INTERVAL);
                    }

					break;
                }

                case RFCOMM_EVENT_CAN_SEND_NOW:
                {
                    if (connection_state != CONNECTED)
                        return;

                    rfcomm_send(rfcomm_cid, &tx_data, 1);

                    break;
                }

                case RFCOMM_EVENT_CHANNEL_CLOSED:
                {
                    // Connection lost... retry from the start
                    connection_state = SCANNING;
                    gap_inquiry_start(SCAN_INTERVAL);

                    break;
                }
			}
            break;
        }

        case RFCOMM_DATA_PACKET:
        {
            rx_data = packet[size - 1];
            break;
        }
	}
}

void input_cb(char c)
{
    if (connection_state == CONNECTED)
    {
        tx_data = c;
        rfcomm_request_can_send_now_event(rfcomm_cid);        
    }
}

int main()
{
    stdio_init_all();
    cyw43_arch_init();

    status_timer.process = &status_timer_cb;
    btstack_run_loop_set_timer(&status_timer, STATUS_INTERVAL);
    btstack_run_loop_add_timer(&status_timer);
    btstack_stdin_setup(input_cb);

    event_cb_reg.callback = &event_cb;
    hci_add_event_handler(&event_cb_reg);

    l2cap_init();
    rfcomm_init();
    gap_discoverable_control(0);
    gap_connectable_control(0);
    gap_ssp_set_io_capability(SSP_IO_CAPABILITY_DISPLAY_YES_NO);
	hci_power_control(HCI_POWER_ON);

    btstack_run_loop_execute();
}
