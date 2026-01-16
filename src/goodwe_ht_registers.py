from .enums import DataType, DeviceClass, HAEntityType, Parameter, RegisterTypes, WriteParameter, WriteSelectParameter

goodwe_ht_parameters: dict[str, Parameter] = {
    # Status 1 (Register 32002)
    "Status 1": Parameter(
        addr=32002+1, count=1, dtype=DataType.U16, multiplier=1/1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER,
        value_template= """
                            {% set states = {
                            '0': 'Standby',
                            '1': 'In operation',
                            '2': 'Fault',
                            '3': 'Self-checking',
                            '4': 'Updating',
                            '5': 'Night mode'
                            } %}
                            {{ states[value] if value in states else 'unknown' }}
                            """
    ),

    # Input DC Power (Register 32064)
    "Input DC Power": Parameter(
        addr=32064+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="kW",
        device_class=DeviceClass.POWER,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Grid Line Voltages (Registers 32066-32068)
    "Grid AB Voltage": Parameter(
        addr=32066+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid BC Voltage": Parameter(
        addr=32067+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid CA Voltage": Parameter(
        addr=32068+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Grid Phase Voltages (Registers 32069-32071)
    "Grid A Phase Voltage": Parameter(
        addr=32069+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid B Phase Voltage": Parameter(
        addr=32070+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid C Phase Voltage": Parameter(
        addr=32071+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Grid Phase Currents (Registers 32072-32076)
    # Note: S32 (signed 32-bit) per protocol
    "Grid A Phase Current": Parameter(
        addr=32072+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="A",
        device_class=DeviceClass.CURRENT,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid B Phase Current": Parameter(
        addr=32074+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="A",
        device_class=DeviceClass.CURRENT,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid C Phase Current": Parameter(
        addr=32076+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="A",
        device_class=DeviceClass.CURRENT,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Peak Active Power (Register 32078)
    "Peak Active Power": Parameter(
        addr=32078+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="kW",
        device_class=DeviceClass.POWER,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Active Power (Register 32080)
    "Active Power": Parameter(
        addr=32080+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="kW",
        device_class=DeviceClass.POWER,
        register_type=RegisterTypes.HOLDING_REGISTER,
        state_class="measurement"
    ),

    # Reactive Power (Register 32082)
    "Reactive Power": Parameter(
        addr=32082+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="kVar",
        device_class=DeviceClass.POWER,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Power Factor (Register 32084)
    "Power Factor": Parameter(
        addr=32084+1, count=1, dtype=DataType.I16, multiplier=1/1000, unit="",
        device_class=DeviceClass.POWER_FACTOR,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Grid Frequency (Register 32085)
    "Grid Frequency": Parameter(
        addr=32085+1, count=1, dtype=DataType.U16, multiplier=1/100, unit="Hz",
        device_class=DeviceClass.FREQUENCY,
        register_type=RegisterTypes.HOLDING_REGISTER,
        state_class="measurement"
    ),

    # Efficiency (Register 32086)
    "Efficiency": Parameter(
        addr=32086+1, count=1, dtype=DataType.U16, multiplier=1/100, unit="%",
        device_class=DeviceClass.POWER_FACTOR,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Internal Temperature (Register 32087)
    "Internal Temperature": Parameter(
        addr=32087+1, count=1, dtype=DataType.I16, multiplier=1/10, unit="C",
        device_class=DeviceClass.TEMPERATURE,
        register_type=RegisterTypes.HOLDING_REGISTER,
        state_class="measurement"
    ),

    # Energy Counters (Registers 32106, 32114, 32116, 32118)
    "Cumulative Energy": Parameter(
        addr=32106+1, count=2, dtype=DataType.U32, multiplier=1/100, unit="kWh",
        device_class=DeviceClass.ENERGY,
        register_type=RegisterTypes.HOLDING_REGISTER,
        state_class="total"
    ),
    "Daily Energy": Parameter(
        addr=32114+1, count=2, dtype=DataType.U32, multiplier=1/100, unit="kWh",
        device_class=DeviceClass.ENERGY,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Monthly Energy": Parameter(
        addr=32116+1, count=2, dtype=DataType.U32, multiplier=1/100, unit="kWh",
        device_class=DeviceClass.ENERGY,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Yearly Energy": Parameter(
        addr=32118+1, count=2, dtype=DataType.U32, multiplier=1/100, unit="kWh",
        device_class=DeviceClass.ENERGY,
        register_type=RegisterTypes.HOLDING_REGISTER,
        state_class="total_increasing"
    ),

    # Device Information (Registers 35502, 35510)
    "Serial Number": Parameter(
        addr=35502+1, count=1, dtype=DataType.UTF8, multiplier=1/1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Model": Parameter(
        addr=35510+1, count=8, dtype=DataType.UTF8, multiplier=1/1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # DSP Versions (Registers 35515, 35516)
    "DSP1 Version": Parameter(
        addr=35515+1, count=1, dtype=DataType.U16, multiplier=1/1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "DSP2 Version": Parameter(
        addr=35516+1, count=1, dtype=DataType.U16, multiplier=1/1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Fault Codes (Register 35710)
    "DSP Fault Code": Parameter(
        addr=35710+1, count=2, dtype=DataType.U32, multiplier=1/1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # DC Bus Voltage (Register 35753)
    "DC Bus Voltage": Parameter(
        addr=35753+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # ISO Value (Register 35757)
    "ISO Value": Parameter(
        addr=35757+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="kohm",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    # "Max Active Power": Parameter( # slave device failure when reading on G@-1000K
    #     addr=41380+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="kW",
    #     device_class=DeviceClass.POWER,
    #     register_type=RegisterTypes.HOLDING_REGISTER
    # ),

    # Status 2 (Register 37207)
    # Often observe slave device failure with this register.
    # "Status 2": Parameter(
    #     addr=37207+1, count=1, dtype=DataType.U16, multiplier=1/1, unit="",
    #     device_class=DeviceClass.ENUM,
    #     register_type=RegisterTypes.HOLDING_REGISTER
    # ),
}


# TODO set up mppt register number according to model
for i in range(1, 21):
    goodwe_ht_parameters.update({
        f"PV{i} Voltage": Parameter(
            addr=32016+2*(i-1)+1, count=1, dtype=DataType.I16, multiplier=1/10, unit="V",
            device_class=DeviceClass.VOLTAGE,
            register_type=RegisterTypes.HOLDING_REGISTER,
            state_class="measurement"
        ),
    # PV String Currents (Address 32017-32055)
    f"PV{i} Current": Parameter(
        addr=32017+2*(i-1)+1, count=1, dtype=DataType.I16, multiplier=1/100, unit="A",
        device_class=DeviceClass.CURRENT,
        register_type=RegisterTypes.HOLDING_REGISTER,
        state_class="measurement"
    ),
    })


goodwe_ht_write_params: dict[str, WriteParameter | WriteSelectParameter] = {
    "Active Power Control": WriteParameter(
        addr=42408+1,
        count=1,
        dtype=DataType.I16,
        multiplier=1/10,
        register_type=RegisterTypes.HOLDING_REGISTER,
        ha_entity_type=HAEntityType.NUMBER,
        min=0, 
        max=110,
        unit="%"
    ),
    "Command Power On": WriteParameter(
        addr=41330+1,
        count=1,
        dtype=DataType.U16,
        multiplier=1,
        register_type=RegisterTypes.HOLDING_REGISTER,
        ha_entity_type=HAEntityType.BUTTON,
        payload_press=0
    ),
    "Command Power Off": WriteParameter(
        addr=41331+1,
        count=1,
        dtype=DataType.U16,
        multiplier=1,
        register_type=RegisterTypes.HOLDING_REGISTER,
        ha_entity_type=HAEntityType.BUTTON,
        payload_press=0
    ),
    "Power Switch": WriteParameter(
        addr=41331+1,
        count=1,
        dtype=DataType.U16,
        multiplier=1,
        register_type=RegisterTypes.HOLDING_REGISTER,
        ha_entity_type=HAEntityType.SWITCH,
        payload_on=1,
        payload_off=0,
        always_available=True
    )
}

if __name__ == "__main__":
    from pprint import pprint
    pprint(goodwe_ht_parameters)