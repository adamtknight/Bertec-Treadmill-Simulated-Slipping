import asyncio
import qtm
import math
import socket
import json
import struct
import math
import time

FORCE_THRESHOLD = 10.0  # Adjust this value as per your requirements
# Set the treadmill parameters in m/s and m/s^2


# Define thresholds
HEEL_STRIKE_THRESHOLD = 1300
TOE_OFF_THRESHOLD = 1250

# Initialize foot state
left_foot_on_treadmill = False
right_foot_on_treadmill = False

def create_packet(belt_speed_mps, belt_acceleration_mps2, incline_angle):
    belt_speed = [int(speed * 1000) for speed in belt_speed_mps]
    belt_acceleration = [int(acc * 1000) for acc in belt_acceleration_mps2]

    packet = bytearray(64)

    struct.pack_into('>B', packet, 0, 0)

    for i in range(4):
        struct.pack_into('>h', packet, 1 + i*2, belt_speed[i])
        struct.pack_into('>h', packet, 9 + i*2, belt_acceleration[i])
        if i == 0:
            struct.pack_into('>h', packet, 17, incline_angle)

    for i in range(4):
        struct.pack_into('>h', packet, 19 + i*2, ~belt_speed[i])
        struct.pack_into('>h', packet, 27 + i*2, ~belt_acceleration[i])
        if i == 0:
            struct.pack_into('>h', packet, 35, ~incline_angle)

    return packet
def on_packet(packet):
    global left_foot_on_treadmill, right_foot_on_treadmill
    header, force_data = packet.get_force()

    for p_num, plate_data in enumerate(force_data):
        for force in plate_data[1]:
            # print("----------FORCE DATA --------------")
            # print(force_data)
            # print("-------------PLATE DATA -----------")
            # print(plate_data)
            # print("------------- P1 ---------")
            # print(plate_data[1])
            # print("-------------FORCE---------")
            # print(force)
            if plate_data[0].id == 1:
                left_force = abs(force.z)
                # Handle left foot
                if left_force > HEEL_STRIKE_THRESHOLD and not left_foot_on_treadmill:
                    print("Left Heel Strike")
                    left_foot_on_treadmill = True
                elif left_force < TOE_OFF_THRESHOLD and left_foot_on_treadmill:
                    print("Left Toe Off")
                    left_foot_on_treadmill = False
            else:
                right_force = abs(force.z)
                
                # Handle right foot
                if right_force > HEEL_STRIKE_THRESHOLD and not right_foot_on_treadmill:
                    
                    right_foot_on_treadmill = True
                elif right_force < TOE_OFF_THRESHOLD and right_foot_on_treadmill:
                    print("Right Toe Off")
                    f_belt_speed_mps = [6, 1.75, 0, 0]  # speeds in m/s
                    f_belt_acceleration_mps2 = [10, 10, 0, 0]  # accelerations in m/s^2
                    f_incline_angle = 0
                    packet = create_packet(f_belt_speed_mps, f_belt_acceleration_mps2, f_incline_angle)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_address = ('127.0.0.1', 4000)
                    sock.connect(server_address)
                    sock.sendall(packet)

                    time.sleep(0.12)
                    f_belt_speed_mps = [1.75, 1.75, 0, 0]  # speeds in m/s
                    f_belt_acceleration_mps2 = [5, 5, 0, 0]  # accelerations in m/s^2
                    f_incline_angle = 0
                    packet = create_packet(f_belt_speed_mps, f_belt_acceleration_mps2, f_incline_angle)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_address = ('127.0.0.1', 4000)
                    sock.connect(server_address)
                    sock.sendall(packet)
                    print("Right Heel Strike")
                    right_foot_on_treadmill = False

# def on_packet(packet):
#     global foot_on_treadmill
#     header, force_data = packet.get_force()
#     count = 0
#     for plate_data in force_data:
#         count+=1
#         for force in plate_data[1]:
#             force_magnitude = abs(force.z)
            
#             # Detect heel strike and toe off
#             if force_magnitude > HEEL_STRIKE_THRESHOLD and not foot_on_treadmill:
#                 print("Heel Strike")
#                 # f_belt_speed_mps = [0.0, 1.0, 0, 0]  # speeds in m/s
#                 # f_belt_acceleration_mps2 = [5, 5, 0, 0]  # accelerations in m/s^2
#                 # f_incline_angle = 0
#                 # packet = create_packet(f_belt_speed_mps, f_belt_acceleration_mps2, f_incline_angle)
#                 # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 # server_address = ('127.0.0.1', 4000)
#                 # sock.connect(server_address)
#                 # sock.sendall(packet)
#                 foot_on_treadmill = True
#             elif force_magnitude < TOE_OFF_THRESHOLD and foot_on_treadmill:
#                 print("Toe Off")
#                 f_belt_speed_mps = [0.0, 5, 0, 0]  # speeds in m/s
#                 f_belt_acceleration_mps2 = [10, 10, 0, 0]  # accelerations in m/s^2
#                 f_incline_angle = 0
#                 packet = create_packet(f_belt_speed_mps, f_belt_acceleration_mps2, f_incline_angle)
#                 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 server_address = ('127.0.0.1', 4000)
#                 sock.connect(server_address)
#                 sock.sendall(packet)

#                 time.sleep(10)
#                 f_belt_speed_mps = [0.0, 1.0, 0, 0]  # speeds in m/s
#                 f_belt_acceleration_mps2 = [5, 5, 0, 0]  # accelerations in m/s^2
#                 f_incline_angle = 0
#                 packet = create_packet(f_belt_speed_mps, f_belt_acceleration_mps2, f_incline_angle)
#                 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 server_address = ('127.0.0.1', 4000)
#                 sock.connect(server_address)
#                 sock.sendall(packet)
                
#                 foot_on_treadmill = False
        
#         if count > 0:
#             break

async def setup():
    """ Main function """
    connection = await qtm.connect("128.119.66.119")
    if connection is None:
        return

    await connection.stream_frames(components=["force"], on_packet=on_packet)

if __name__ == "__main__":
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()
