from skyfield.api import Star, load, Topos
from skyfield.data import hipparcos
import matplotlib.pyplot as plt
import numpy as np

# Load star catalog and ephemeris data
with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)
ts = load.timescale()
planets = load('de406.bsp')  # Use DE406 for extended date range

# Define Giza's location
giza = Topos('29.9792 N', '31.1342 E')

# HIP numbers for the stars of interest
hip_numbers = [11767, 72607, 65378, 67301, 85819, 68756]  # Adding Thuban and other relevant stars
star_names = ['Polaris', 'Beta UMi', 'Zeta UMa', 'Eta UMa', 'Thuban', 'Gamma Draconis']
stars = {name: Star.from_dataframe(df.loc[hip]) for name, hip in zip(star_names, hip_numbers)}

# Define time range to explore (e.g., 2600 BC to 2400 BC in 50-year steps)
years = [-2600, -2550, -2500, -2450]
fig, axs = plt.subplots(2, 2, figsize=(18, 10))
axs = axs.flatten()

# Plotting for each specified year
for ax, year in zip(axs, years):
    time = ts.utc(year, 2, 20, 21, 0, 0)
    observer = planets['earth'] + giza

    ax.set_title(f"Giza - North Horizon - February {abs(year)} BC")
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_xlabel('Azimuth (East to West)')
    ax.set_ylabel('Altitude')

    for name, star in stars.items():
        astrometric = observer.at(time).observe(star)
        alt, az, d = astrometric.apparent().altaz()
        
        # Calculate and display angular distance from the North Celestial Pole (NCP)
        ncp_distance = 90 - alt.degrees
        ax.plot(az.radians, alt.radians, 'o', label=f"{name} ({ncp_distance:.2f}° from NCP)")
        ax.annotate(name, (az.radians, alt.radians), textcoords="offset points", xytext=(0, 10), ha='center')
        
    ax.legend(loc='upper left', fontsize='small')
    ax.grid(True)

plt.tight_layout()

# Save the figure as a high-resolution image
plt.savefig('Giza_North_Horizon_Star_Alignment.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
