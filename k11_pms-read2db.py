try:
    import struct
except ImportError:
    import ustruct as struct

# added by dieter
import time
import MySQLdb as mariadb
import netrc

# Connect the sensor TX pin to the board/computer RX pin
# For use with a microcontroller board:
#import board
#import busio
#uart = busio.UART(board.TX, board.RX, baudrate=9600)

# For use with Raspberry Pi/Linux:
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

# For use with USB-to-serial cable:
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.25)

## set up database connection
def db_connect():
    try:
        host = 'localhost'
        host_ip = '172.0.0.1'
        cred = netrc.netrc().authenticators(host)
        #print(cred)
        mdb_conn = mariadb.connect(host_ip, cred[0], cred[2], 'meteo')

    except:
        print("I am unable to connect to mariadb database meteo!")

    return mdb_conn

mdb_conn = db_connect()


buffer = []

while True:
    data = uart.read(32)  # read up to 32 bytes
    # print("string: ", data)
    data = list(data)
    # print("read: ", data)          # this is a bytearray type

    buffer += data

    while buffer and buffer[0] != 0x42:
        buffer.pop(0)

    if len(buffer) > 200:
        buffer = []  # avoid an overrun if all bad data
    if len(buffer) < 32:
        continue

    if buffer[1] != 0x4d:
        buffer.pop(0)
        continue

    frame_len = struct.unpack(">H", bytes(buffer[2:4]))[0]
    if frame_len != 28:
        buffer = []
        continue

    frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))

    pm10_standard, pm25_standard, pm100_standard, pm10_env, \
        pm25_env, pm100_env, particles_03um, particles_05um, particles_10um, \
        particles_25um, particles_50um, particles_100um, skip, checksum = frame

    check = sum(buffer[0:30])

    if check != checksum:
        buffer = []
        continue

    sensors = {4:pm10_env, 5:pm25_env, 6:pm100_env}
    
    timestamp = time.strftime("%y-%m-%d %H:%M:%S")
    for sensorid in sensors:
        mcursor_measurement_insert = mdb_conn.cursor()
        sql_insert_measurement_new = """INSERT INTO measurement (sensor_id, parameter_id, measuredatetime, measure) VALUES (%s, %s, %s, %s);"""
        sql_insert_measurement = """INSERT INTO measurement (sensor_id, parameter_id, measuredatetime, measure) VALUES (%s, %s, %s, %s);"""
        #print(pm10_env)
        inserttuple = (6, sensorid, timestamp, float(sensors[sensorid]))
        #print(inserttuple)
        mcursor_measurement_insert.execute(sql_insert_measurement, inserttuple)
        mdb_conn.commit()

    buffer = buffer[32:]

    break


mdb_conn.close()
