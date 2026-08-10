import matplotlib.pyplot as plt
def calculate_Force(mass,acc):
    return mass*acc
def calculate_velocity(vel_1, acceleration, t):
    return vel_1 + acceleration * t
mass = float(input("Enter Mass (kg): "))
acc = float(input("Enter Acceleration (m/s): "))
force = calculate_Force(mass,acc)
print("Force:",force, "N")
velocities =[]
time = []
vel_1 = float(input("Enter Intial Velocity (ms^-1): "))
acceleration = float(input("Enter acceleration (m/s^2): "))
t = int(input("Enter No. of Seconds (sec): "))
for t in range(1, (t + 1)):
    vel_f = calculate_velocity(vel_1, acceleration, t)
    velocities.append(vel_f)
    time.append(t)
print("Velocities :", velocities)
print("Maximum velocity:", max(velocities), "m/s")
print("Minimum velocity:", min(velocities), "m/s")
print("Average velocity:", sum(velocities) / len(velocities), "m/s")
print("Maximum Time:", max(time), "s")
print("Minimum Time:", min(time), "s")
print("Average Time:", sum(time) / len(time), "s")
def calculate_acceleration(v_initial, v_final, t_initial, t_final):
    return ((v_final-v_initial)/(t_final-t_initial))
acc_from_graph = calculate_acceleration(
    velocities[0],
    velocities[-1],
    time[0],
    time[-1]
)

print("Calculated acceleration:", acc_from_graph, "m/s^2")
plt.plot(time, velocities, marker="o", label="Velocity")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Velocity vs Time")
plt.grid(True)
plt.legend()
plt.show()