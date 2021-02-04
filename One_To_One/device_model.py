from random import random
from pickle import dumps, loads

class Hardware():
    def __init__(self, sensors):
        self.sensors = sensors

    def __str__(self):
        return f'Hardware: {self.sensors}'

    def sim_value(self, key):
        return random() * (self.sensors[key][1] - self.sensors[key][0]) + self.sensors[key][0]

    def sim_all(self):
        result = {}
        for key in self.sensors:
            result[key] = self.sim_value(key)
        return result

    def serialize(self):
        return dumps(self.sim_all())


if __name__ == '__main__':
    h = Hardware({'temp': (80, 90), 'humidity': (40, 50)})
    print(h)
    print(h.serialize())
    print(loads(h.serialize()))
