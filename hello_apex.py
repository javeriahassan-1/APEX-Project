import csv
import os
import numpy as np
import matplotlib.pyplot as plt


def get_valid_float(prompt, allow_negative=True):

    while True:

        try:

            value = float(input(prompt))

            if not allow_negative and value < 0:

                print(
                    "Invalid input. "
                    "Please enter a non-negative value."
                )

                continue

            return value

        except ValueError:

            print(
                "Invalid input. "
                "Please enter a numerical value."
            )


def get_valid_int(prompt, minimum=None, maximum=None):

    while True:

        try:

            value = int(input(prompt))

            if (
                minimum is not None
                and value < minimum
            ):

                print(
                    f"Invalid input. "
                    f"Please enter a value of at least "
                    f"{minimum}."
                )

                continue

            if (
                maximum is not None
                and value > maximum
            ):

                print(
                    f"Invalid input. "
                    f"Please enter a value no greater than "
                    f"{maximum}."
                )

                continue

            return value

        except ValueError:

            print(
                "Invalid input. "
                "Please enter a whole number."
            )


def check_vehicle_status(vel, temp):

    if temp > 100 and vel >= 80:
        return "CRITICAL"

    elif temp > 100:
        return "OVERHEATING"

    elif vel >= 80:
        return "SPEED_LIMIT"

    return "NORMAL"


def get_next_session_filename():

    session_number = 1

    while True:

        filename = (
            f"telemetry_session_{session_number:03d}.csv"
        )

        if not os.path.exists(filename):
            return filename

        session_number += 1


def get_available_sessions():

    sessions = []

    for filename in os.listdir():

        if (
            filename.startswith("telemetry_session_")
            and filename.endswith(".csv")
        ):

            sessions.append(filename)

    sessions.sort()

    return sessions


def detect_anomalies(velocities, times):

    velocity_data = np.array(velocities)

    mean_velocity = np.mean(velocity_data)

    std_velocity = np.std(velocity_data)

    anomaly_times = []

    anomaly_velocities = []

    for index, velocity in enumerate(velocities):

        if abs(
            velocity - mean_velocity
        ) > 2 * std_velocity:

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


def detect_temperature_trend(temperatures):

    increasing_count = 0

    decreasing_count = 0

    stable_count = 0

    tolerance = 2

    for index in range(
        1,
        len(temperatures)
    ):

        previous = temperatures[index - 1]

        current = temperatures[index]

        if current > previous + tolerance:

            increasing_count += 1

        elif current < previous - tolerance:

            decreasing_count += 1

        else:

            stable_count += 1

    if (
        increasing_count > decreasing_count
        and increasing_count > stable_count
    ):

        return "INCREASING"

    elif (
        decreasing_count > increasing_count
        and decreasing_count > stable_count
    ):

        return "DECREASING"

    elif (
        stable_count > increasing_count
        and stable_count > decreasing_count
    ):

        return "STABLE"

    return "FLUCTUATING"


def detect_velocity_trend(velocities):

    increasing_count = 0

    decreasing_count = 0

    stable_count = 0

    tolerance = 2

    for index in range(
        1,
        len(velocities)
    ):

        previous = velocities[index - 1]

        current = velocities[index]

        if current > previous + tolerance:

            increasing_count += 1

        elif current < previous - tolerance:

            decreasing_count += 1

        else:

            stable_count += 1

    if (
        increasing_count > decreasing_count
        and increasing_count > stable_count
    ):

        return "INCREASING"

    elif (
        decreasing_count > increasing_count
        and decreasing_count > stable_count
    ):

        return "DECREASING"

    elif (
        stable_count > increasing_count
        and stable_count > decreasing_count
    ):

        return "STABLE"

    return "FLUCTUATING"


def calculate_risk_score(
    critical_count,
    overheating_count,
    speed_count,
    anomaly_count
):

    risk_score = 0

    risk_score += critical_count * 30

    risk_score += overheating_count * 20

    risk_score += speed_count * 10

    risk_score += anomaly_count * 15

    if risk_score > 100:

        risk_score = 100

    return risk_score


def assess_vehicle_condition(
    risk_score,
    temperature_trend,
    velocity_trend
):

    if risk_score <= 20:

        condition = "HEALTHY"

    elif risk_score <= 50:

        condition = "CAUTION"

    elif risk_score <= 75:

        condition = "WARNING"

    else:

        condition = "CRITICAL"

    if (
        temperature_trend == "INCREASING"
        and condition == "HEALTHY"
    ):

        condition = "CAUTION"

    elif (
        temperature_trend == "INCREASING"
        and condition == "CAUTION"
    ):

        condition = "WARNING"

    elif (
        temperature_trend == "FLUCTUATING"
        and condition == "HEALTHY"
    ):

        condition = "CAUTION"

    if (
        temperature_trend == "INCREASING"
        and velocity_trend == "INCREASING"
        and condition == "WARNING"
    ):

        condition = "CRITICAL"

    return condition


