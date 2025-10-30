import serial
import serial.tools.list_ports
import time

import menu


# Menu changer
def menu_change(new_menu):
    menu.active = new_menu
    print(menu.active.menu_str())
    ser.write(menu.active.menu_str())

def execute_action(action):
    action.execute()
    
def execute_item(item):
    if item.get_type() == "action":
        execute_action(item) 
    elif item.get_type() == "menu":
        menu_change(item)


# Search Arduino or CH340 controller
def find_arduino(target_vid, target_pid):
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        vid = f"{port.vid:04X}" if port.vid else None
        pid = f"{port.pid:04X}" if port.pid else None
        
        if vid == target_vid and pid == target_pid:
            return port.device
    return None

# Port and baudrate
vid, pid = "2341", "8036" # Change to match yours
arduino_port = find_arduino(vid, pid) 
baud_rate = 9600

# Inicia la conexión serial con el Arduino
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Espera 2 segundos para que la conexión serial se establezca

# Store local time
local_time = int(time.mktime(time.localtime()))

# Enviar comandos al Arduino para encender y apagar el LEDc
try:
    ser.write(b"_OK\n")
    ser.write(f"{local_time}\n".encode('utf-8'))
    time.sleep(1)

    menu_change(menu.main)
    while True:
        if ser.in_waiting > 0:  # Comprobar si hay datos disponibles para leer
            key = ser.readline().decode('utf-8').strip()  # Leer y decodificar el dato
            if key.startswith('$'):
                key = key[1:]
            print(f"Arduino: {key}")  # Mostrar la tecla recibida
            if key == 'u':
                ser.write(b"_SS\n")
            elif key == 'd':
                pass
            elif key == 'S':
                menu_change(menu.main)
            elif key == 'D':
                pass
            elif key == 'M':
                pass
            elif key == 'H':
                pass
            else:
                try:
                    execute_item(menu.active.items[int(key)-1])
                except Exception as e:
                    print("Index out of bounds")
            

except KeyboardInterrupt:
    print("\nUser disconnected.")

finally:
    # Cierra la conexión serial
    ser.write(b"_KO\n")
    ser.close()
    print("Disconnected.")
