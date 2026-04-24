# Mitigating Relay Attacks in PKE Systems

## Overview
This repository contains the simulation code and academic reports for the project: Mitigating Relay Attacks in Passive Keyless Entry Systems via Distance Bounding Protocols.

This research and simulation were developed for EE 673: Applied Cryptography at the University of North Dakota (UND).

## The Vulnerability
Standard Passive Keyless Entry (PKE) systems use challenge-response cryptography to verify the identity of a key fob. However, these systems are highly vulnerable to Relay Attacks, where an adversary uses RF bridging hardware to extend the physical range of the vehicle's wake-up signal. This tricks the vehicle into unlocking and starting even when the legitimate key fob is located far away (e.g., inside the owner's house).

## The Solution
This project implements a simulation of a Distance Bounding Protocol (based on the Hancke-Kuhn rapid bit-exchange model). By strictly measuring the Round Trip Time (RTT) of the cryptographic exchange at the physical layer, the verifier (vehicle) can estimate the actual distance of the prover (key fob) using the speed of light. If the calculated distance exceeds a strict physical threshold, the authentication is rejected, effectively neutralizing relay hardware delays.

## Repository Contents
- `distance_bounding_sim.py`: A Python script simulating the rapid bit-exchange, RTT measurement, and distance-threshold validation logic.
- `distance_bounding_sim_v2.py`: An enhanced Monte Carlo simulation that runs 500 iterations of legitimate and attack scenarios, generating an analytical scatter plot using `numpy` and `matplotlib`.

## How to Run the Simulation

### Basic Simulation (`distance_bounding_sim.py`)
This simulation is built using Python's standard library and does not require any external dependencies or pip installations.

1. Clone this repository to your local machine.
2. Navigate to the repository directory in your terminal.
3. Execute the script:
   ```bash
   python distance_bounding_sim.py
   ```

The console will output the expected RTT and distance estimations for both a standard authentication scenario and a long-range relay attack.

### Monte Carlo Simulation (`distance_bounding_sim_v2.py`)
This simulation runs a larger set of iterations across a range of distances to graph the results. 

1. Install the required external dependencies:
   ```bash
   pip install numpy matplotlib
   ```
2. Execute the script:
   ```bash
   python distance_bounding_sim_v2.py
   ```
This will output a plot visualizing the relationship between the actual physical distance and the estimated RTT distance.

## Author
Steven Iden - Department of Electrical Engineering, University of North Dakota
