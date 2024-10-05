import calcs as c
import os
import json
import math
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

data_path = os.path.join(os.getcwd(), 'data')

with open (os.path.join(data_path, 'keplar.json'), 'r') as f:
    data = json.load(f) 

planets = ["Mercury" , "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

def_delta_t = 1
max_keyframes = 500

grav_constant = 6.674e-11
sun_mass = 1.989e30

pos_data = {}

for planet in planets: 
    positions = []
    planet_data = data[planet]
    a = planet_data["semi_major_axis"]
    e = planet_data["eccentricity"]
    i = planet_data["inclination"]
    def_mean_long = planet_data["mean_long"]
    mean_long_change = planet_data["mean_long_change"]
    long_peri = planet_data["long_peri"]
    long_node = planet_data["long_node"]
    orbital_time = 2 * math.pi *math.sqrt(math.pow(a*1.496e11,3)/(grav_constant*sun_mass))/86400
    delta_t = def_delta_t
    n_keyframes = math.floor(orbital_time/delta_t)
    if n_keyframes > max_keyframes:
        n_keyframes = max_keyframes
        delta_t = orbital_time/n_keyframes

    arg_peri = c.arg_peri(long_peri, long_node)

    T = c.convert_to_jed(5,10,2024,0)
    T = c.get_T(T)

    for _ in range(n_keyframes):
        mean_long = c.mean_long(def_mean_long, mean_long_change, T)
        M = c.mean_anomaly(mean_long, long_peri)
        E = c.newton_raphson_kepler(M, e)
        pos = c.get_orbital_pos(E,e,a)
        pos = c.get_relative_pos(pos, i, long_node, arg_peri)

        positions.append(pos)

        if planet == "Earth":
            print(f"Step {_+1}/{n_keyframes}")
            print(f"Mean Longitude: {mean_long}, Mean Anomaly: {M}, Eccentric Anomaly: {E}")
            print(f"Position: {pos}\n")
        T += (delta_t /(365.2 * 100))
    
    pos_data[planet] = {"positions": positions, "relative_to": "Sun", "time_scale": delta_t}

    with open (os.path.join(os.getcwd(), 'data', 'orbits.json'), 'w') as f:
        f.write(json.dumps(pos_data, indent=4))

#print(pos_data)


# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')

# # Define colors for each planet for easier visualization
# colors = {
#     "Mercury": 'gray', "Venus": 'black', "Earth": 'blue', "Mars": 'red',
#     "Jupiter": 'orange', "Saturn": 'gold', "Uranus": 'cyan', "Neptune": 'purple'
# }

    #Plot the orbits
# for planet, data in pos_data.items():
#     # Extract the x, y, z coordinates of each keyframe position
#     x_vals = [pos[0] for pos in data["positions"]]
#     y_vals = [pos[1] for pos in data["positions"]]
#     z_vals = [pos[2] for pos in data["positions"]]

#     # Plot each planet's orbit
#     ax.scatter(x_vals, y_vals, z_vals, label=planet, s=10, color=colors[planet])
    
#     #Mark the starting position
#     ax.scatter(x_vals[0], y_vals[0], z_vals[0], color=colors[planet], s=30)

# x_vals = [pos[0] for pos in pos_data["Earth"]["positions"]]
# y_vals = [pos[1] for pos in pos_data["Earth"]["positions"]]
# z_vals = [pos[2] for pos in pos_data["Earth"]["positions"]]
# ax.scatter(x_vals, y_vals, z_vals, label = "Earth", s=10, color=colors["Earth"])

# x_vals = [pos[0] for pos in pos_data["Venus"]["positions"]]
# y_vals = [pos[1] for pos in pos_data["Venus"]["positions"]]
# z_vals = [pos[2] for pos in pos_data["Venus"]["positions"]]
# ax.scatter(x_vals, y_vals, z_vals, label = "Venus", s=10, color=colors["Venus"])

# x_vals = [pos[0] for pos in pos_data["Mercury"]["positions"]]
# y_vals = [pos[1] for pos in pos_data["Mercury"]["positions"]]
# z_vals = [pos[2] for pos in pos_data["Mercury"]["positions"]]
# ax.scatter(x_vals, y_vals, z_vals, label = "Mercury", s=10, color=colors["Mercury"])


# # Mark the Sun at the origin
# ax.scatter(0, 0, 0, color='orange', s=100, label='Sun')

# # Set plot labels
# ax.set_xlabel("X (AU)")
# ax.set_ylabel("Y (AU)")
# ax.set_zlabel("Z (AU)")
# ax.set_title("Planetary Orbits")
# ax.legend(loc="upper right")

# # Show plot
# plt.show()

# import math
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.animation import FuncAnimation

# Sample data creation (replace this with your actual data)
# Simulating positions for Venus over 18 steps
 # Replace with actual positions

# Set up the figure and axis
# fig, ax = plt.subplots()
# ax.set_xlim(-1.5, 1.5)  # Adjust limits based on your orbital data
# ax.set_ylim(-1.5, 1.5)
# ax.set_title("Venus Orbit Animation")
# ax.set_xlabel("X Position (AU)")
# ax.set_ylabel("Y Position (AU)")
# line, = ax.plot([], [], 'bo')  # 'bo' for blue points

# # Initialize the plot
# def init():
#     line.set_data([], [])
#     return line,

# # Update function for the animation
# def update(frame):
#     x_data = [pos[0] for pos in pos_data["Venus"]["positions"][:frame + 1]]
#     y_data = [pos[1] for pos in pos_data["Venus"]["positions"][:frame + 1]]
#     line.set_data(x_data, y_data)
#     return line,

# # Create the animation
# ani = FuncAnimation(fig, update, frames=len(positions), init_func=init,
#                     interval=100, blit=True)

# # Show the plot
# plt.show()
