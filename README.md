# RFID-Enabled-Automated-Iron-Temperature-Control
The project presents the construction of a fully functional iron that automatically sets the temperature by reading RFID identifiers placed in ironed clothes. The temperature control algorithm is based on PID control.
<p align="center">
  <img src="https://github.com/user-attachments/assets/d58c7142-7ddf-4006-8156-5569e0c2d7dd">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/8aab20bf-c929-4ce9-ae06-862c8b10b950">
</p>

# Power and PID control
Power control guide by “Electronoobs”, which accurately describes zero crossing detection, triac control, and PID https://www.youtube.com/watch?v=P6mbBJDIvxI&ab_channel=Electronoobs 
The design is based on the use of phase-delay control, which allows precise adjustment of the heating temperature. A key component of the system is the detection of the moment when the AC line voltage passes through zero, which is important for synchronizing the control with the voltage cycle.



The display was realized on the TFT LCD ST7735S using the user library “boochow” https://github.com/boochow/MicroPython-ST7735/blob/master/ST7735.py.  Temperature reading is realized with the RC522 RFID module based on the user library “kevinmcaleer” https://github.com/kevinmcaleer/pico-rfid/blob/main/mfrc522.py.


