# Created by Phillip Boettcher and Joshua Werner on 5/8/25
# Go Vandals

from pyModbusTCP.client import ModbusClient
import numpy as np


class modbus_client():
    def __init__(self):
        self.c = ModbusClient(host="192.168.1.10", port=502, unit_id=1, auto_open=True)

        self.regs = self.c.read_holding_registers(0, 7)
        self.coils = self.c.read_coils(0, 10)

        print('regs:' + str(self.regs))
        print('coils:' + str(self.coils))



    def write_modbus(self, register, value):

        if self.regs:
            print(self.regs)
        else:
            print("read error")

        self.c.write_single_register(register,value)

