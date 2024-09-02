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

# Expand the star list with additional stars for extended analysis
hip_numbers = [11767, 72607, 65378, 67301, 85819, 68756, 10234, 88972, 54872]  # Additional stars for analysis
star_names = ['Polaris', 'Beta UMi', 'Zeta UMa', 'Eta UMa', 'Thuban', 'Gamma Draconis', 'Alpha Boo', 'Beta Leo', 'Alpha Gem']
stars = {name: Star.from_dataframe(df.loc[hip]) for name, hip in zip(star_names, hip_numbers)}

# Define an extended time range (4000 BC to 1000 BC)
years = np.arange(-4000, -1000, 50)  # Simulating every 50 years

# Store results for plotting
star_distances = {name: [] for name in star_names}

# Calculate the angular distance from the NCP for each star over the extended period
for year in years:
    time = ts.utc(year, 2, 20, 21, 0, 0)
    observer = planets['earth'] + giza

    for name, star in stars.items():
        astrometric = observer.at(time).observe(star)
        alt, az, d = astrometric.apparent().altaz()
        ncp_distance = 90 - alt.degrees
        star_distances[name].append(ncp_distance)

# Plotting results
plt.figure(figsize=(15, 8))
for name, distances in star_distances.items():
    plt.plot(years, distances, label=name)

plt.xlabel('Year (BC)')
plt.ylabel('Angular Distance from NCP (degrees)')
plt.title('Angular Distance of Stars from North Celestial Pole Over Time')
plt.gca().invert_xaxis()
plt.legend()
plt.grid()
plt.savefig('Extended_Star_Analysis.png', dpi=300, bbox_inches='tight')
plt.show()
