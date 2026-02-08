import matplotlib.pyplot as plt
from simulation import PandemicSimulation

def visualize_simulation():
    # Run simulation
    population_size = 1000
    sim = PandemicSimulation(population_size=population_size, 
                             starting_immunity=1, 
                             starting_infecters=5, 
                             days_contagious=14, 
                             lockdown_day=20, 
                             mask_day=100)
    
    print("Running simulation...")
    daily_contagious = sim.run_simulation(days=100)
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(daily_contagious, label='Contagious People')
    plt.axvline(x=20, color='r', linestyle='--', label='Lockdown Start')
    plt.xlabel('Day')
    plt.ylabel('Number of Contagious People')
    plt.title(f'Pandemic Simulation (Pop: {population_size})')
    plt.legend()
    plt.grid(True)
    
    output_file = 'pandemic_plot.png'
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    visualize_simulation()
