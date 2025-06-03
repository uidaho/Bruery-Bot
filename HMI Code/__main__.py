# Created by Phillip Boettcher on 5/8/25
# Go Vandals


import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
from PyQt6.QtCore import QTimer
import pyqt_simple as PyQtS
from modbus import modbus_client




class GuiHMI:

    gui = PyQtS.PyQtSimple()

    set_temperature = None
    temperature = 0
    set_level = None
    level = 0
    gas = 0
    pressure = 0

    def __init__(self):


        self.app, self.window, self.layout = self.gui.create_window('Brewery Bot HMI', 'grid', (800, 600))


        self.setup_ui()

        self.update_modbus_read()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_modbus_read)
        self.timer.start(5000)
        self.window.show()
        sys.exit(self.app.exec())

    def setup_ui(self):
        title = self.gui.create_label(self.layout, 'Brewery Bot HMI', 0, 1, 'left')
        font = title.font()
        font.setBold(True)
        font.setPointSize(20)
        title.setFont(font)

        ## Time ---------------------------------------------------------------------------------------------
        time_row = 1

        self.gui.create_label(self.layout, 'Run Time (min):', time_row, 1, 'right')
        self.run_time_label = self.gui.create_label(self.layout, '', time_row, 2, 'left')

        self.gui.create_label(self.layout, 'Lag Time (min):', time_row, 3, 'right')
        self.lag_time_label = self.gui.create_label(self.layout, '', time_row, 4, 'left')

        self.gui.create_label(self.layout, 'Update Set Lag Time (min):', time_row, 5, 'right')
        self.set_lag_time_entry = self.gui.create_entrybox(self.layout, time_row, 6, 'left')
        update_set_lag_time_button = self.gui.create_button(self.layout, 'Update', self.write_modbus_exp_lag_time, time_row, 7)
        ## ---------------------------------------------------------------------------------------------------




        ## Temperature ---------------------------------------------------------------------------------------
        temp_row = 2

        self.gui.create_label(self.layout, 'Actual Temperature (C):', temp_row, 1, 'right')
        self.temperature_label = self.gui.create_label(self.layout, '', temp_row, 2, 'left')

        self.gui.create_label(self.layout, 'Set Temperature (C):', temp_row, 3, 'right')
        self.set_temp_label = self.gui.create_label(self.layout, '', temp_row, 4, 'left')

        self.gui.create_label(self.layout, 'Update Set Temperature (C):', temp_row, 5, 'right')
        self.set_temp_entry = self.gui.create_entrybox(self.layout, temp_row, 6, 'left')
        update_set_temp_button = self.gui.create_button(self.layout, 'Update', self.write_modbus_set_temp, temp_row, 7)
        ## ---------------------------------------------------------------------------------------------------





        ## Pumps -------------------------------------------------------------------------------------------
        pump_row = 3

        self.gui.create_label(self.layout, 'Set Pump On Time (sec):', pump_row, 3, 'right')
        self.pump_on_time_label = self.gui.create_label(self.layout, 0, 3, 4, 'left')

        self.gui.create_label(self.layout, 'Update Pump On Time (sec):', pump_row, 5, 'right')
        self.update_pump_on_time_entry = self.gui.create_entrybox(self.layout, pump_row,6, 'left')
        update_pump_on_time_button = self.gui.create_button(self.layout, 'Update', self.write_modbus_pump_on_time, pump_row, 7)

        self.gui.create_label(self.layout, 'Set Pump Pulse Length (sec):', pump_row+1, 3, 'right')
        self.pump_pulse_length_label = self.gui.create_label(self.layout, 0, 4, 4, 'left')

        self.gui.create_label(self.layout, 'Update Pump Pulse Length (sec):', pump_row+1, 5, 'right')
        self.update_pulse_length_entry = self.gui.create_entrybox(self.layout, pump_row+1,6, 'left')
        update_pulse_length_button = self.gui.create_button(self.layout, 'Update', self.write_modbus_pump_pulse_length, pump_row+1, 7)
        ## ---------------------------------------------------------------------------------------------------


        ## Motor ------------------------------------------------------------------------------------------
        motor_row = 5

        self.gui.create_label(self.layout, 'Set Motor Speed (rpm):', motor_row, 3, 'right')
        self.set_motor_speed_label = self.gui.create_label(self.layout, 0, motor_row, 4, 'left')

        self.gui.create_label(self.layout, 'Update Set Motor Speed (rpm):', motor_row, 5, 'right')
        self.update_set_motor_speed_entry = self.gui.create_entrybox(self.layout, motor_row, 6, 'left')
        update_set_motor_speed_button = self.gui.create_button(self.layout, 'Update', self.write_modbus_motor_set_speed, motor_row, 7)
        ## ---------------------------------------------------------------------------------------------------

        ## Coils
        coil_row = 6

        self.gui.create_label(self.layout, 'On:', coil_row, 1, 'right')
        self.on_off_label = self.gui.create_label(self.layout, None, coil_row, 2, 'left')

        self.gui.create_label(self.layout, 'Run Experiment:', coil_row, 3, 'right')
        self.run_exp_label = self.gui.create_label(self.layout, None, coil_row, 4, 'left')

        self.gui.create_label(self.layout, 'Feedstock Low:', coil_row, 5, 'right')
        self.feedstock_low_label = self.gui.create_label(self.layout, None, coil_row, 6, 'left')

        self.gui.create_label(self.layout, 'Feedstock Empty:', coil_row+1, 1, 'right')
        self.feedstock_empty_label = self.gui.create_label(self.layout, None, coil_row+1, 2, 'left')

        self.gui.create_label(self.layout, 'Waste Full:', coil_row+1, 3, 'right')
        self.waste_full_label = self.gui.create_label(self.layout, None, coil_row+1, 4, 'left')

        self.gui.create_label(self.layout, 'Temperature Out of Range:', coil_row+1, 5, 'right')
        self.temp_out_of_range_label = self.gui.create_label(self.layout, None, coil_row+1, 6, 'left')

        self.gui.create_label(self.layout, 'Level Out of Range:', coil_row+2, 1, 'right')
        self.level_out_of_range_label = self.gui.create_label(self.layout, None, coil_row+2, 2, 'left')

        self.gui.create_label(self.layout, 'Pumps in Auto:', coil_row+2, 3, 'right')
        self.pumps_in_auto_label = self.gui.create_label(self.layout, None, coil_row+2, 4, 'left')

        self.gui.create_label(self.layout, 'Run Pumps in Hand:', coil_row+2, 5, 'right')
        self.pumps_in_hand_label = self.gui.create_label(self.layout, None, coil_row+2, 6, 'left')

        self.gui.create_label(self.layout, 'Pumps Paused for Fill or Empty:', coil_row+3, 1, 'right')
        self.pumps_paused_label = self.gui.create_label(self.layout, None, coil_row+3, 2, 'left')



    def write_modbus(self):
        pass

    def write_modbus_set_temp(self):
        try:
            modbus = modbus_client()
            register = 1
            value = self.set_temp_entry.text()
            value = float(value) * 10
            value = int(value)

            modbus.write_modbus(register, value)
            self.update_modbus_read()
        except ValueError:
            pass

    def write_modbus_motor_set_speed(self):
        try:
            modbus = modbus_client()
            register = 0
            value = self.update_set_motor_speed_entry.text()
            value = int(value)
            modbus.write_modbus(register, value)
            self.update_modbus_read()
        except ValueError:
            pass

    
    def write_modbus_exp_lag_time(self):
        try:
            modbus = modbus_client()
            register = 4
            value = self.set_lag_time_entry.text()
            value = int(value)
            modbus.write_modbus(register, value)
            self.update_modbus_read()
        except ValueError:
            pass

    
    def write_modbus_pump_on_time(self):
        try:
            modbus = modbus_client()
            register = 5
            value = self.update_pump_on_time_entry.text()
            value = int(value)
            modbus.write_modbus(register, value)
            self.update_modbus_read()
        except ValueError:
            pass

    def write_modbus_pump_pulse_length(self):
        try:
            modbus = modbus_client()
            register = 6
            value = self.update_pulse_length_entry.text()
            value = int(value)
            modbus.write_modbus(register, value)
            self.update_modbus_read()
        except ValueError:
            pass




    def update_modbus_read(self):
        try:
            modbus = modbus_client()
            motor_set_speed = modbus.regs[0]
            temp_set_point = modbus.regs[1]
            main_tank_temp = modbus.regs[2]
            exp_run_time = modbus.regs[3]
            exp_lag_time = modbus.regs[4]
            pump_on_time = modbus.regs[5]
            pump_pulse_length = modbus.regs[6]

            main_tank_temp = main_tank_temp / 10.0
            temp_set_point = temp_set_point / 10.0
            self.temperature_label.setText(f'{main_tank_temp}')
            self.set_temp_label.setText(f'{temp_set_point}')

            self.run_time_label.setText(f'{exp_run_time}')
            self.lag_time_label.setText(f'{exp_lag_time}')

            self.pump_on_time_label.setText(f'{pump_on_time}')
            self.pump_pulse_length_label.setText(f'{pump_pulse_length}')

            self.set_motor_speed_label.setText(f'{motor_set_speed}')

            run_exp = modbus.coils[1]
            on_off = modbus.coils[0]
            feedstock_low = modbus.coils[2]
            feedstock_empty = modbus.coils[3]
            waste_full = modbus.coils[4]
            temp_out_of_range = modbus.coils[5]
            level_out_of_range = modbus.coils[6]
            pumps_in_auto = modbus.coils[7]
            run_pumps_in_hand = modbus.coils[8]
            pumps_paused_for_fill_empty = modbus.coils[9]

            self.on_off_label.setText(f'{on_off}')
            self.run_exp_label.setText(f'{run_exp}')
            self.feedstock_low_label.setText(f'{feedstock_low}')
            self.feedstock_empty_label.setText(f'{feedstock_empty}')
            self.waste_full_label.setText(f'{waste_full}')
            self.temp_out_of_range_label.setText(f'{temp_out_of_range}')
            self.level_out_of_range_label.setText(f'{level_out_of_range}')
            self.pumps_in_auto_label.setText(f'{pumps_in_auto}')
            self.pumps_in_hand_label.setText(f'{run_pumps_in_hand}')
            self.pumps_paused_label.setText(f'{pumps_paused_for_fill_empty}')
        except TypeError:
            self.gui.create_label(self.layout, 'Modbus Error! Check Modbus Parameters / Ethernet Connection', 10, 5)



if __name__ == '__main__':
    GuiHMI()
