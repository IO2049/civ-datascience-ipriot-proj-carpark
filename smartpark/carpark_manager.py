from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config, write_config
import logging
import time

'''
    TODO: 
    - make your own module, or rename this one. Yours won't be a mock-up, so "mocks" is a bad name here. -DONE-
    - Read your configuration from a file. -DONE-
    - Write entries to a log file when something happens. -DONE-
    - The "display" should update instantly when something happens -DONE-
    - Make a "Car" class to contain information about cars: -DONE-
        * License plate number. You can use this as an identifier -DONE-
        * Entry time -DONE-
        * Exit time -DONE-
    - The manager class should record all activity. This includes: -DONE-
        * Cars arriving -DONE-
        * Cars departing -DONE-
        * Temperature measurements. -DONE-
    - The manager class should provide informtaion to potential customers: -DONE-
        * The current time (optional) -DONE-
        * The number of bays available -DONE-
        * The current temperature -DONE-
    
'''
class CarparkManager(CarparkSensorListener,CarparkDataProvider):
    #constant, for where to get the configuration data
    CONFIG_FILE = "samples_and_snippets\\config.json"

    def __init__(self, log_file='carpark.log'):
        #Load config
        self.config_data = parse_config(self.CONFIG_FILE)
        self.car = Car(self.config_data)

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
        return self.config_data['free-spaces']
    
    @property
    def temperature(self):
        return self.config_data['temperature']

    @property
    def current_time(self):
        return time.localtime()

    def incoming_car(self,license_plate):
        old_spaces = self.config_data['free-spaces']
        old_cars = self.config_data['total-cars']
        if old_spaces == 0:
            print("No available spaces")
            logging.warning(f"Attempted to exceed limits")
            return False

        print('Car in! ' + license_plate)
        self.car.record_license(license_plate)

        self.config_data['free-spaces'] = max(0, self.config_data['free-spaces'] - 1)
        self.config_data['total-cars'] = max(0, self.config_data['total-cars'] + 1)
        write_config(self.CONFIG_FILE, self.config_data)
        logging.info(f'Available spaces: {old_spaces} -> {self.config_data['free-spaces']}')
        logging.info(f'Total cars: {old_cars} -> {self.config_data['total-cars']}')
        return True

    def outgoing_car(self,license_plate):
        plates = self.config_data['license-plate']
        if license_plate not in plates:
            print("License not recognised")
            logging.warning(f"Attempted to remove unrecognised plates {license_plate}")
            return False
        
        print('Car out! ' + license_plate)
        self.config_data['license-plate'].remove(license_plate)
        old_spaces = self.config_data['free-spaces']
        old_cars = self.config_data['total-cars']
        self.config_data['free-spaces'] = max(0, self.config_data['free-spaces'] + 1)
        self.config_data['total-cars'] = max(0, self.config_data['total-cars'] - 1)
        write_config(self.CONFIG_FILE, self.config_data)
        logging.info(f"Available spaces: {old_spaces} -> {self.config_data['free-spaces']}")
        logging.info(f"Total cars: {old_cars} -> {self.config_data['total-cars']}")
        return True

    def temperature_reading(self,reading):
        print(f'temperature is {reading}')
        self.config_data['temperature'] = reading
        write_config(self.CONFIG_FILE, self.config_data)
        logging.info(f'Temperature updated to: {self.config_data['temperature']}')




class Car():
    CONFIG_FILE = "samples_and_snippets\\config.json"

    def __init__(self,config_data, plate=None, entry_time=0, exit_time=0, log_file='carpark.log'):
        #Load config
        self.config_data = config_data

        #Setup logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'

        )
        logging.info('CarparkManager started')

        self.LicensePlate = plate
        self.EntryTime = entry_time
        self.ExitTime = exit_time

    def record_license(self, license_plate):
        """Records string as license plate and updates JSON confing file with string
        
        Logs the recording and updating of license-plate list"""
        self.config_data['license-plate'].append(license_plate)
        write_config(self.CONFIG_FILE, self.config_data)
        logging.info(f"Recorded license: {license_plate}")
