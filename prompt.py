import os
import pandas as pd
import numpy as np
from rocketpy import Environment, SolidMotor, Rocket, Flight

from rocketpy import TrapezoidalFins

# Add this before creating the Flight object




# ===============================
# 1. USER INPUT
# ===============================
print("=== Rocket Simulation + INS Tool ===")

eng_file = input("Enter motor .eng file path: ").strip()

if not os.path.exists(eng_file):
    raise FileNotFoundError("Motor file not found!")


# ===============================
# 2. ENVIRONMENT
# ===============================
env = Environment(
    latitude=40.0,
    longitude=44.0,
    elevation=1000
)
# Add a wind profile (Velocity North, Velocity East)
env.set_atmospheric_model(
    type='custom_atmosphere', 
    pressure=101325, 
    temperature=288.15,
    wind_u=0, 
    wind_v=5  # 5 m/s wind blowing towards the East
)


# ===============================
# 3. MOTOR (AUTO LOAD)
# ===============================
motor = SolidMotor(
    thrust_source=eng_file,
    burn_time=3.9,

    dry_mass=1.5,
    dry_inertia=(0.01, 0.01, 0.002),

    grains_center_of_mass_position=0.2,
    center_of_dry_mass_position=0.1,

    grain_number=5,
    grain_separation=0.005,
    grain_density=1815,
    grain_outer_radius=0.033,
    grain_initial_inner_radius=0.015,
    grain_initial_height=0.12,

    nozzle_radius=0.033,
    throat_radius=0.011
)

# ===============================
# 4. ROCKET (GENERIC TEMPLATE)
# ===============================
rocket = Rocket(
    radius=0.0635,
    mass=14,
    inertia=(6.3, 6.3, 0.03),
    center_of_mass_without_motor=0.5,

    power_off_drag=0.5,
    power_on_drag=0.5
)

rocket.add_motor(motor, position=-1.2)

fins = TrapezoidalFins(
    n=4,
    root_chord=0.12,
    tip_chord=0.06,
    span=0.10,
    rocket_radius=0.0635,
    cant_angle=0.5 # This 0.5 degree tilt forces the rocket to SPIN
)
rocket.add_surfaces(fins, positions=-1.5) 

# ===============================
# 5. FLIGHT
# ===============================
flight = Flight(
    rocket=rocket,
    environment=env,
    inclination=85,
    heading=0,
    rail_length=5
)

# ===============================
# 6. EXPORT CSV (FIXED dt)
# ===============================

# Define your desired constant time step (e.g., 0.01s for 100Hz)
dt = 0.01 
t_max = flight.t_final
t_uniform = np.arange(0, t_max, dt)

# Helper to sample at specific times
def get_uniform_data(var):
    # flight variables in RocketPy are usually Functions/Callables
    return var(t_uniform)

df = pd.DataFrame({
    "time": t_uniform,
    "pos_x": get_uniform_data(flight.x),
    "pos_y": get_uniform_data(flight.y),
    "pos_z": get_uniform_data(flight.z),
    "vel_x": get_uniform_data(flight.vx),
    "vel_y": get_uniform_data(flight.vy),
    "vel_z": get_uniform_data(flight.vz),
    "acc_x": get_uniform_data(flight.ax),
    "acc_y": get_uniform_data(flight.ay),
    "acc_z": get_uniform_data(flight.az),
    "omg_p": get_uniform_data(flight.w1),
    "omg_q": get_uniform_data(flight.w2),
    "omg_r": get_uniform_data(flight.w3),
    "orient_0" : get_uniform_data(flight.e0),
    "orient_1" : get_uniform_data(flight.e1),
    "orient_2" : get_uniform_data(flight.e2),
    "orient_3" : get_uniform_data(flight.e3),
})

df.to_csv("rocket_data_fixed_dt.csv", index=False)

print(f"✅ Rocket CSV generated with constant dt = {dt}s!")

flight.plots.trajectory_3d()


