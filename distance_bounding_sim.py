import random

# --- SYSTEM CONSTANTS ---
SPEED_OF_LIGHT = 299792458  # c in meters per second
THRESHOLD_DISTANCE = 2.0    # d_max in meters (maximum allowed distance to unlock)
NUM_BITS = 64               # Number of rapid bit exchanges in the Hancke-Kuhn protocol

# Prover processing time (t_proc). 
# In Hancke-Kuhn, this is near-zero because the crypto is pre-computed.
T_PROC = 1e-9               # 1 nanosecond

def precomputation_phase():
    """
    Simulates the slow cryptographic phase.
    The Fob and Car use their secret key to generate two 64-bit registers.
    """
    register_0 = [random.choice([0, 1]) for _ in range(NUM_BITS)]
    register_1 = [random.choice([0, 1]) for _ in range(NUM_BITS)]
    return register_0, register_1

def rapid_exchange_phase(register_0, register_1, true_distance, attacker_delay=0.0):
    """
    Simulates the physical layer timing of the rapid bit exchange.
    Returns the total time taken for the exchange and the validity of the responses.
    """
    # Calculate base Time of Flight (ToF) based on physics
    time_of_flight_one_way = true_distance / SPEED_OF_LIGHT
    
    total_time_recorded = 0.0
    correct_responses = 0

    for i in range(NUM_BITS):
        # 1. Car sends a challenge bit
        challenge_bit = random.choice([0, 1])
        
        # 2. Fob instantly replies based on the challenge bit
        if challenge_bit == 0:
            response_bit = register_0[i]
        else:
            response_bit = register_1[i]
            
        # Verify the Fob sent the correct bit (Standard Crypto Check)
        if response_bit == (register_0[i] if challenge_bit == 0 else register_1[i]):
            correct_responses += 1

        # 3. Car records the RTT for this specific bit
        # RTT = (Trip to Fob) + (Processing Time) + (Trip to Car) + (Attacker Hardware Delay)
        bit_rtt = (time_of_flight_one_way) + T_PROC + (time_of_flight_one_way) + attacker_delay
        total_time_recorded += bit_rtt

    return total_time_recorded, correct_responses

def run_simulation(scenario_name, true_distance, is_attack=False):
    print(f"\n[{scenario_name.upper()}]")
    print(f"Actual Physical Distance: {true_distance}m")
    
    # Define attacker latency (e.g., analog-to-digital conversion, transmission)
    # Even advanced SDRs introduce a few microseconds of delay.
    relay_delay = 5e-6 if is_attack else 0.0 
    if is_attack:
        print(f"Adversary Relay Latency: {relay_delay * 1e6} microseconds per bit")

    # Phase 1: Pre-computation (The Standard Crypto)
    reg0, reg1 = precomputation_phase()

    # Phase 2: The Physical Measurement
    total_time, correct_bits = rapid_exchange_phase(reg0, reg1, true_distance, relay_delay)

    # Phase 3: The Verification (System Model Equations)
    # Calculate average RTT per bit
    avg_rtt = total_time / NUM_BITS
    
    # Equation 2: d_est = c * (t_end - t_start - t_proc) / 2
    estimated_distance = SPEED_OF_LIGHT * (avg_rtt - T_PROC) / 2

    # Equation 3: (R' == R) AND (d_est <= d_max)
    crypto_valid = (correct_bits == NUM_BITS)
    distance_valid = (estimated_distance <= THRESHOLD_DISTANCE)

    print("-" * 30)
    print(f"Cryptographic Check: {'PASS' if crypto_valid else 'FAIL'} ({correct_bits}/{NUM_BITS} bits correct)")
    print(f"Measured Avg RTT:    {avg_rtt * 1e9:.2f} ns")
    print(f"Calculated Distance: {estimated_distance:.2f} meters")
    print("-" * 30)
    
    if crypto_valid and distance_valid:
        print(">>> ACCESS GRANTED: Proximity and Identity Verified. <<<")
    elif crypto_valid and not distance_valid:
        print(">>> ACCESS DENIED: Relay Attack Detected! Distance Bound Exceeded. <<<")
    else:
        print(">>> ACCESS DENIED: Invalid Cryptographic Key. <<<")

if __name__ == "__main__":
    print("=== PKE Distance Bounding Simulation ===")
    
    # Scenario 1: Normal Operation (Owner is standing next to the car)
    run_simulation(
        scenario_name="Normal Authentication", 
        true_distance=1.0, 
        is_attack=False
    )
    
    # Scenario 2: Standard Relay Attack (Owner is 50m away in their house, attackers bridge the gap)
    run_simulation(
        scenario_name="Relay Attack", 
        true_distance=50.0, 
        is_attack=True
    )