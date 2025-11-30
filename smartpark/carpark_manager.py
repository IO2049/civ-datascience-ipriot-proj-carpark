from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config, write_config
import logging
import time

'''
    TODO: 
    - make your own module, or rename this one. Yours won't be a mock-up, so "mocks" is a bad name here. -DONE-
    - Read your configuration from a file. -DONE-
    - Write entries to a log file when something happens.
    - The "display" should update instantly when something happens
    - Make a "Car" class to contain information about cars:
        * License plate number. You can use this as an identifier
        * Entry time
        * Exit time
    - The manager class should record all activity. This includes:
        * Cars arriving
        * Cars departing
        * Temperature measurements.
    - The manager class should provide informtaion to potential customers:
        * The current time (optional)
        * The number of bays available
        * The current temperature
    
'''
class CarparkManager(CarparkSensorListener,CarparkDataProvider):
    #constant, for where to get the configuration data
    CONFIG_FILE = "samples_and_snippets\\config.json"

    def __init__(self, log_file='carpark.log'):
        #Load config
        self.config_data = parse_config(CarparkManager.CONFIG_FILE)

        #Setup logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'

        )
        logging.info('CarparkManager started')
        pass

    @property
    def available_spaces(self):
        return self.config_data['total-spaces']
    
    @property
    def temperature(self):
        return self.config_data['temperature']

    @property
    def current_time(self):
        return time.localtime()

    def incoming_car(self,license_plate):
        print('Car in! ' + license_plate)
        old_spaces = self.config_data.get(0, self.config_data['total-spaces'])
        old_cars = self.config_data.get(0, self.config_data['total-cars'])
        self.config_data['total-spaces'] = max(0, self.config_data['total-spaces'] - 1)
        self.config_data['total-cars'] = max(0, self.config_data['total-cars'] + 1)
        write_config(self.CONFIG_FILE, self.config_data)
        logging.info(f'Available spaces: {old_spaces} -> {self.config_data['total-spaces']}')
        logging.info(f'Total cars: {old_cars} -> {self.config_data['total-cars']}')

    def outgoing_car(self,license_plate):
        print('Car out! ' + license_plate)
        old_spaces = self.config_data.get(0, self.config_data['total-spaces'])
        old_cars = self.config_data.get(0, self.config_data['total-cars'])
        self.config_data['total-spaces'] = max(0, self.config_data['total-spaces'] + 1)
        self.config_data['total-cars'] = max(0, self.config_data['total-cars'] - 1)
        write_config(self.CONFIG_FILE, self.config_data)
        logging.info(f'Available spaces: {old_spaces} -> {self.config_data['total-spaces']}')
        logging.info(f'Total cars: {old_cars} -> {self.config_data['total-cars']}')

    def temperature_reading(self,reading):
        print(f'temperature is {reading}')
        self.config_data['temperature'] = reading
        write_config(self.CONFIG_FILE, self.config_data)
        logging.info(f'Temperature updated to: {self.config_data['temperature']}')

class Car:
    def __init__(self,plate=None):
        self.LicensePlate = plate
        self.EntryTime = entry_time
        self.ExitTime = exit_time
        
        