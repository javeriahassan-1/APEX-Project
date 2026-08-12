import csv
import os
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# VEHICLE STATUS
# =========================================================

def check_vehicle_status(vel, temp):

    if temp > 100 and vel >= 80:
        return "CRITICAL"

    elif temp > 100:
        return "OVERHEATING"

    elif vel >= 80:
        return "SPEED_LIMIT"

    else:
        return "NORMAL"


# =========================================================
# SESSION FILENAME
# =========================================================

def get_next_session_filename():

    session_number = 1

    while True:

        filename = (
            f"telemetry_session_{session_number:03d}.csv"
        )

        if not os.path.exists(filename):
            return filename

        session_number += 1


# =========================================================
# GET SAVED TELEMETRY SESSIONS
# =========================================================

def get_saved_sessions():

    sessions = []

    for filename in os.listdir():

        if (
            filename.startswith("telemetry_session_")
            and filename.endswith(".csv")
        ):

            sessions.append(filename)

    sessions.sort()

    return sessions


# =========================================================
# ANOMALY DETECTION
# =========================================================

def detect_anomalies(velocities, times):

    velocity_data = np.array(velocities)

    mean_velocity = np.mean(velocity_data)
    std_velocity = np.std(velocity_data)

    anomaly_times = []
    anomaly_velocities = []

    for index, velocity in enumerate(velocities):

        if abs(velocity - mean_velocity) > 2 * std_velocity:

            anomaly_times.append(times[index])
            anomaly_velocities.append(velocity)

    anomaly_count = len(anomaly_velocities)

    return (
        anomaly_times,
        anomaly_velocities,
        anomaly_count,
        mean_velocity,
        std_velocity
    )


# =========================================================
# LOAD TELEMETRY FROM CSV
# =========================================================

def load_telemetry(filename):

    times = []
    velocities = []
    temperatures = []
    statuses = []

    with open(filename, "r", newline="") as file:

        reader = csv.reader(file)

        next(reader)

        for row in reader:

            times.append(int(row[0]))
            velocities.append(float(row[1]))
            temperatures.append(float(row[2]))
            statuses.append(row[3])

    return (
        times,
        velocities,
        temperatures,
        statuses
    )


# =========================================================
# RUN NEW TELEMETRY SESSION
# =========================================================

def run_new_session():

    times = []
    velocities = []
    temperatures = []
    statuses = []

    time = 0

    end_time = int(
        input("What's the total monitoring time (s)? ")
    )

    # -----------------------------------------------------
    # TELEMETRY COLLECTION
    # -----------------------------------------------------

    while time <= end_time:

        temp = float(
            input("What's the current temperature (°C)? ")
        )

        vel = float(
            input("What's the current velocity (m/s)? ")
        )

        status = check_vehicle_status(
            vel,
            temp
        )

        print("\nAt time:", time, "s")
        print("Velocity:", vel, "m/s")
        print("Temperature:", temp, "°C")
        print("Status:", status)

        # -------------------------------------------------
        # WARNING SYSTEM
        # -------------------------------------------------

        if status == "CRITICAL":

            print(
                "WARNING: Critical condition! "
                "Slow down and stop the vehicle safely."
            )

        elif status == "OVERHEATING":

            print(
                "WARNING: Temperature is too high."
            )

        elif status == "SPEED_LIMIT":

            print(
                "WARNING: Speed limit exceeded."
            )

        else:

            print(
                "Vehicle operating normally."
            )

        # -------------------------------------------------
        # STORE TELEMETRY
        # -------------------------------------------------

        times.append(time)
        velocities.append(vel)
        temperatures.append(temp)
        statuses.append(status)

        time += 1

    # -----------------------------------------------------
    # SAVE NEW SESSION TO CSV
    # -----------------------------------------------------

    filename = get_next_session_filename()

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Time",
            "Velocity",
            "Temperature",
            "Status"
        ])

        for time, velocity, temperature, status in zip(
            times,
            velocities,
            temperatures,
            statuses
        ):

            writer.writerow([
                time,
                velocity,
                temperature,
                status
            ])

    print(
        "\nTelemetry saved successfully as:",
        filename
    )

    return (
        times,
        velocities,
        temperatures,
        statuses
    )


# =========================================================
# ANALYZE TELEMETRY
# =========================================================

