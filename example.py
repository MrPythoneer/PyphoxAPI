import time


import pyphox


HOST = "192.168.193.215:8080"

def StartStopExample():
    conn = pyphox.connect(HOST)

    # 'Start' and 'stop' only start and stop measuring
    # There's no urgency to even run these functions
    conn.start()
    time.sleep(5)
    conn.stop()


def SensorsExample():
    # Before running this, run an experiment in Phyphox
    # that utilizes the light sensor. Don't forget to allow
    # Remote Access and change the HOST to the one provided
    # in the app
    conn = pyphox.connect(HOST)

    light: pyphox.VSensor = conn.register_sensor(pyphox.SensorType.LIGHT)

    conn.start()
    time.sleep(1)
    print("light: ", light.get_value())
    conn.stop()

if __name__ == '__main__':
    SensorsExample()
