from machine import Pin, I2C, SPI
import framebuf
import utime
from max6675 import MAX6675
import time
import math
from mfrc522 import MFRC522
from ST7735 import TFT
from sysfont import sysfont

import time
# Inicjalizacja interfejsu SPI do obsługi LCD na magistrali SPI 0 przy użyciu odpowiednich # pinów 
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=None)
tft=TFT(spi,17,7,16)
tft.initg()
tft.fill(TFT.WHITE)
tft.rgb(True)
previous_oled_update = time.ticks_ms()
oled_update_interval = 1700  # Częstotliwość aktualizacji OLED w ms
# Konfiguracja pinów wej/wyj dla MAX6675
sck = Pin(2, Pin.OUT)
cs = Pin(3, Pin.OUT)
so = Pin(4, Pin.IN)
sensor = MAX6675(sck, cs , so)
initial_temperature = sensor.read()  # Początkowy odczyt temperatury
#Zmienne sterowania mocą dostarczaną do żelazka
firing_pin = Pin(6, Pin.OUT)
zero_cross = Pin(5, Pin.IN)
last_CH1_state = 0
zero_cross_detected = False
zero_cross_count = 0  # Licznik przejść przez zero
maximum_firing_delay = 8000
currentMillis = 0
previousMillis = 0
TempDelay = 150

setpoint = 100;
#PID konfiguracja zmiennych, stałych
kp = 750; #jakos 300-350 było na dole git
kd = 550; #szybkosc reakcji systemu na zmiane temperatury z czujnika im wieksza to wieksza
ki= 0;
PID_p = 0;
PID_i = 0;
PID_d = 0;
PID_value = 0;
previous_error = 0;
Time=0;
integral = 0
previous_time = time.ticks_ms()
previous_temperature = None   
previous_set_temperature = None  # Globalna zmienna do przechowywania poprzedniej ustawionej temperatury
# Inicjalizacja modułu MFRC522
# SDA=cs=13=csn, SCK=14 na pinie sck musi byc, MOSI=15=TX, MISO=12=RX, rst=11                 
rc522 = MFRC522(spi_id=1,cs=13,sck=14,miso=12,mosi=15,rst=11)
rc522.setRxGain(43) #ustawienie mocy antteny RFID , 48 max
# Inicjalizacja zmiennej do śledzenia czasu ostatniego sprawdzenia RFID
previous_rfid_check = time.ticks_ms()
rfid_check_interval = 1000  # 2000 ms = 2 sekundy
# Definiowanie mapowania UID na wartości setpoint
uid_to_setpoint = {
    "40d13934": 120,  # UID dla "Tkaniny syntetyczne"
    "40fd8934": 140,  # UID dla "Bawełna"
    "e72903d9": 220,  # UID dla "Wełna / Len"
    "a011d854": 130,
    "b031d854": 180,
    "b029d854": 240,
    "a019d854": 230,
    "b023d854": 200,
    # Dodaj więcej kart i ich setpointów tutaj
    }

def handle_interrupt(pin):
    global zero_cross_detected, zero_cross_count, last_CH1_state
    if pin.value() == 1 and last_CH1_state == 0:
        zero_cross_detected = True
        zero_cross_count += 1  # Inkrementacja licznika przejść przez zero
    last_CH1_state = pin.value()
    
# Konfiguracja przerwań
zero_cross.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=handle_interrupt)

