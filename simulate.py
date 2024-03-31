import simpy
import statistics
import random

wait_time= []
truckMoveTime=6
craneMoveTime=3

class Terminal(object):
    def __init__(self,env, num_berths, num_cranes, num_trucks) -> None:
        self.env =env
        self.berth=simpy.Resource(env, num_berths)
        self.truck=simpy.Resource(env, num_trucks)
        self.crane=simpy.Resource(env, num_cranes)
        

    #vessel takes berth
    def dock_vessel(self, vessel):
        yield self.env.timeout(random.randint(1, 3))

    #move containers from vessel to truck
    def move_to_truck(self, vessel):
        yield self.env.timeout(truckMoveTime)

    #move containers from truck using crane
    def move_from_truck(self, vessel):
        yield self.env.timeout(craneMoveTime)


def vessel_arrival(env, vessel, terminal):
    #arrive at terminal
    arrival_time = env.now

    #get berth
    with terminal.berth.request() as request:
        yield request
        # yield env.process(terminal.dock_vessel(vessel))

    #get truck
    with terminal.truck.request as request:
        yield request
        # yield env.process(terminal.move_to_truck(vessel))

    with terminal.crane.request as request:
        yield request
        #yield env.process(terminal.move_from_truck(vessel))



    