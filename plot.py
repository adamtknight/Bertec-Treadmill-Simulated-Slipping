import asyncio
import qtm
import socket
import struct
import matplotlib.pyplot as plt
import time

FORCE_THRESHOLD = 10.0  # Adjust this value as per your requirements

# Define thresholds
HEEL_STRIKE_THRESHOLD = 100
TOE_OFF_THRESHOLD = 50

# Initialize foot state and data lists
foot_on_treadmill = False
force_data_list = []
time_data_list = []

start_time = time.time()  # record the starting time

def on_packet(packet):
    global foot_on_treadmill
    header, force_data = packet.get_force()
    count = 0
    for plate_data in force_data:
        count+=1
        for force in plate_data[1]:
            force_magnitude = abs(force.z)
            force_data_list.append(force_magnitude)
            time_data_list.append(time.time() - start_time)  # store relative time
        if count > 0:
            break
            # your existing code

async def stop_after_10_seconds():
    """Stop the event loop after 10 seconds"""
    await asyncio.sleep(40)
    asyncio.get_event_loop().stop()

async def setup():
    """ Main function """
    connection = await qtm.connect("128.119.66.119")
    if connection is None:
        return

    await connection.stream_frames(components=["force"], on_packet=on_packet)
    asyncio.ensure_future(stop_after_10_seconds())  # schedule the stop function

if __name__ == "__main__":
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()

    # After the event loop has stopped, plot the data
    plt.plot(time_data_list, force_data_list)
    plt.xlabel('Time (s)')
    plt.ylabel('Force Magnitude')
    plt.title('Force over Time')
    plt.show()
