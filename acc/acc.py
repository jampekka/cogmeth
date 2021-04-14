import sys
from collections import Counter
import random
import math

from copy import deepcopy

class Vehicle:
    def __init__(self, accelerator):
        self.position = 0.0
        self.velocity = 0.0
        self.accelerator = accelerator
        self.crashed = False

# This ain't no technological breakdown, oh no, this is the RoadToHell
# https://www.youtube.com/watch?v=gUUdQfnshJ4
class RoadToHell:
    def __init__(self, length=100.0):
        self.length = length
        self.vehicles = []
        self.time = 0.0

    def spread_equally(self):
        n = len(self.vehicles)
        for i, v in enumerate(self.vehicles):
            v.position = i/n*self.length

        self.vehicles.sort(key=lambda x: x.position)

    def add_vehicle(self, accelerator):
        v = Vehicle(accelerator)
        self.vehicles.append(v)
        return v
    
    def step(self, dt):
        self.time += dt
        n = len(self.vehicles)
        for i, v in enumerate(self.vehicles):
            lv = self.vehicles[(i+1)%n]
            dx = lv.position - v.position
            dv = lv.velocity - v.velocity

            normalizer = 0.0
            if dx < 0 or n < 2:
                normalizer = self.length
                dx += normalizer
            
            accel = v.accelerator(dt, v.velocity, dx, dv)

            v.velocity += accel*dt
            v.position += v.velocity*dt
            dx = (lv.position + normalizer) - (v.position)
            
            if dx < 0 and n > 1: # TODO: Can the first car crash!?
                v.position = lv.position
                v.velocity = 0.0

def target_distance_accelerator(dt, v, dx, dv):
    target_distance = 5.0
    acceleration_magnitude = 1.0
    if dx > target_distance:
        return acceleration_magnitude
    else:
        return -acceleration_magnitude

def target_speed_accelerator(dt, v, dx, dv):
    target_velocity = 50.0/3.6
    acceleration_magnitude = 1.0
    if v < target_velocity:
        return acceleration_magnitude
    else:
        return -acceleration_magnitude

def dv_accelerator(dt, v, dx, dv):
    gain = 0.1
    accel = gain*dv
    return accel

def lagger(f, lag_n):
    history = []
    def accel(*args):
        nonlocal history
        history.insert(0, args)
        history = history[:lag_n]
        return f(*history[-1])
    return accel

def noiser(f, noise_std):
    return lambda *args: f(*args) + random.gauss(0, noise_std)

def demo():
    dur = 30
    dt = 1/100
    lag = int(1/dt)
    noise = 1.0
    start_velocity = 0.0
    
    hell = RoadToHell()
    base_a = target_speed_accelerator
    
    n_vehicles = 1
    for i in range(n_vehicles):
        a = base_a
        a = lagger(a, lag)
        a = noiser(a, noise)
        v = hell.add_vehicle(a)
        v.velocity = start_velocity
    hell.spread_equally()
    times = []
    velocity_log = []

    for i in range(int(dur/dt)):
        times.append(i*dt)
        velocities = []
        for v in hell.vehicles:
            velocities.append(v.velocity)
        velocity_log.append(velocities)
        hell.step(dt)
    
    import numpy as np
    import matplotlib.pyplot as plt
    velocity_log = np.array(velocity_log)
    plt.plot(times, velocity_log)
    plt.xlabel("Time")
    plt.ylabel("Velocity (m/s)")
    plt.show()

if __name__ == "__main__":
    demo()
