from typing import final

from .enums import DataType, DeviceClass, HAEntityType, Parameter, RegisterTypes, WriteParameter
from .server import Server
import logging
logger = logging.getLogger(__name__)

write_params: dict[str, WriteParameter] = {
    # Register 55: Active power adjustment mode (RW)
    "Enable Active Power Control": WriteParameter(
        addr=20200+1, count=1, dtype=DataType.U16, multiplier=1/1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER,
        ha_entity_type=HAEntityType.SWITCH,
        payload_on=1,
        payload_off=0
    ),
    # Register 10: Active power adjustment (RW)
    "Active Power Adjustment": WriteParameter(
        addr=20013+1, count=2, dtype=DataType.U32, multiplier=1/10, unit="kW",
        device_class=DeviceClass.POWER,
        register_type=RegisterTypes.HOLDING_REGISTER,
        ha_entity_type=HAEntityType.NUMBER,
        min=0,
        max=500000,
    ),
    # Register 14: Set Active Power (percentage) (RW)
    "Set Active Power Percentage": WriteParameter(
        addr=20021+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="%",
        device_class=DeviceClass.POWER_FACTOR,
        register_type=RegisterTypes.HOLDING_REGISTER,
        ha_entity_type=HAEntityType.NUMBER,
        min=0, max=100,
    ),
}

