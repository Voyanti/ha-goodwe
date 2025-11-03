# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Home Assistant add-on for **GoodWe Inverters** that communicates over Modbus (TCP/RTU) and publishes data to MQTT for Home Assistant integration.

**Important**: This codebase was cloned from an Atess inverter add-on and is being adapted for GoodWe inverters. You will see many references to "Atess" throughout the code (e.g., `atess_inverter.py`, `atess_registers.py`, class names, etc.). This is intentional - the architecture and core components remain the same, but the register definitions and device-specific logic need to be updated for GoodWe compatibility.

The add-on reads inverter/battery data via Modbus at configurable intervals and publishes to MQTT topics that Home Assistant auto-discovers. It also supports writing parameters back to devices via MQTT commands.

**Modbus Documentation**: See `pdfs/Ezlogger3000C_MODBUS_Interface_Description (1).pdf` for GoodWe Modbus register specifications.

## Commands

### Local Development
```bash
# Run locally with test configuration and local MQTT broker
./run_locally.sh

# Run tests (starts local mosquitto, runs unittests)
./test.sh
```

### Testing
```bash
# Run all unit tests
export PYTHONPATH=src/
python3 -m unittest -v

# Run specific test
python3 -m unittest tests.test_app
```

### Entry Point
The add-on is started via `run.sh` which calls:
```bash
python3 -u -m src.app
```

## Architecture

### Core Components

**App (`src/app.py`)**
- Main application orchestrator
- Lifecycle: `setup()` → `connect()` → `loop()`
- Manages clients, servers, and MQTT connection
- Implements "midnight sleep" feature (sleeps 3 min before to 5 min after midnight)
- Uses dependency injection pattern with callbacks for client/server instantiation

**Client (`src/client.py`)**
- Wraps pymodbus `ModbusSerialClient` or `ModbusTcpClient`
- Handles Modbus read/write operations with retry logic on `ModbusIOException`
- Note: Modbus addresses are 1-indexed in this codebase but pymodbus expects 0-indexed (client automatically converts)
- `SpoofClient` class provides fake data for local testing

**Server (`src/server.py`)**
- Abstract base class representing a Modbus device (inverter/battery)
- Each server has: name, serial number, modbus_id, connected_client
- Key responsibilities:
  - Read model code and verify against supported models
  - Setup valid registers for specific model
  - Batch read registers (125 registers per batch by default)
  - Decode/encode register values using `_decoded()` and `_encoded()` abstract methods
  - Maintain internal state (`holding_state`, `input_state`) for efficient batch reading
- Batching: Reads all registers in batches, stores in internal state, then indexes specific parameters from state

**MqttClient (`src/modbus_mqtt.py`)**
- Extends `paho.mqtt.client.Client`
- Publishes Home Assistant MQTT discovery topics
- Handles bidirectional communication:
  - Publishes read parameter values to `{base_topic}/{server_name}/{register_slug}/state`
  - Subscribes to write commands at `{base_topic}/{server_name}/{register_slug}/set`
- Exception in `message_handler` callback kills the entire process (by design)
- Disconnection from broker triggers process termination

### Configuration

Configuration is loaded from `/data/options.json` (in Home Assistant) or `config.yaml` (local dev).

**Structure:**
- `servers`: List of Modbus devices with name, serialnum, server_type, connected_client, modbus_id
- `clients`: List of Modbus connections (TCP or RTU) with connection parameters
- MQTT settings: host, port, credentials, topics
- `pause_interval_seconds`: Interval between read cycles
- Midnight sleep settings

See `config.yaml` for example configuration and `src/options.py` for dataclass definitions.

### Register Definitions

Register maps are currently defined in `src/atess_registers.py` (inherited from Atess codebase):
- `atess_parameters`: Common read-only parameters
- `PCS_parameters`, `PBD_parameters`, `not_PCS_parameters`: Model-specific parameters
- `atess_write_parameters`, `atess_PBD_write_parameters`: Writable parameters

**Note**: These will need to be updated for GoodWe inverters based on the Modbus specification in `pdfs/`.

Each parameter includes: address, data type, multiplier, unit, device_class, Home Assistant entity type.

### Adding New Server Types

1. Create new server class inheriting from `Server` (see `src/atess_inverter.py` as example)
2. Implement abstract methods: `_decoded()`, `_encoded()`, `read_model()`, `setup_valid_registers_for_model()`
3. Define register maps (parameters and write_parameters)
4. Add to `ServerTypes` enum in `src/implemented_servers.py`
5. Use the enum value as `server_type` in configuration

### Data Flow

1. App initializes clients and servers from config
2. Clients connect to Modbus devices
3. Servers verify availability, read model, setup valid registers, create batches
4. MQTT client publishes discovery topics
5. Main loop:
   - For each server: `read_batches()` reads all registers into internal state
   - For each parameter: `read_from_state()` decodes value from state
   - Publish each value to MQTT
   - Sleep for `pause_interval_seconds`
   - Check for midnight sleep condition

### Error Handling

- Modbus read errors: Retry with 20s delay on `ModbusIOException`
- MQTT disconnection: Kills process (restarts via Home Assistant)
- Exception in MQTT message callback: Kills process
- Missing client/server references: Raises `ValueError`

## Development Notes

- Python 3.10 target (specified in Dockerfile)
- Type hints are used but mypy configuration is minimal (only sets `python_path`)
- Tests use `SpoofClient` for mocking Modbus responses
- Local testing requires mosquitto broker running on port 1884
- Serial numbers should be verified on connection (though currently commented out in some places)
- **Legacy code notes**:
  - This was cloned from Atess inverter add-on, so Atess references remain throughout
  - Tests reference Sungrow inverters (from an earlier generation)
  - When adapting for GoodWe, focus on register definitions and device-specific decoding/encoding logic

## Home Assistant Integration

- Add-on slug: `ha-atess`
- Docker image: `ghcr.io/voyanti/ha-atess`
- Requires MQTT broker and Home Assistant MQTT integration
- Auto-discovery uses standard HA MQTT discovery protocol
- Write parameters appear as number/select/switch entities based on `ha_entity_type`
