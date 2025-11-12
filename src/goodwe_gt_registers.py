from .enums import DataType, DeviceClass, HAEntityType, Parameter, RegisterTypes, WriteParameter, WriteSelectParameter

goodwe_gt_parameters: dict[str, Parameter] = {
    # Grid Line Voltages (Address 32066-32068)
    "Grid Voltage AB": Parameter(
        addr=32066+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid Voltage BC": Parameter(
        addr=32067+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid Voltage CA": Parameter(
        addr=32068+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Grid Phase Voltages (Address 32069-32071)
    "Grid Voltage A": Parameter(
        addr=32069+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid Voltage B": Parameter(
        addr=32070+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid Voltage C": Parameter(
        addr=32071+1, count=1, dtype=DataType.U16, multiplier=1/10, unit="V",
        device_class=DeviceClass.VOLTAGE,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Grid Phase Currents (Address 32072-32076, S32 type)
    "Grid Current A": Parameter(
        addr=32072+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="A",
        device_class=DeviceClass.CURRENT,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid Current B": Parameter(
        addr=32074+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="A",
        device_class=DeviceClass.CURRENT,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid Current C": Parameter(
        addr=32076+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="A",
        device_class=DeviceClass.CURRENT,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Power and Energy (Address 32080+)
    "Active Power": Parameter(
        addr=32080+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="kW",
        device_class=DeviceClass.POWER,
        register_type=RegisterTypes.HOLDING_REGISTER,
        state_class="measurement"
    ),
    "Reactive Power": Parameter(
        addr=32082+1, count=2, dtype=DataType.I32, multiplier=1/1000, unit="kVar",
        device_class=DeviceClass.POWER,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Power Factor": Parameter(
        addr=32084+1, count=1, dtype=DataType.I16, multiplier=1/1000, unit="",
        device_class=DeviceClass.POWER_FACTOR,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Grid Frequency": Parameter(
        addr=32085+1, count=1, dtype=DataType.U16, multiplier=1/100, unit="Hz",
        device_class=DeviceClass.FREQUENCY,
        register_type=RegisterTypes.HOLDING_REGISTER,
        state_class="measurement"
    ),

    # Insulation
    # "Insulation Impedance": Parameter(
    #     addr=32088+1, count=1, dtype=DataType.U16, multiplier=1, unit="k",
    #     device_class=DeviceClass.ENUM,
    #     register_type=RegisterTypes.HOLDING_REGISTER
    # ),

    # Energy Totals
    "Total Energy Production": Parameter(
        addr=32106+1, count=2, dtype=DataType.U32, multiplier=1/100, unit="kWh",
        device_class=DeviceClass.ENERGY,
        register_type=RegisterTypes.HOLDING_REGISTER,
        state_class="total"
    ),
    "Daily Energy Production": Parameter(
        addr=32114+1, count=2, dtype=DataType.U32, multiplier=1/100, unit="kWh",
        device_class=DeviceClass.ENERGY,
        register_type=RegisterTypes.HOLDING_REGISTER,
        state_class="total_increasing"
    ),

    # Device Information
    "Serial Number": Parameter(
        addr=35502+1, count=1, dtype=DataType.UTF8, multiplier=1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Model": Parameter(
        addr=35510+1, count=1, dtype=DataType.UTF8, multiplier=1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),

    # Status and Diagnostics
    "DSP Fault Code": Parameter(
        addr=35710+1, count=2, dtype=DataType.U32, multiplier=1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
    "Work Mode": Parameter(
        addr=35758+1, count=1, dtype=DataType.U16, multiplier=1, unit="",
        device_class=DeviceClass.ENUM,
        register_type=RegisterTypes.HOLDING_REGISTER
    ),
}

for i in range(1, 21):
    goodwe_gt_parameters.update({
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

goodwe_gt_write_params: dict[str, WriteParameter | WriteSelectParameter] = {
    "Command: Power On": WriteParameter(
        addr=41330+1,
        count=1,
        dtype=DataType.U16,
        multiplier=1,
        register_type=RegisterTypes.HOLDING_REGISTER,
        ha_entity_type=HAEntityType.BUTTON,
        payload_press=0
    ),
    "Command: Power Off": WriteParameter(
        addr=41331+1,
        count=1,
        dtype=DataType.U16,
        multiplier=1,
        register_type=RegisterTypes.HOLDING_REGISTER,
        ha_entity_type=HAEntityType.BUTTON,
        payload_press=0
    ),
}


if __name__ == "__main__":
    from pprint import pprint
    pprint(goodwe_gt_parameters)