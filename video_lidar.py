import cv2
import numpy as np
import csv
import matplotlib.pyplot as plt

# Video settings
frame_size = (600, 600)
fps = 10  # Frames per second
video_filename = "lidar_video.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
out = cv2.VideoWriter(video_filename, fourcc, fps, frame_size)

angles = []
distances = []

with open("lidar_data.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header

    for row in reader:
        angle = float(row[0])
        distance = float(row[1])
        angles.append(angle)
        distances.append(distance)

        if angle >= 350:  
            angles_rad = np.radians(angles)
            x = np.array(distances) * np.cos(angles_rad)
            y = np.array(distances) * np.sin(angles_rad)

            # Create the plot
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.scatter(x, y, s=2, color="blue")
            ax.set_xlabel("X Distance (mm)")
            ax.set_ylabel("Y Distance (mm)")
            ax.set_title("LIDAR Scan")
            ax.set_xlim(-3000, 3000)  # Adjust based on your LIDAR range
            ax.set_ylim(-3000, 3000)
            ax.grid(True)
            ax.set_aspect('equal')
            plt.savefig("temp_frame.png")

            frame = cv2.imread("temp_frame.png")
            if frame is None:
                print("Error reading the frame!")
            frame = cv2.resize(frame, frame_size)  # Ensure size matches video settings
            out.write(frame)

            # Reset for next scan
            angles.clear()
            distances.clear()

# Release video writer
out.release()
if not out.isOpened():
    print("Error: VideoWriter failed to open!")
print(f"Video saved as {video_filename}")
