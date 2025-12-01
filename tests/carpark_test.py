import unittest
import tempfile
import sys,os
import logging
from pathlib import Path
cwd = Path(os.path.dirname(__file__))
parent = str(cwd.parent)

sys.path.append(parent + "/smartpark")


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

#Change the line below to import your manager class
from smartpark.carpark_manager import CarparkManager, Car


class TestProject(unittest.TestCase):

    def test_fresh_carpark(self):
        """Test 1: config.json if being read correctly"""
        # arrange
        """Set config["CarParks]["free-spaces] = 1000"""
        # act
        carpark = CarparkManager()
        # assert
        self.assertEqual(1000,carpark.available_spaces)

    def test_temp(self):
        """Test 2: config.json if being read correctly"""
        # arrange
        """Set config["CarParks]["temperature] = 12.0"""
        # act
        carpark = CarparkManager()
        # assert
        self.assertEqual(12.0,carpark.temperature)

if __name__=="__main__":
#    print("cwd: " + parent + "/smartpark")
    unittest.main()
