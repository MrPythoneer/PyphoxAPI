import json
from typing import Any
from urllib.request import urlopen

from .sensortypes import SensorType
from .sensors import Sensor, VSensor, XYZSensor


class Pyphox:
    '''Represents a connection to the remote server and controls the experiment'''

    __slots__ = ('address', 'query', 'sensors', 'sensors_data')

    address: str
    query: str
    sensors: list[str]
    sensors_data: set[str, float]

    def __init__(self, address: str, sensors: list[str]):
        self.address = address
        self.sensors = sensors
        self.query = ""
        self.sensors_data = []

    def register_sensor(self, sensor: SensorType) -> Sensor:
        '''
        Returns XYZSensor or VSensor representing a sensor in the experiment.

        Since VSensor has only one variable, it's automatically going to be \
        fetched with Fetch()

        Since XYZSensor has several variables, none will be fetched with Fetch().
        In order to fetch data from the sensor, IncludeX, IncludeY or IncludeZ \
        should be called.
        '''
        if not self.has_sensor(sensor):
            return None

        prefix = sensor.prefix()
        stype = sensor.value.type
        if stype == 'XYZ':
            return XYZSensor(self, prefix)

        elif stype == 'V':
            self.query += prefix + "&"
            return VSensor(self, prefix)

        else:
            return None

    def has_sensor(self, sensor: SensorType) -> bool:
        '''Returns true if the experiment uses the given sensor type, \
           otheriwse, false will be returned'''
        return sensor.value.name in self.sensors

    def execute(self, command: str) -> dict[str, Any]:
        '''Executes some remote command on the host. Returns the JSON-like \
           result of the command'''
        resp = urlopen(self.address + command)
        data = json.load(resp)
        resp.close()

        return data

    def fetch(self) -> None:
        '''Requests the remote host for the latest data. The data will be \
           saved to the SensorsData field'''
        res = self.execute("/get?" + self.query)

        data = {}
        for k, v in res["buffer"].items():
            data[k] = v["buffer"][0]

        self.sensors_data = data

    def start(self) -> bool:
        '''Starts measuring. By default, Fetch() is called automatically'''
        res = self.execute("/control?cmd=start")
        self.fetch()
        return res["result"]

    def stop(self) -> bool:
        '''Stops measuring'''
        res = self.execute("/control?cmd=stop")
        return res["result"]

    def clear(self) -> bool:
        '''Clears the experiment buffer'''
        res = self.execute("/control?cmd=clear")
        return res["result"]


def connect(address: str) -> Pyphox:
    '''Connects to the remote experiment at the given address'''
    address = "http://" + address
    config_resp = urlopen(address + "/config")

    sensors = []
    for inp in json.load(config_resp)['inputs']:
        sensor = inp['source']
        sensors.append(sensor)

    config_resp.close()

    return Pyphox(address, sensors)
