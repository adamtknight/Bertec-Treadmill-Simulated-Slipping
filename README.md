# Slip Simulation on a Treadmill

This python script simulates a slip event on a treadmill. It connects to a treadmill and a force plate to detect foot strikes, then causes the treadmill to slip after a random number of steps within a user-defined range. 

## Parameters

Several parameters can be customized in the code:

- `TIME_TO_SLIP`: Time from heel strike to slip (in seconds)
- `TIME_OF_SLIP`: Duration of the slip (in seconds)
- `SLIP_ACCELERATION`: Acceleration value of the slip (in m/s^2)
- `SLIP_VELOCITY`: Velocity value of the slip (in m/s)
- `PARTICIPANT_SPEED`: The participant's walking speed (in m/s)
- `MIN_SLIP_STEP`, `MAX_SLIP_STEP`: The range within which the slip event can occur (in number of steps)
- `TREADMILL_IP`, `TREADMILL_PORT`: The IP address and port number of the treadmill
- `QTM_IP`: The IP address of the Qualisys Track Manager (QTM)
- `HEEL_STRIKE_THRESHOLD`, `TOE_OFF_THRESHOLD`: Force thresholds for detecting a heel strike and toe off event (in Newtons)

## Usage

1. Set the required parameters in the script.
2. Run the script.
3. Press enter to get the treadmill up to the participant's speed.
4. Press enter again to start the slip simulation.

## Dependencies

This script requires the `asyncio`, `qtm`, `socket`, `json`, `struct`, `math`, `time`, and `random` Python libraries.
