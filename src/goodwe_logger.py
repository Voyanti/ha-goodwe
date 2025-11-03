from typing import final

from enums import Parameter
from server import Server

goodwe_parameters: dict[str, Parameter] = {
    # TODO
}


@final
class GoodweLogger(Server):
    def __init__(self, name, serial, modbus_id, connected_client):
        super().__init__(name, serial, modbus_id, connected_client)

        self._manufacturer = "Goodwe"
        self._supported_models = ('') 
        self._serialnum = "unknown"
        self._parameters = dict.copy(goodwe_parameters)
        self._write_parameters = {}

    @property
    def manufacturer(self):
        return self._manufacturer
    
    @property
    def write_parameters(self):
        return self._write_parameters