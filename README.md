# RFID-Enabled-Automated-Iron-Temperature-Control

The project presents the construction of a fully functional iron that automatically sets the temperature by reading RFID identifiers placed in ironed clothes. The temperature control algorithm is based on PID control.
<p align="center">
  <img src="https://github.com/user-attachments/assets/d4ed9dc0-e8c1-4179-bdef-a33d72f8b425">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/8aab20bf-c929-4ce9-ae06-862c8b10b950">
</p>

### Simplified block diagram of the automated iron demonstration model

<p align="center">
  <img src="https://github.com/user-attachments/assets/ecc0c315-ce39-46e9-818b-9561bd2f1921">
</p>

# Schematic and project heating power control module
The project schematic, sample 3D model and gerber file is in the folder "PCB Design Electronic Temperature Control System for Automated Iron"
<p align="center">
  <img src="https://github.com/user-attachments/assets/1409585e-9fe1-43e5-a72e-cab69f359077">
  <img src="https://github.com/user-attachments/assets/8e4f7270-c5d8-43d3-9067-631738742f07">
</p>

# Power and PID control

Power control guide by “Electronoobs”, which accurately describes zero crossing detection, triac control, and PID https://www.youtube.com/watch?v=P6mbBJDIvxI&ab_channel=Electronoobs. 
The design is based on the use of phase-delay control, which allows precise adjustment of the heating temperature. A key component of the system is the detection of the moment when the AC line voltage passes through zero, which is important for synchronizing the control with the voltage cycle.
<p align="center">
  <img src="https://github.com/user-attachments/assets/d9746f44-6ded-443f-8944-6878a1418bd3">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/f6fe8c1e-ad30-462f-878b-743e11e43f99">
  <img src="https://github.com/user-attachments/assets/23aac976-357b-4ec9-88b5-69a84c59b32c">
  <img src="https://github.com/user-attachments/assets/bf14816c-53ea-4296-b89a-5f5566fb2242">
</p>

# List of elements needed to build the project

<p align="center">
  <img src="https://github.com/user-attachments/assets/f0798c2c-b4db-4ef2-8f07-f5ab6efee7ca">
</p>

- Raspberry Pi Pico
- RC522 RFID module
- RFID TAG MIFARE 13.56 MHz - sticker
- 10A Glass Tube Fuse and Fuse Socket
- MAX6675 converter chip - SPI temperature sensor
- Thermocouple type K - KPS-TP300
- TFT LCD 128x160 SPI ST7735S display
- Triac BTA16-600BQ + thermal pad and heat sink (for TO220 case)
- MOC3020-LIT triac driver
- EL817C optocoupler
- Bridge rectifier MP1010G-DC
- MR010NAL ferrite material
- AC/DC converter
- 2x Resistor 43k Ohm
- Resistor 1k Ohm
- Resistor 220 Ohm

> [!CAUTION]
> Of course, you can choose other components, but you must remember to protect the microcontroller from too much current and select, for example, a suitable triac with a driver operating at 230V and 10-20A.

# An example of using automated iron in IoT
<p align="center">
  <img src="https://github.com/user-attachments/assets/d454ec80-646d-402d-bd42-c17971e1c51a">
</p>

# Library guide

- The display was realized on the TFT LCD ST7735S using the user library “boochow” https://github.com/boochow/MicroPython-ST7735/blob/master/ST7735.py.
- Temperature reading was realized with the RC522 RFID module based on the user library “kevinmcaleer” https://github.com/kevinmcaleer/pico-rfid/blob/main/mfrc522.py.
- The conversion of the thermoelectric signal from the thermocouple to a digital temperature value was based on the
“BetaRavener” user library and the max6675 chip https://github.com/BetaRavener/micropython-hw-lib/blob/master/MAX6675/max6675.py.

### Listing of a program fragment including implementation of libraries, constants and variables

Go to the main.py file and find such items in the program as PID configuration, maximum_faring_delay, and uid_to_setpoint.
Add your tags and the temperature values ​​they represent. If the system is not working configure Kp, Kd, ​​Ki and maximum_firing_deley.
<p align="center">
  <img src="https://github.com/user-attachments/assets/8d394e15-2927-41f8-8645-64bd6f782bf2">
</p>

- Kp is responsible for the immediate response 
- Kd is for predicting future error and stabilization
- Ki is for eliminating the long-term error

> [!IMPORTANT]
> To adjust system start with Kp, if the system responds quickly enough, go to setting the Kd coefficient and then to Ki

> [!IMPORTANT]
> The dictionary uid_to_setpoint = {} is for add the UID of your TAG and the temperature it should represent.

> [!WARNING]
> If you add operations to your code that require more processing time by the Raspberry Pi, pay attention to the Maximum Faring Delay. Exceeding this limit may cause desynchronization with the sinusoidal signal, which will affect the stability and accuracy of the system..
