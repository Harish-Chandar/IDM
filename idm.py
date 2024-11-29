import math
import random

t = 0 # Initialize time
dt = 0.1 # Calculate values every 0.1 seconds

cars = [] # Cars array of type IDM

class IDM:
    def __init__(self, x0, v0, T, s0, a, b, v, L):
        self.x = x0 # Init position (m)
        self.v0 = v0  # Desired velocity (m/s)
        self.T = T    # Desired time gap (s)
        self.s0 = s0  # Minimum spacing (m)
        self.a = a    # Maximum acceleration (m/s2)
        self.b = b    # Comfortable deceleration (m/s2)
        self.v = v # Init Velocity (m/s)
        self.s = s0 # Init gap (m)
        self.L = L # Length of the vehicle
        if L > 20:
            self.truck = True
        else:
            self.truck = False
        self.dvdt = 0 # Placeholder for acceleration
        self.s_star = 0  # Placeholder for dynamic desired gap

    def calcAcc(self, dv, xl, l, d=4):
        self.s_star = self.s0 + max(0, self.v*self.T + (self.v*dv)/(2*math.sqrt(self.a*self.b)))
        self.dvdt = self.a*(1-math.pow(self.v/self.v0, d)-math.pow(self.s_star/self.s,2))
        dsdt = -1 * dv
        # xl = position of car in front; l = length of car in front
        self.updateVals(xl, l)
        return self.dvdt
    
    def updateVals(self, xl, l):
        if self.v + self.dvdt*dt < 0:
            self.x = self.x - 0.5 * math.pow(self.v, 2) / self.dvdt
            self.v = 0
            self.dvdt = 0
            return
        self.v += self.dvdt*dt
        self.x += self.v*dt + 0.5*self.dvdt*(dt**2)
        self.s = xl - self.x - l

def formatfour(number):
    num_str = str(number)
    
    num_str = num_str.lstrip('0')
    
    if '.' not in num_str:
        return float(num_str.zfill(4))
    
    if len(num_str) < 4:
        return float(num_str.zfill(4))
    else:
        return float(num_str[:4])

# Simulator

speed_limit = 120 # Speed Limit (km/h)
speed_limit /= 3.6 # Speed Limit conversion (m/s)

# Generate Cars
def start_simulator(numcars):
    x_log = open("x_log", "w")
    v_log = open("v_log", "w")
    dvdt_log = open("dvdt_log", "w")
    sstar_log = open("sstar_log", "w")
    cars_log = open("cars_log", "w")
    log_header = "Time, "
    for i in range(numcars):
        aggressiveness = random.random()*0.5 + 0.7
        acceleration = aggressiveness
        deceleration = aggressiveness*2
        t_headway = 1.8- 0.7/3 + aggressiveness/3
        s_min = random.random()*2 + 2
        car_len = random.random()*2 + 4.5
        chance_truck = 0.1
        if random.random() > 1-chance_truck: # truck
            car_len += 8
            t_headway += 1
            s_min += 2
            deceleration *= 0.75
            vmax = speed_limit * 0.8
        else:
            vmax = speed_limit * 1.1
            vmax += aggressiveness * 3
        
        if i == 0:
            x_init = 0
        else:
            x_init = cars[0].x - cars[0].L - s_min - random.random()*20

        # IDM(x0, v0, T, s0, a, b, v, L):
        cars.insert(0,IDM(x0=x_init, v0=vmax, T=t_headway, s0=s_min, a=acceleration, b=deceleration, v=0, L=car_len))
        log_header += "Car"
        log_header += str(i)
        log_header += ", "
    x_log.write(log_header)
    v_log.write(log_header)
    dvdt_log.write(log_header)
    sstar_log.write(log_header)
    cars_log.write("Car #, x_in, vmax, t_he, smin, leng \n")
    for i, car in enumerate(cars):
        cars_log.write(f"Car {i+1}, {formatfour(car.x)}, {formatfour(car.v0)}, {formatfour(car.T)}, {formatfour(car.s0)}, {formatfour(car.L)} \n")
    cars_log.close()


def print_vehicles():
    for i, car in enumerate(cars):
        print(f"Car {i + 1}: Position = {car.x:.2f} m, Velocity = {car.v:.2f} m/s, Acceleration = {car.dvdt:.2f} m/s2")

def print_vehicle(i, car):
    print(f"Car {i + 1}: Position = {car.x:.2f} m, Velocity = {car.v:.2f} m/s, Acceleration = {car.dvdt:.2f} m/s2")

print_vehicles()

def run_simulator(t):
    # t += dt
    global cars
    cars.sort(key=lambda car: car.x)
    print(f"Simulator Time = {t:.1f}s")
    for i in range(len(cars)):
        car = cars[i]
        if i == len(cars) - 1:
            dvdt = car.calcAcc(car.v, car.x+2000, 5)
        else:
            following_car = cars[i+1]
            dv = car.v - following_car.v
            dvdt = car.calcAcc(dv, following_car.x, following_car.L)
        print_vehicle(i, car);
    return cars


