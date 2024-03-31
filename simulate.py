import simpy
import statistics
import random

wait_time= []
#per container
truckMoveTime=6
craneMoveTime=3

vesselArivalTime=5 * 60 
numContainerPerVessel=150


class Terminal(object):
    def __init__(self,env, num_berths, num_cranes, num_trucks) -> None:
        self.env =env
        # self.berth=simpy.Resource(env, num_berths)
        self.berth=[simpy.Resource(env) for _ in range(num_berths)]
        self.crane=[simpy.Resource(env)  for _ in range(num_cranes)]
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

    


def vessel_arrival(env, vessel, terminal, num_berths, num_cranes,num_trucks):
    #arrive at terminal
    arrival_time = env.now
    print(f"Vessel {vessel} arrived at terminal at {env.now} minutes")

    #get berth
    with terminal.berth[vessel % num_berths].request() as request:
        yield request
        print(f"Vessel {vessel} docked at berth {vessel % num_berths} at {env.now} minutes")
        yield env.process(terminal.dock_vessel(vessel))

    #vessel-containers gets download by crane
    for _ in range(numContainerPerVessel):
        with terminal.crane[vessel % num_cranes].request() as request:
            yield request
            print(f"Vessel {vessel} unloaded by crane {vessel % num_cranes} at {env.now} minutes")
            yield env.process(terminal.move_by_crane(vessel))

    #get truck
    with terminal.truck.request() as request:
        yield request
        print(f"Vessel {vessel} containers moved by truck at {env.now} minutes")
        yield env.process(terminal.move_to_truck(vessel))

    
    wait_time.append(env.now - arrival_time)


def run_terminal(env, num_berths, num_cranes , num_trucks):
    terminal = Terminal(env, num_berths, num_cranes, num_trucks)

    for vessel in range(1,3):
        env.process(vessel_arrival(env, vessel, terminal, num_berths, num_cranes, num_trucks ))

    while True:
        #exponential distribution of average 5hrs
        yield env.timeout(random.expovariate(1/vesselArivalTime))
        vessel += 1
        env.process(vessel_arrival(env, vessel, terminal, num_berths, num_cranes, num_trucks))


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





    