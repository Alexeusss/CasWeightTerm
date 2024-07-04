import serial
import serial.tools.list_ports
import time
import logging
import re

# Настройка логгера
logging.basicConfig(filename='log.csv', level=logging.INFO, format='%(asctime)s,%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def list_serial_ports():
    """ Возвращает список доступных COM портов """
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def read_weight(port):
    """ Чтение данных с весового терминала """
    weight_pattern = re.compile(r'(\d+\.\d+) kg')

    try:
        with serial.Serial(port, baudrate=9600, timeout=1) as ser:
            while True:
                if ser.in_waiting > 0:
                    try:
                        line = ser.readline().decode('latin1').strip()
                        if line:
                            match = weight_pattern.search(line)
                            if match:
                                weight = match.group(1)
                                if "ST" in line:
                                    message = f"СТАБ: {weight}0 kg"
                                elif "US" in line:
                                    message = f"НСТАБ: {weight}0 kg"
                                else:
                                    message = f"Received: {line}"
                            else:
                                message = f"Received: {line}"

                            print(message)
                            logging.info(message)
                    except UnicodeDecodeError as e:
                        print(f"Ошибка декодирования: {e}")
                time.sleep(0.1)
    except serial.SerialException as e:
        print(f"Error: {e}")

def main():
    available_ports = list_serial_ports()
    if not available_ports:
        print("Нет доступных COM портов")
        return

    print("Доступные COM порты:")
    for port in available_ports:
        print(port)

    port = input("Введите номер COM порта (например, COM3): ").strip()
    if port not in available_ports:
        print(f"COM порт {port} не найден среди доступных портов.")
        return

    read_weight(port)

if __name__ == '__main__':
    main()