def show_temp(real_temperature, set_temperature):
    global previous_temperature, previous_set_temperature
    temp_set = "{:.2f}".format(set_temperature)

    # Definiujemy stałe na początku funkcji
    text_scale = 2
    temp_scale = 3
    approximate_char_width = 5.2 # Domyślna szerokość znaku, dostosuj do faktycznej czcionki i skali
    char_offset = 11 # Domyślny odstęp między znakami, dostosuj do faktycznej czcionki i skali
    degree_symbol_radius = 3  # Promień symbolu stopni, dostosuj do skali

    # Reset całego ekranu, jeśli zmieniła się ustawiona temperatura
    if set_temperature != previous_set_temperature:
        tft.fill(tft.BLACK)  # Czyszczenie całego ekranu
        # Rysowanie stałego tekstu
        tft.text((10, 10), "Grzanie do:", tft.WHITE, sysfont, text_scale)
        tft.text((20, 35), temp_set, tft.CYAN, sysfont, temp_scale)
        tft.text((10, 70), "Temperatura:", tft.WHITE, sysfont, text_scale)
        # Rysowanie symbolu stopni i "C"
        current_temp_length = len(temp_set) * approximate_char_width * temp_scale + 20
        tft.circle((current_temp_length + degree_symbol_radius * 2, 35 + temp_scale - degree_symbol_radius), degree_symbol_radius, tft.CYAN)
        tft.text((current_temp_length + char_offset, 35), "C", tft.CYAN, sysfont, temp_scale)
        previous_set_temperature = set_temperature

    # Aktualizacja wyświetlanej temperatury, jeśli jest inna niż poprzednio zmierzona
    if real_temperature != previous_temperature:
        temp = "{:.2f}".format(real_temperature)
        # "Czyszczenie" obszaru temperatury przed narysowaniem nowej wartości
        tft.fillrect((20, 90), (120, 30), tft.BLACK)
        
        # Ponowne narysowanie wartości temperatury
        tft.text((20, 95), temp, tft.CYAN, sysfont, temp_scale)
        
        # Rysowanie symbolu stopni i "C"
        current_temp_length = len(temp) * approximate_char_width * temp_scale + 20
        tft.circle((current_temp_length + degree_symbol_radius * 2, 95 + temp_scale - degree_symbol_radius), degree_symbol_radius, tft.CYAN)
        tft.text((current_temp_length + char_offset, 95), "C", tft.CYAN, sysfont, temp_scale)
        
        previous_temperature = real_temperature

def calculate_PID(setpoint, real_temperature):
    global previous_error, integral, previous_time, PID_p, PID_i, PID_d, PID_value

    current_time = time.ticks_ms()
    elapsedTime = (current_time - previous_time) / 1000  # Convert ms to seconds

    # Compute all the working error variables
    error = setpoint - real_temperature
    integral += error * elapsedTime

    # Oblicz wartość pochodnej tylko gdy elapsedTime > 0, aby uniknąć dzielenia przez zero
    if elapsedTime > 0:
        derivative = (error - previous_error) / elapsedTime
    else:
        derivative = 0

    # Compute PID values
    PID_p = kp * error
    PID_i = ki * integral
    PID_d = kd * derivative

    # Compute final PID value
    PID_value = PID_p + PID_i + PID_d

    # Remember some variables for next time
    previous_error = error
    previous_time = current_time
    return PID_value


def delay_MAX6675():
    global previousMillis, TempDelay, currentMillis
    currentMillis = time.ticks_ms()
    if currentMillis - previousMillis >= TempDelay:
        previousMillis = currentMillis
        return True
    return False

def delay_MAX6675():
    global previousMillis, TempDelay, currentMillis
    currentMillis = time.ticks_ms()
    if currentMillis - previousMillis >= TempDelay:
        previousMillis = currentMillis
        return True
    return False

def delay_MAX6675():
    global previousMillis, TempDelay, currentMillis
    currentMillis = time.ticks_ms()
    if currentMillis - previousMillis >= TempDelay:
        previousMillis = currentMillis
        return True
    return False

while True:
    if delay_MAX6675():
        real_temperature = sensor.read()  # Pobierz rzeczywistą temperaturę
        current_time = time.ticks_ms()
        print(real_temperature)

        # Kontrola PID
        PID_value = calculate_PID(setpoint, real_temperature)
        if PID_value > maximum_firing_delay:
            PID_value = maximum_firing_delay
        elif PID_value < 0:
            PID_value = 0

    if zero_cross_detected:
        firing_delay = maximum_firing_delay - PID_value
        utime.sleep_us(int(firing_delay))
        firing_pin.on()
        utime.sleep_us(100)  # Impuls wyzwalający o długości 100 µs
        firing_pin.off()
        zero_cross_detected = False

    # Sprawdzanie karty RFID co 2 sekundy
    if time.ticks_diff(current_time, previous_rfid_check) > rfid_check_interval:
        previous_rfid_check = current_time
        (stat, tag_type) = rc522.request(rc522.REQALL)
        if stat == rc522.OK:
            (status, raw_uid) = rc522.SelectTagSN()
            if status == rc522.OK:
                rfid_uid = "{:02x}{:02x}{:02x}{:02x}".format(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                print("Card detected! UID: {}".format(rfid_uid))
                if rfid_uid in uid_to_setpoint:
                    setpoint = uid_to_setpoint[rfid_uid]
                else:
                    print("Nieznana karta")
            else:
                print("Error reading card")

    # Aktualizacja OLED tylko co ustalony interwał czasowy
    if time.ticks_diff(current_time, previous_oled_update) > oled_update_interval:
        show_temp(real_temperature, setpoint)
        previous_oled_update = current_time

 

       
       
       