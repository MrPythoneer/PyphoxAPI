from typing import Any


class Sensor:
    """Represents a Phyphox sensor"""

    __slots__ = ('prefix', 'phyphox')
    prefix: str
    phyphox: Any

    def __init__(self, phyphox: Any, prefix: str) -> None:
        self.prefix = prefix
        self.phyphox = phyphox

    def get(self, var: str) -> float:
        """Returns the 'var' value of the sensor from phyphox sensors_data"""
        return self.phyphox.sensors_data[self.prefix+var]

    def get_time(self) -> float:
        """Returns the Time value of the sensor from phyphox sensors_data"""
        return self.get('_time')

    def include_time(self) -> None:
        """Next Fetch() calls will fetch the sensor time"""
        self.phyphox.query += self.prefix + '_time&'


class XYZSensor(Sensor):
    """Represents a sensor with X, Y, and Z variables"""

    def get_x(self) -> float:
        """Returns the X value of the sensor from phyphox sensors_data"""
        return self.get('X')

    def get_y(self) -> float:
        """Returns the Y value of the sensor from phyphox sensors_data"""
        return self.get('Y')

    def get_z(self) -> float:
        """Returns the Z value of the sensor from phyphox sensors_data"""
        return self.get('Z')

    def include_x(self) -> None:
        """Next Fetch() calls will fetch the X value form the sensor"""
        self.phyphox.query += self.prefix + 'X&'

    def include_y(self) -> None:
        """Next Fetch() calls will fetch the X value form the sensor"""
        self.phyphox.query += self.prefix + 'Y&'

    def include_z(self) -> None:
        """Next Fetch() calls will fetch the X value form the sensor"""
        self.phyphox.query += self.prefix + 'Z&'

    def include_all(self) -> None:
        """Next Fetch() calls will fetch all the data form the sensor besides time"""
        self.phyphox.query += (self.prefix + 'X&' +
                               self.prefix + 'Y&' +
                               self.prefix + 'Z&')


class VSensor(Sensor):
    """Represents a single-value sensor"""

    def get_value(self) -> float:
        """Returns the value of the sensor from phyphox sensors_data"""
        return self.phyphox.sensors_data[self.prefix]