def analyze_telemetry(
    times,
    velocities,
    temperatures,
    statuses
):

    velocity_data = np.array(velocities)
    temperature_data = np.array(temperatures)

    # -----------------------------------------------------
    # VELOCITY ANALYSIS
    # -----------------------------------------------------

    (
        anomaly_times,
        anomaly_velocities,
        anomaly_count,
        mean_velocity,
        std_velocity

    ) = detect_anomalies(
        velocities,
        times
    )

    # -----------------------------------------------------
    # TEMPERATURE ANALYSIS
    # -----------------------------------------------------

    mean_temperature = np.mean(
        temperature_data
    )

    std_temperature = np.std(
        temperature_data
    )

    # -----------------------------------------------------
    # EVENT COUNTS
    # -----------------------------------------------------

    critical_count = statuses.count(
        "CRITICAL"
    )

    overheating_count = statuses.count(
        "OVERHEATING"
    )

    speed_count = statuses.count(
        "SPEED_LIMIT"
    )

    normal_count = statuses.count(
        "NORMAL"
    )

    # -----------------------------------------------------
    # TELEMETRY REPORT
    # -----------------------------------------------------

    print(
        "\n========== APEX TELEMETRY REPORT =========="
    )

    print("\n--- Vehicle Events ---")

    print("Critical Events:", critical_count)
    print("Overheating Events:", overheating_count)
    print("Speed-limit Events:", speed_count)
    print("Normal Events:", normal_count)

    print("\n--- Velocity Analysis ---")

    print(
        "Average velocity:",
        mean_velocity,
        "m/s"
    )

    print(
        "Velocity standard deviation:",
        std_velocity,
        "m/s"
    )

    print(
        "Anomaly count:",
        anomaly_count
    )

    print("\n--- Temperature Analysis ---")

    print(
        "Average temperature:",
        mean_temperature,
        "°C"
    )

    print(
        "Temperature standard deviation:",
        std_temperature,
        "°C"
    )

    print("\n--- Anomaly Data ---")

    print(
        "Anomaly times:",
        anomaly_times
    )

    print(
        "Anomaly velocities:",
        anomaly_velocities
    )

    # -----------------------------------------------------
    # VELOCITY GRAPH
    # -----------------------------------------------------

    plt.figure()

    plt.plot(
        times,
        velocities,
        marker="o",
        label="Velocity"
    )

    plt.scatter(
        anomaly_times,
        anomaly_velocities,
        marker="x",
        s=100,
        label="Anomaly"
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")

    plt.title(
        "APEX — Vehicle Velocity vs Time"
    )

    plt.grid(True)
    plt.legend()

    plt.show()

    # -----------------------------------------------------
    # TEMPERATURE GRAPH
    # -----------------------------------------------------

    plt.figure()

    plt.plot(
        times,
        temperatures,
        marker="o",
        label="Temperature"
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°C)")

    plt.title(
        "APEX — Vehicle Temperature vs Time"
    )

    plt.grid(True)
    plt.legend()

    plt.show()


# =========================================================
# APEX MAIN MENU
# =========================================================

print("\n========== APEX ==========")

print("1. Run New Telemetry Session")
print("2. Analyze Previous Telemetry")

choice = input("Select an option: ")


# =========================================================
# OPTION 1 — NEW SESSION
# =========================================================

if choice == "1":

    (
        times,
        velocities,
        temperatures,
        statuses

    ) = run_new_session()

    analyze_telemetry(
        times,
        velocities,
        temperatures,
        statuses
    )

# =========================================================
# OPTION 2 — PREVIOUS SESSION
# =========================================================
elif choice == "2":

    sessions = get_saved_sessions()

    if len(sessions) == 0:

        print("\nNo saved telemetry sessions found.")

    else:

        print("\n========== SAVED TELEMETRY SESSIONS ==========")

        for index, filename in enumerate(
            sessions,
            start=1
        ):

            print(
                index,
                ".",
                filename
            )

        session_choice = int(
            input(
                "\nSelect a session number: "
            )
        )

        if (
            session_choice >= 1
            and session_choice <= len(sessions)
        ):

            filename = sessions[
                session_choice - 1
            ]

            print(
                "\nLoading:",
                filename
            )

            (
                times,
                velocities,
                temperatures,
                statuses

            ) = load_telemetry(
                filename
            )

            analyze_telemetry(
                times,
                velocities,
                temperatures,
                statuses
            )

        else:

            print(
                "\nInvalid session number."
            )