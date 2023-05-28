import asyncio
import socket
import struct
import json

# Set the treadmill parameters in m/s and m/s^2
belt_speed_mps = [2.0, 1.0, 0, 0]  # speeds in m/s
belt_acceleration_mps2 = [0.25, 0.5, 0, 0]  # accelerations in m/s^2
incline_angle = 0

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

async def send_packet():
    packet = create_packet(belt_speed_mps, belt_acceleration_mps2, incline_angle)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect the socket to the server
        server_address = ('127.0.0.1', 4000)
        sock.connect(server_address)

        # Send the packet
        sock.sendall(packet)
        print('Packet sent.')

        # Receive the response
        data = sock.recv(64)
        print('Received: {}'.format(data.hex()))
    finally:
        print('Closing socket.')
        sock.close()

if __name__ == "__main__":
    asyncio.run(send_packet())