def generate_recommendation(condition):

    if condition == "HEALTHY":

        return (
            "Vehicle operating normally. "
            "Continue monitoring."
        )

    elif condition == "CAUTION":

        return (
            "Minor irregularities or changing "
            "vehicle conditions detected. "
            "Monitor the vehicle closely."
        )

    elif condition == "WARNING":

        return (
            "Multiple risk factors or worsening "
            "trends detected. Reduce operating "
            "stress and inspect the vehicle."
        )

    return (
        "Critical operating condition detected. "
        "Stop the vehicle safely and inspect "
        "immediately."
    )


def load_telemetry(filename):

    times = []

    velocities = []

    temperatures = []

    statuses = []

    with open(
        filename,
        "r",
        newline=""
    ) as file:

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


def run_new_session():

    times = []

    velocities = []

    temperatures = []

    statuses = []

    time = 0

    end_time = get_valid_int(
        "What's the total monitoring time (s)? ",
        minimum=0
    )

    while time <= end_time:

        temp = get_valid_float(
            "What's the current temperature (°C)? "
        )

        vel = get_valid_float(
            "What's the current velocity (m/s)? ",
            allow_negative=False
        )

        status = check_vehicle_status(
            vel,
            temp
        )

        print("\nAt time:", time, "s")

        print("Velocity:", vel, "m/s")

        print("Temperature:", temp, "°C")

        print("Status:", status)

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

        times.append(time)

        velocities.append(vel)

        temperatures.append(temp)

        statuses.append(status)

        time += 1

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

        for (
            current_time,
            velocity,
            temperature,
            status
        ) in zip(
            times,
            velocities,
            temperatures,
            statuses
        ):

            writer.writerow([
                current_time,
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


def analyze_telemetry(
    times,
    velocities,
    temperatures,
    statuses
):

    temperature_data = np.array(
        temperatures
    )

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

    mean_temperature = np.mean(
        temperature_data
    )

    std_temperature = np.std(
        temperature_data
    )

    temperature_trend = detect_temperature_trend(
        temperatures
    )

    velocity_trend = detect_velocity_trend(
        velocities
    )

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

    risk_score = calculate_risk_score(
        critical_count,
        overheating_count,
        speed_count,
        anomaly_count
    )

    condition = assess_vehicle_condition(
        risk_score,
        temperature_trend,
        velocity_trend
    )

    recommendation = generate_recommendation(
        condition
    )

    print(
        "\n================================================"
    )

    print(
        "              APEX TELEMETRY REPORT"
    )

    print(
        "================================================"
    )

    print("\n--- VEHICLE EVENTS ---")

    print(
        "Critical Events:",
        critical_count
    )

    print(
        "Overheating Events:",
        overheating_count
    )

    print(
        "Speed-limit Events:",
        speed_count
    )

    print(
        "Normal Events:",
        normal_count
    )

    print("\n--- VELOCITY ANALYSIS ---")

    print(
        "Average Velocity:",
        mean_velocity,
        "m/s"
    )

    print(
        "Velocity Standard Deviation:",
        std_velocity,
        "m/s"
    )

    print(
        "Anomaly Count:",
        anomaly_count
    )

    print(
        "Velocity Trend:",
        velocity_trend
    )

    print("\n--- TEMPERATURE ANALYSIS ---")

    print(
        "Average Temperature:",
        mean_temperature,
        "°C"
    )

    print(
        "Temperature Standard Deviation:",
        std_temperature,
        "°C"
    )

    print(
        "Temperature Trend:",
        temperature_trend
    )

    print("\n--- ANOMALY DATA ---")

    print(
        "Anomaly Times:",
        anomaly_times
    )

    print(
        "Anomaly Velocities:",
        anomaly_velocities
    )

    print("\n--- VEHICLE HEALTH ASSESSMENT ---")

    print(
        "Risk Score:",
        risk_score,
        "/ 100"
    )

    print(
        "Overall Condition:",
        condition
    )

    print(
        "Recommendation:",
        recommendation
    )

    print(
        "\n================================================\n"
    )

    plt.figure()

    plt.bar(
        ["Risk Score"],
        [risk_score]
    )

    plt.ylim(0, 100)

    plt.ylabel("Risk Score")

    plt.title(
        "APEX — Vehicle Risk Assessment"
    )

    plt.grid(True)

    plt.show()

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


while True:

    print("\n========== APEX ==========")

    print("1. Run New Telemetry Session")

    print("2. Analyze Previous Telemetry")

    print("3. Exit")

    choice = input(
        "Select an option: "
    )

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

    elif choice == "2":

        sessions = get_available_sessions()

        if len(sessions) == 0:

            print(
                "\nNo telemetry sessions found."
            )

        else:

            print(
                "\n========== AVAILABLE TELEMETRY SESSIONS =========="
            )

            for index, session in enumerate(
                sessions,
                start=1
            ):

                print(
                    index,
                    ".",
                    session
                )

            session_choice = get_valid_int(
                "\nSelect a session number: ",
                minimum=1,
                maximum=len(sessions)
            )

            filename = sessions[
                session_choice - 1
            ]

            print(
                "\nLoading telemetry:",
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

    elif choice == "3":

        print(
            "\nExiting APEX. Goodbye, Engineer. 🏎️"
        )

        break

    else:

        print(
            "Invalid choice. "
            "Please select 1, 2, or 3."
        )