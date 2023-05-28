import asyncio
import qtm
import math
import socket
import json
import struct
import math
import time
import random

##############VALUES TO CHANGE##################
#Time from heel_strike to slip
TIME_TO_SLIP = 0.45 #sec

#Time that the slipping speed takes place for
TIME_OF_SLIP = 0.15 #sec

#Acceleration value of the slip
SLIP_ACCELERATION = 10 #m/s

#Velocity value of the slip
SLIP_VELOCITY = 2.5 #m/s

PARTICIPANT_SPEED = 1.25 #m/s

# Define the range for slip steps
MIN_SLIP_STEP = 4 # minimum steps
MAX_SLIP_STEP = 8 # maximum steps

#########ADDRESS VALUES############
TREADMILL_IP = '127.0.0.1'
TREADMILL_PORT = 4000

QTM_IP = "128.119.66.119"

# Define thresholds
HEEL_STRIKE_THRESHOLD = 150
TOE_OFF_THRESHOLD = 100

# Initialize foot state
left_foot_on_treadmill = False
right_foot_on_treadmill = False

# Initialize slip step counter
slip_step_counter = 0
slip_step_threshold = random.randint(MIN_SLIP_STEP, MAX_SLIP_STEP)

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
    global left_foot_on_treadmill, right_foot_on_treadmill, slip_step_counter, slip_step_threshold
    header, force_data = packet.get_force()

    for p_num, plate_data in enumerate(force_data):
        for force in plate_data[1]:
            if plate_data[0].id == 1:
                left_force = abs(force.z)
                # Handle left foot
                if left_force > HEEL_STRIKE_THRESHOLD and not left_foot_on_treadmill:
                    slip_step_counter += 1
                    if slip_step_counter == slip_step_threshold:
                        handle_slip("L")
                        # Reset slip_step_counter and set new slip_step_threshold
                        slip_step_counter = 0
                        slip_step_threshold = random.randint(MIN_SLIP_STEP, MAX_SLIP_STEP)
                    left_foot_on_treadmill = True
                elif left_force < TOE_OFF_THRESHOLD and left_foot_on_treadmill:
                    left_foot_on_treadmill = False
            else:
                right_force = abs(force.z)
                # Handle right foot
                if right_force > HEEL_STRIKE_THRESHOLD and not right_foot_on_treadmill:
                    slip_step_counter += 1
                    if slip_step_counter == slip_step_threshold:
                        handle_slip("R")
                        # Reset slip_step_counter and set new slip_step_threshold
                        slip_step_counter = 0
                        slip_step_threshold = random.randint(MIN_SLIP_STEP, MAX_SLIP_STEP)
                    right_foot_on_treadmill = True
                elif right_force < TOE_OFF_THRESHOLD and right_foot_on_treadmill:
                    right_foot_on_treadmill = False

def handle_slip(side):
    time.sleep(TIME_TO_SLIP)
    if (side == "R"):
        f_belt_speed_mps = [SLIP_VELOCITY, PARTICIPANT_SPEED, 0, 0]  # speeds in m/s
        f_belt_acceleration_mps2 = [SLIP_ACCELERATION, 0, 0, 0]  # accelerations in m/s^2
        f_incline_angle = 0
    else:
        f_belt_speed_mps = [PARTICIPANT_SPEED, SLIP_VELOCITY, 0, 0]  # speeds in m/s
        f_belt_acceleration_mps2 = [0, SLIP_ACCELERATION, 0, 0]  # accelerations in m/s^2
        f_incline_angle = 0

    packet = create_packet(f_belt_speed_mps, f_belt_acceleration_mps2, f_incline_angle)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (TREADMILL_IP, TREADMILL_PORT)
    sock.connect(server_address)
    sock.sendall(packet)

    time.sleep(TIME_OF_SLIP)
    f_belt_speed_mps = [PARTICIPANT_SPEED, PARTICIPANT_SPEED, 0, 0]  # speeds in m/s
    f_belt_acceleration_mps2 = [10, 10, 0, 0]  # accelerations in m/s^2
    f_incline_angle = 0
    packet = create_packet(f_belt_speed_mps, f_belt_acceleration_mps2, f_incline_angle)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (TREADMILL_IP, TREADMILL_PORT)
    sock.connect(server_address)
    sock.sendall(packet)

async def setup():
    """ Main function """
    connection = await qtm.connect(QTM_IP)
    if connection is None:
        return

    await connection.stream_frames(components=["force"], on_packet=on_packet)

def start_treadmill():
    # Set both belts to participant speed
    f_belt_speed_mps = [PARTICIPANT_SPEED, PARTICIPANT_SPEED, 0, 0]
    f_belt_acceleration_mps2 = [0.3, 0.3, 0, 0] # accelerations in m/s^2
    f_incline_angle = 0
    
    packet = create_packet(f_belt_speed_mps, f_belt_acceleration_mps2, f_incline_angle)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (TREADMILL_IP, TREADMILL_PORT)
    sock.connect(server_address)
    sock.sendall(packet)
    sock.close()

if __name__ == "__main__":
    input("Press enter to start treadmill...")
    start_treadmill()

    input("Press enter to start slipping...")
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()

