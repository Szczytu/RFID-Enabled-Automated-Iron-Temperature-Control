# RFID-Enabled-Automated-Iron-Temperature-Control
The project presents the construction of a fully functional iron that automatically sets the temperature by reading RFID identifiers placed in ironed clothes. The temperature control algorithm is based on PID control.
<p align="center">
  <img src="https://github.com/user-attachments/assets/d4ed9dc0-e8c1-4179-bdef-a33d72f8b425">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/8aab20bf-c929-4ce9-ae06-862c8b10b950">
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
  <img src="https://github.com/user-attachments/assets/6ababfed-aee1-4488-a546-1aaef164576b">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/850e76e5-5dcc-41f5-b324-bc423a77c18c">
  <img src="https://github.com/user-attachments/assets/71757215-ee91-4b2d-baca-23cf9f552a21">
  <img src="https://github.com/user-attachments/assets/597de46d-10db-4cc7-b8df-10e4c418f0da">
</p>

The display was realized on the TFT LCD ST7735S using the user library “boochow” https://github.com/boochow/MicroPython-ST7735/blob/master/ST7735.py.  Temperature reading is realized with the RC522 RFID module based on the user library “kevinmcaleer” https://github.com/kevinmcaleer/pico-rfid/blob/main/mfrc522.py.