goodwe_parameters: dict[str, Parameter] = {
    "System Time": Parameter(
        addr=20000+1, count=2, dtype=DataType.U32, multiplier=1/1, unit="",
        device_class=DeviceClass.TIMESTAMP,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Register 17: Total Active Power (RO)
    "Total Active Power": Parameter(
        addr=20025+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="kW",
        device_class=DeviceClass.POWER,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # Register 24: Plants Status (RO)
    "Grid status": Parameter(
        addr=20038+1, count=1, dtype=DataType.U16, multiplier=1/1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # Register 25: Total A-Phase current (RO)
    "Total A-Phase Current": Parameter(
        addr=20039+1, count=1, dtype=DataType.I16, multiplier=1/10, unit="A",
        device_class=DeviceClass.CURRENT,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # Register 26: Total B-Phase current (RO)
    "Total B-Phase Current": Parameter(
        addr=20040+1, count=1, dtype=DataType.I16, multiplier=1/10, unit="A",
        device_class=DeviceClass.CURRENT,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # Register 27: Total C-Phase current (RO)
    "Total C-Phase Current": Parameter(
        addr=20041+1, count=1, dtype=DataType.I16, multiplier=1/10, unit="A",
        device_class=DeviceClass.CURRENT,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # Register 28: Vab (RO)
    "Vab": Parameter(
        addr=20042+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # Register 29: Vbc (RO)
    "Vbc": Parameter(
        addr=20043+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # Register 30: Vca (RO)
    "Vca": Parameter(
        addr=20044+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # Register 35: Maximum value of active power regulation (RO)
    "Maximum Active Power Regulation": Parameter(
        addr=20060+1, count=2, dtype=DataType.U32, multiplier=1/1000, unit="kW",
        device_class=DeviceClass.POWER,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # Register 38: ESN - Electronic Serial Number (RO)
    "ESN": Parameter(
        addr=20064+1, count=8, dtype=DataType.UTF8, multiplier=1/1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # Register 41: Target value of power dispatch (RO)
    "Target Power Dispatch Read Only": Parameter(
        addr=20075+1, count=2, dtype=DataType.U32, multiplier=1/10, unit="kW",
        device_class=DeviceClass.POWER,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # Register 43: Percentage of active dispatch (RO)
    "Target Power Dispatch Percentage Read Only": Parameter(
        addr=20079+1, count=2, dtype=DataType.U32, multiplier=1/1, unit="%",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    
}


@final
class GoodweLogger(Server):
    def __init__(self, name, serial, modbus_id, connected_client):
        super().__init__(name, serial, modbus_id, connected_client)

        self._manufacturer = "Goodwe"
        self._supported_models = ('ezlogger',) 
        self._serialnum = "unknown"
        self._parameters = dict.copy(goodwe_parameters)
        self._write_parameters = dict.copy(write_params)

    @property
    def manufacturer(self):
        return self._manufacturer
    
    @property
    def write_parameters(self):
        return self._write_parameters
    
    @property
    def parameters(self):
        return self._parameters
    
    @property
    def supported_models(self):
        return self._supported_models
    
    def is_available(self, register_name="System Time"):
        # self.verify_serialnum()
        return super().is_available(register_name)
    
    def read_model(self) -> str:
        return "ezlogger"
    
    def verify_serialnum(self, serialnum_name_in_definition:str="Serial Number") -> bool:
        """ Verify that the serialnum specified in config.yaml matches 
        with the num in the regsiter as defined in implementation of Server

        Arguments:
        ----------
            - serialnum_name_in_definition: str: Name of the register in server.registers containing the serial number
        """
        logger.info("Verifying serialnumber")
        serialnum = self.read_registers(serialnum_name_in_definition)                                                

        if serialnum is None: 
            logger.info(f"Server with serial {self.serial} not available")
            return False
        elif self.serial != serialnum: raise ValueError(f"Mismatch in configured serialnum {self.serial} \
                                                                        and actual serialnum {serialnum} for server {self.name}.")
        return True
    
    def setup_valid_registers_for_model(self):
        # GoodWe EzLogger doesn't have model-specific registers
        # All registers are available for all EzLogger models
        return

    @staticmethod
    def _decoded(registers, dtype):
        """
        Decode registers read from GoodWe EzLogger.

        GoodWe uses big-endian encoding per MODBUS-TCP standard (Section 3.2.3 of PDF):
        "MODBUS uses a 'big-Endian' to represent addresses and data items."

        Parameters:
        -----------
        registers: list of ints as read from 16-bit ModBus Registers
        dtype: DataType enum (U16, I16, U32, I32, U64, I64, UTF8)
        """
        import struct

        def _decode_u16(registers):
            """Unsigned 16-bit integer"""
            return registers[0]

        def _decode_i16(registers):
            """Signed 16-bit integer"""
            return struct.unpack('>h', struct.pack('>H', registers[0]))[0]

        def _decode_u32(registers):
            """
            Unsigned 32-bit integer from 2 registers.
            Big-endian: first register is high word, second is low word.
            """
            high = registers[0]
            low = registers[1]
            packed = struct.pack('>HH', high, low)
            return struct.unpack('>I', packed)[0]

        def _decode_i32(registers):
            """
            Signed 32-bit integer from 2 registers.
            Big-endian: first register is high word, second is low word.
            """
            high = registers[0]
            low = registers[1]
            packed = struct.pack('>HH', high, low)
            return struct.unpack('>i', packed)[0]

        def _decode_u64(registers):
            """
            Unsigned 64-bit integer from 4 registers.
            Big-endian: registers[0] is most significant.
            """
            packed = struct.pack('>HHHH', registers[0], registers[1], registers[2], registers[3])
            return struct.unpack('>Q', packed)[0]

        def _decode_i64(registers):
            """
            Signed 64-bit integer from 4 registers.
            Big-endian: registers[0] is most significant.
            """
            packed = struct.pack('>HHHH', registers[0], registers[1], registers[2], registers[3])
            return struct.unpack('>q', packed)[0]

        def _decode_utf8(registers):
            """
            Decode ASCII string from registers.
            Each register contains 2 ASCII characters (big-endian).
            Per PDF Section 2.1 Register 38: ESN is "ASCII, 16 bytes" (8 registers).

            Note: Despite the parameter name UTF8 (inherited from codebase),
            GoodWe specifically uses ASCII encoding per the PDF specification.
            """
            # Convert registers to bytes (big-endian)
            byte_data = b''
            for reg in registers:
                # Each register is 2 bytes, big-endian
                byte_data += struct.pack('>H', reg)

            # Decode as ASCII (per PDF specification), strip null terminators and whitespace
            decoded = byte_data.decode('ascii', errors='ignore').rstrip('\x00').strip()
            return decoded

        # Dispatch to appropriate decoder
        if dtype == DataType.U16:
            return _decode_u16(registers)
        elif dtype == DataType.I16:
            return _decode_i16(registers)
        elif dtype == DataType.U32:
            return _decode_u32(registers)
        elif dtype == DataType.I32:
            return _decode_i32(registers)
        elif dtype == DataType.U64:
            return _decode_u64(registers)
        elif dtype == DataType.I64:
            return _decode_i64(registers)
        elif dtype == DataType.UTF8:
            return _decode_utf8(registers)
        else:
            raise NotImplementedError(f"Data type {dtype} decoding not implemented for GoodWe")

    @staticmethod
    def _encoded(value, dtype):
        """
        Encode value to write to GoodWe EzLogger registers.

        GoodWe uses big-endian encoding per MODBUS-TCP standard.

        Parameters:
        -----------
        value: int, float, or str value to encode
        dtype: DataType enum (U16, I16, U32, I32, UTF8)

        Returns:
        --------
        list[int]: List of 16-bit register values to write
        """
        import struct

        def _encode_u16(value):
            """Encode unsigned 16-bit integer"""
            U16_MAX = 2**16 - 1

            if isinstance(value, float):
                value = int(value)

            if value > U16_MAX:
                raise ValueError(f"Cannot write {value=} to U16 register (max {U16_MAX})")
            if value < 0:
                raise ValueError(f"Cannot write negative {value=} to U16 register")

            return [int(value)]

        def _encode_i16(value):
            """Encode signed 16-bit integer"""
            I16_MIN = -(2**15)
            I16_MAX = 2**15 - 1

            if isinstance(value, float):
                value = int(value)

            if value > I16_MAX or value < I16_MIN:
                raise ValueError(f"Cannot write {value=} to I16 register (range {I16_MIN} to {I16_MAX})")

            # Pack as signed, unpack as unsigned for register value
            packed = struct.pack('>h', int(value))
            return [struct.unpack('>H', packed)[0]]

        def _encode_u32(value):
            """
            Encode unsigned 32-bit integer to 2 registers.
            Big-endian: first register is high word, second is low word.
            """
            U32_MAX = 2**32 - 1

            if isinstance(value, float):
                value = int(value)

            if value > U32_MAX:
                raise ValueError(f"Cannot write {value=} to U32 register (max {U32_MAX})")
            if value < 0:
                raise ValueError(f"Cannot write negative {value=} to U32 register")

            # Pack as 32-bit unsigned, unpack as two 16-bit values (big-endian)
            packed = struct.pack('>I', int(value))
            high, low = struct.unpack('>HH', packed)
            return [high, low]

        def _encode_i32(value):
            """
            Encode signed 32-bit integer to 2 registers.
            Big-endian: first register is high word, second is low word.
            """
            I32_MIN = -(2**31)
            I32_MAX = 2**31 - 1

            if isinstance(value, float):
                value = int(value)

            if value > I32_MAX or value < I32_MIN:
                raise ValueError(f"Cannot write {value=} to I32 register (range {I32_MIN} to {I32_MAX})")

            # Pack as 32-bit signed, unpack as two 16-bit values (big-endian)
            packed = struct.pack('>i', int(value))
            high, low = struct.unpack('>HH', packed)
            return [high, low]

        def _encode_utf8(value):
            """
            Encode ASCII string to registers.
            Each register contains 2 ASCII characters (big-endian).
            Per PDF Section 2.1: Strings are ASCII encoded (e.g., ESN register).

            Note: Despite the parameter name UTF8 (inherited from codebase),
            GoodWe specifically uses ASCII encoding per the PDF specification.
            This prevents multi-byte character issues and ensures proper alignment.
            """
            if not isinstance(value, str):
                value = str(value)

            # Encode to ASCII bytes (will raise UnicodeEncodeError if non-ASCII chars present)
            try:
                byte_data = value.encode('ascii')
            except UnicodeEncodeError as e:
                raise ValueError(f"String '{value}' contains non-ASCII characters. "
                               f"GoodWe registers require ASCII encoding only.") from e

            # Pad to even length with null bytes
            if len(byte_data) % 2 != 0:
                byte_data += b'\x00'

            # Convert bytes to registers (2 bytes per register, big-endian)
            registers = []
            for i in range(0, len(byte_data), 2):
                reg_value = struct.unpack('>H', byte_data[i:i+2])[0]
                registers.append(reg_value)

            return registers

        # Dispatch to appropriate encoder
        if dtype == DataType.U16:
            return _encode_u16(value)
        elif dtype == DataType.I16:
            return _encode_i16(value)
        elif dtype == DataType.U32:
            return _encode_u32(value)
        elif dtype == DataType.I32:
            return _encode_i32(value)
        elif dtype == DataType.UTF8:
            return _encode_utf8(value)
        else:
            raise NotImplementedError(f"Data type {dtype} encoding not implemented for GoodWe") 