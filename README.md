# Voyanti Goodwe
Homeassistant Addon for Goodwe Inverters

[Homeassistant](https://www.home-assistant.io/) (HA) Add-on for Goodwe Inverters.

Communicates with Goodwe Inverters/Logger/Meters over Modbus TCP/ Serial, and publishes all available values to MQTT.

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/Voyanti/ha-modbus-addons)

**Features**

- Customisable read interval at which all registers are updated
- Supports using multiple Modbus TCP hubs, each connected to multiple Paneltrack meters

**Requires**

- MQTT broker e.g. [Mosquitto](https://github.com/home-assistant/addons/blob/master/mosquitto/DOCS.md)
- [Homeassistant MQTT integration](https://www.home-assistant.io/integrations/mqtt/) to enable discovering the MQTT devices and entities

**Tested with**

- Python 3.10
- Homeassistant version x
- Supervisor version x

Supported models:
- None

## Goodwe-specifics

When reading through the EzLogger3000:
- Registers containing ASCII should be read using the listed start offset but
num_registers or count == 0, not the number of registers to read - the device 
will respond with the appropriate amount of data
- When reading from both HT and GT type devices, wait a few seconds 
(tested=5s) between reads from separate modsbus ids.
- GT register 32072 (Grid Current A), 32066 (Grid Voltage AB): response length 
seems to vary
- When reading, the immediate response sometimes has a mismatching 
Transport Identifier. Reread, and the logger responds to the original query
- PV inverter switch off at nighttime ( logger responds with Modbus error code 
0x04: slave device failure)

<!-- ![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield] -->
