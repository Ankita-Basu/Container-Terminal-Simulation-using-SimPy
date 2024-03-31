# Container-Terminal-Simulation-using-SimPy

This repository contains a simulation of a container terminal using SimPy, a process-based discrete-event simulation framework in Python. The simulation models the arrival of vessels at the terminal, berthing operations, quay crane movements, and truck transportation of containers.

# Features:

- Vessel arrival process: Vessels arrive at the terminal following an exponential distribution with an average of 5 hours between arrivals.
- Berthing operations: There are two available berths at the terminal. If both berths are occupied, incoming vessels join a queue.
- Quay crane operations: Two quay cranes are responsible for unloading containers from vessels. Each crane takes 3 minutes to move one container. The cranes operate independently but cannot serve the same vessel simultaneously.
- Truck transportation: Three trucks transport containers from quay cranes to yard blocks. Each truck takes 6 minutes to drop off a container and return to the quay crane.
- Logging system: The simulation includes a simple logging system that records events such as vessel arrival, berthing, quay crane movements, and truck operations. The log includes the current simulation time.

# Usage:

- Clone the repository and install the required dependencies (`simpy`).
- Run the simulation script (`container_terminal_simulation.py`) and set the simulation time.
- Analyze the output log to understand the performance of the container terminal.

This simulation serves as a tool for studying and optimizing the operations of container terminals, providing insights into vessel waiting times, berthing efficiency, and overall terminal throughput.
