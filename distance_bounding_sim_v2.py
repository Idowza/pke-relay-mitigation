import random
import numpy as np
import matplotlib.pyplot as plt

# --- SYSTEM CONSTANTS ---
SPEED_OF_LIGHT = 299792458  # c in meters per second
THRESHOLD_DISTANCE = 2.0    # d_max in meters (maximum allowed distance to unlock)
NUM_BITS = 64               # Number of rapid bit exchanges
T_PROC_BASE = 1e-9          # Base processing time: 1 nanosecond

def precomputation_phase():
    """Simulates the cryptographic pre-computation."""
    reg_0 = np.random.randint(2, size=NUM_BITS)
    reg_1 = np.random.randint(2, size=NUM_BITS)
    return reg_0, reg_1

def rapid_exchange_phase(reg_0, reg_1, true_distance, attacker_delay=0.0):
    """Simulates the physical layer exchange with realistic signal jitter."""
    time_of_flight_one_way = true_distance / SPEED_OF_LIGHT
    total_time_recorded = 0.0

    for i in range(NUM_BITS):
        # Add realistic hardware jitter (Standard deviation of 0.5 nanoseconds)
        jitter = np.random.normal(0, 0.5e-9) 
        actual_t_proc = max(0, T_PROC_BASE + jitter)

        # RTT = (Trip to Fob) + (Processing Time) + (Trip to Car) + (Relay Delay)
        bit_rtt = (time_of_flight_one_way * 2) + actual_t_proc + attacker_delay
        total_time_recorded += bit_rtt

    return total_time_recorded

def run_monte_carlo():
    print("Running Monte Carlo Simulation (500 iterations)...")
    
    # Generate random test distances between 0.1m and 100m
    test_distances = np.random.uniform(0.1, 100.0, 500)
    
    normal_results_dist = []
    normal_results_est = []
    
    attack_results_dist = []
    attack_results_est = []

    for dist in test_distances:
        # --- Scenario A: Normal Authentication ---
        reg0, reg1 = precomputation_phase()
        total_time_norm = rapid_exchange_phase(reg0, reg1, dist, attacker_delay=0.0)
        est_dist_norm = SPEED_OF_LIGHT * ((total_time_norm / NUM_BITS) - T_PROC_BASE) / 2
        
        normal_results_dist.append(dist)
        normal_results_est.append(est_dist_norm)

        # --- Scenario B: Relay Attack ---
        hardware_delay = 1.5e-6 
        total_time_atk = rapid_exchange_phase(reg0, reg1, dist, attacker_delay=hardware_delay)
        est_dist_atk = SPEED_OF_LIGHT * ((total_time_atk / NUM_BITS) - T_PROC_BASE) / 2
        
        attack_results_dist.append(dist)
        attack_results_est.append(est_dist_atk)

    return normal_results_dist, normal_results_est, attack_results_dist, attack_results_est

def plot_results(n_dist, n_est, a_dist, a_est):
    print("Generating Plot...")
    plt.figure(figsize=(10, 6))
    
    # Plot the simulated data
    plt.scatter(n_dist, n_est, color='blue', alpha=0.6, label='Legitimate Authentication', s=15)
    plt.scatter(a_dist, a_est, color='red', alpha=0.6, label='Relay Attack (1.5$\mu$s latency)', s=15)
    
    # Plot the Threshold Zones
    plt.axhline(y=THRESHOLD_DISTANCE, color='green', linestyle='--', linewidth=2, label='d_max Threshold (2.0m)')
    
    # Shade the "Access Granted" area
    plt.fill_between([0, 100], 0, THRESHOLD_DISTANCE, color='green', alpha=0.1)

    # Formatting the Graph for IEEE standards
    plt.title('Simulated Distance Bounding: Actual vs. Estimated Distance', fontsize=14, fontweight='bold')
    plt.xlabel('Actual Physical Distance of Key Fob (meters)', fontsize=12)
    plt.ylabel('Distance Estimated by Verifier via RTT (meters)', fontsize=12)
    plt.xlim(0, 100)
    
    # [FIXED LINE] Scale Y axis to fit the highest red dots (attacker data)
    plt.ylim(0, max(max(a_est), max(n_est)) * 1.1) 
    
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Save the figure to be included in your LaTeX document
    plt.tight_layout()
    plt.savefig('rtt_simulation_results_fixed.jpg', dpi=300)
    plt.show()
    print("Plot saved as 'rtt_simulation_results_fixed.jpg'")

if __name__ == "__main__":
    n_dist, n_est, a_dist, a_est = run_monte_carlo()
    plot_results(n_dist, n_est, a_dist, a_est)