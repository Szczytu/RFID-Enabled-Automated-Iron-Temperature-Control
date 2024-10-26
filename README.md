# RFID-Enabled-Automated-Iron-Temperature-Control
The project presents the construction of a fully functional iron that automatically sets the temperature by reading RFID identifiers placed in ironed clothes. The temperature control algorithm is based on PID control.
<p align="center">
  <img src="![iron1](https://github.com/user-attachments/assets/659dea1a-f618-4475-b3ad-3f703bdb8027)" alt="demonstration iron with the installed control system
heating power and RFID" width="300"/>
</p>

![iron1](https://github.com/user-attachments/assets/bc5ff706-d3e6-4ebd-bb0b-0ca4072b8503)
![iron2](https://github.com/user-attachments/assets/97fe4aa4-29fc-4500-a4bf-56ea78fb968c)
![iron3](https://github.com/user-attachments/assets/70e24a95-190a-4f5c-9a40-b78c7bedcd9a)

# Power and PID control
Power control guide by “Electronoobs”, which accurately describes zero crossing detection, triac control, and PID https://www.youtube.com/watch?v=P6mbBJDIvxI&ab_channel=Electronoobs 
The design is based on the use of phase-delay control, which allows precise adjustment of the heating temperature. A key component of the system is the detection of the moment when the AC line voltage passes through zero, which is important for synchronizing the control with the voltage cycle.



The display was realized on the TFT LCD ST7735S using the user library “boochow” https://github.com/boochow/MicroPython-ST7735/blob/master/ST7735.py.  Temperature reading is realized with the RC522 RFID module based on the user library “kevinmcaleer” https://github.com/kevinmcaleer/pico-rfid/blob/main/mfrc522.py.


