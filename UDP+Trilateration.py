import socket
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

# === UDP Socket Setup ===
UDP_IP = "192.168.225.147"
UDP_PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((UDP_IP, UDP_PORT))

flag = 1
latest_position = (None, None)  # Stores only the latest position

# === Anchor Positions ===
anchors = np.array([
    [2, 0],   # Anchor 1
    [1, 2],   # Anchor 2
    [0, 0]    # Anchor 3
])

# === Trilateration Function ===
def trilateration(d1, d2, d3):
    x1, y1 = anchors[0]
    x2, y2 = anchors[1]
    x3, y3 = anchors[2]

    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    D = 2 * (x3 - x1)
    E = 2 * (y3 - y1)

    C = d1*2 - d22 - x12 + x22 - y12 + y2*2
    F = d1*2 - d32 - x12 + x32 - y12 + y3*2

    try:
        x = (C * E - F * B) / (A * E - D * B)
        y = (C * D - F * A) / (B * D - E * A)
        return x, y
    except ZeroDivisionError:
        return None, None

# === Matplotlib Animation Setup ===
fig, ax = plt.subplots(figsize=(6, 6))
tag_plot, = ax.plot([], [], 'ro', markersize=8)  # Red dot for tag position

ax.set_xlim(-2,4)
ax.set_ylim(-2, 8)
ax.scatter(anchors[:, 0], anchors[:, 1], color='blue', label="Anchors")  # Plot anchor points
ax.legend()

# === Animation Update Function ===
def update(_):
    global latest_position

    x, y = latest_position
    if x is not None and y is not None:
        tag_plot.set_data([x], [y])
    
    return tag_plot,

ani = FuncAnimation(fig, update, interval=500, repeat=True)

# === Data Receiving Loop ===
def receive_data():
    global flag, latest_position

    while True:
        data, _ = client.recvfrom(1024)
        d_data = data.decode().strip()
        
        if not d_data or "ERRO" in d_data:
            continue  

        sensor_values = [value.strip() for value in d_data.split() if value.strip()]

        if len(sensor_values[0]) > 8:
            if sensor_values[0][8] == '1' and flag == 1:
                d1 = float(sensor_values[0][-5:-1])
                flag = 2
            elif sensor_values[0][8] == '2' and flag == 2:
                d2 = float(sensor_values[0][-5:-1])
                flag = 3
            elif sensor_values[0][8] == '3' and flag == 3:
                d3 = float(sensor_values[0][-5:-1])
                flag = 1

                pos = trilateration(d1, d2, d3)
                if pos != (None, None):
                    latest_position = pos  # Only update the latest position
                    print("Updated Position:", latest_position)

# Start receiving data in a separate thread
threading.Thread(target=receive_data, daemon=True).start()

plt.show()
