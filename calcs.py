import math

# calculates the argument of perihelion
def arg_peri(long_peri, long_node):
    return (long_peri - long_node) % 360

def convert_to_jed(day, month, year, hour):
    # Adjust month and year for January and February
    if month < 3:
        month += 12
        year -= 1

    # Calculate Julian Day
    A = year // 100
    B = 2 - A + A // 4
    
    JD = (math.floor(365.25 * (year + 4716)) +
          math.floor(30.6001 * (month + 1)) +
          day + B - 1524.5)

    # Convert to Julian Ephemeris Date
    JED = JD + (hour / 24)

    return JED

def get_T(t):
    return (t - 2451545.0) / 36525

# calculates the adjusted mean longitude corresponding to J2000
def mean_long(mean_long, mean_long_change, T):
    return (mean_long + mean_long_change * T) % 360

# calculates the mean anomaly
def mean_anomaly(mean_long, long_peri):
    M = mean_long - long_peri
    M = M % 360
    if M > 180:
        M -= 360
    return deg_to_rad(M)

# converts an angle from radians to degrees
def rad_to_deg(angle):
    return angle * (180 / math.pi)

def deg_to_rad(deg):
    return deg * (math.pi / 180)

# finds a close approximation for E given M and e, using the Newton-Raphson method
def newton_raphson_kepler(M, e, tol=1e-10, max_iter=100):
    if e < 0.8:
        E = M
    else:
        E = math.pi

    for _ in range(max_iter):
        f_E = E - e * math.sin(E) - M
        f_prime_E = 1 - e * math.cos(E)
        E_new = E - (f_E / f_prime_E)

        if abs(E_new - E) < tol:
            return E_new

        E = E_new

    return E

# gets the position relative to the orbital plane (2-d)
def get_orbital_pos(E, e, a):
    x = a * (math.cos(E) - e)
    y = a * (math.sqrt(1 - e * e)) * math.sin(E)
    return [x, y, 0]

# gets the position relative to the equatorial plane and the equinox (3-d)
def get_relative_pos(orbital_pos, i, long_node, arg_peri):
    i = deg_to_rad(i)
    long_node = deg_to_rad(long_node)
    arg_peri = deg_to_rad(arg_peri)
    
    x = (math.cos(arg_peri) * math.cos(long_node) - 
         math.sin(arg_peri) * math.sin(long_node) * math.cos(i)) * orbital_pos[0]
    x += (-math.sin(arg_peri) * math.cos(long_node) - 
           math.cos(arg_peri) * math.sin(long_node) * math.cos(i)) * orbital_pos[1]

    y = (math.cos(arg_peri) * math.sin(long_node) + 
         math.sin(arg_peri) * math.cos(long_node) * math.cos(i)) * orbital_pos[0]
    y += (-math.sin(arg_peri) * math.sin(long_node) + 
           math.cos(arg_peri) * math.cos(long_node) * math.cos(i)) * orbital_pos[1]

    z = (math.sin(arg_peri) * math.sin(i) * orbital_pos[0] + 
         math.cos(arg_peri) * math.sin(i) * orbital_pos[1])

    return [x, y, z]
