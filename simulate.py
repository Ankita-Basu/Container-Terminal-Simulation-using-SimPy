import simpy
import statistics
import random

wait_time= []
truckMoveTime=6
craneMoveTime=3

vesselArivalTime=5 * 60 

class Terminal(object):
    def __init__(self,env, num_berths, num_cranes, num_trucks) -> None:
        self.env =env
        self.berth=simpy.Resource(env, num_berths)
        self.crane=simpy.Resource(env, num_cranes)
        self.truck=simpy.Resource(env, num_trucks)
        

    #vessel takes berth
    def dock_vessel(self, vessel):
        yield self.env.timeout(random.randint(1, 3))

    #move containers from truck using crane
    def move_by_crane(self, vessel):
        yield self.env.timeout(craneMoveTime)

    #move containers from vessel to truck
    def move_to_truck(self, vessel):
        yield self.env.timeout(truckMoveTime)

    


def vessel_arrival(env, vessel, terminal):
    #arrive at terminal
    arrival_time = env.now

    #get berth
    with terminal.berth.request() as request:
        yield request
        print(f"Vessel {vessel} docked at berth at {env.now} minutes")
        yield env.process(terminal.dock_vessel(vessel))

    #vessel gets download by crane
    with terminal.crane.request() as request:
        yield request
        print(f"Vessel {vessel} unloaded by crane at {env.now} minutes")
        yield env.process(terminal.move_by_crane(vessel))

    #get truck
    with terminal.truck.request() as request:
        yield request
        print(f"Vessel {vessel} containers moved by truck at {env.now} minutes")
        yield env.process(terminal.move_to_truck(vessel))

    
    wait_time.append(env.now - arrival_time)


def run_terminal(env, num_berths, num_cranes , num_trucks):
    terminal = Terminal(env, num_berths, num_cranes, num_trucks)

    for vessel in range(2):
        env.process(vessel_arrival(env, vessel, terminal))

    while True:
        yield env.timeout(vesselArivalTime)
        vessel += 1
        env.process(vessel_arrival(env, vessel, terminal))


def calculate_wait_time(wait_time):
    average_wait= statistics.mean(wait_time)
    minutes, frac_minutes= divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)

def get_input():
    #given
    num_berth = 2
    num_cane = 2
    num_truck= 3 
    SIMULATION_TIME = int(input("Give simulation run time in minutes: "))

    params = [num_berth, num_cane, num_truck,SIMULATION_TIME]

    return params

def main():
    random.seed(42)
    num_berth, num_cane, num_truck, SIMULATION_TIME = get_input()

    

    env = simpy.Environment()
    env.process(run_terminal(env, num_berth, num_cane, num_truck))
    env.run(until=SIMULATION_TIME)

    mins, secs = calculate_wait_time(wait_time)

    print(f"Average wait time is {mins} minutes and {secs} seconds.")


if __name__ == '__main__':
    main()





    