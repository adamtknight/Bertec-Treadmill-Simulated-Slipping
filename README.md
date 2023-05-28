# Slip Simulation on a Treadmill

This python script simulates a slip event on a treadmill. It connects to a treadmill and a force plate to detect foot strikes, then causes the treadmill to slip after a random number of steps within a user-defined range. 

## Disclaimer

This software is provided "as-is" without any express or implied warranty. In no event will the author be held liable for any damages arising from the use of this software. 

Use of this software is at your own risk. The author assumes no responsibility or liability for any injury, physical or otherwise, suffered as a result of the use of this software.

You are advised to ensure that your use of this software is in compliance with all relevant safety guidelines and regulations, and to take all necessary precautions. This software is intended for experimental and research purposes only and should not be used in a real-world setting without adequate supervision and safety measures.


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

1. Open a new "command prompt" and run:
```bash
cd Documents\Treadmill Controller
```
2. Next open vscode by running:
```bash
code .
```
3. Update the captilized paramaters to fit your needs
4. Open QTM on the main computer and ensure a live session is open or you are recording
5. Open Bertec Treadmill controller and open settings and check 'Remote TCP/IP Control', then click the TCP button and ensure Listen on 127.0.0.1 is checked and 4000 is selected for the listening port. Click 'Ok' and ensure the 'enable remote control' button is selected on the main screen.
6. Run the code by running the command:
```bash
python main.py
```
7. Press enter to bring the treadmill to speed
8. Press enter to begin the slipping randomization trial
9. Stop the code from running by pressing "CTR C"

## DEBUG

- Always ensure QTM is running on the main computer and has either a trial recording or a live session screen open
- Ensure the QTM IP address has not changed by running "ipconfig" as an adiministrator on the main computer.
-Ensure force plates and treadmill are on
-Always ensure treadmill remote control is enabled as described above
## Dependencies

This script requires the `asyncio`, `qtm`, `socket`, `json`, `struct`, `math`, `time`, and `random` Python libraries.
