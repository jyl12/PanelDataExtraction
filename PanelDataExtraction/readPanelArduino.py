import serial
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

g_indicator=0
r_indicator=0
r_led=0

while True:
    reading = ser.readline().decode()
    print(reading)
#     if len(reading)>0:
#         x = reading.split(":")
#         if x[0][4]=='G':
#             #print(x[1][1])
#             if x[1][1]=='H':
#                 g_indicator=1
#             else: 
#                 g_indicator=0
#         else:
#             if x[0][8]=='I':
#                 if x[1][1]=='H':
#                     r_indicator=1
#                 else: 
#                     r_indicator=0
#             else:
#                 if x[1][1]=='H':
#                     r_led=1
#                 else: 
#                     r_led=0   
#     print([g_indicator,r_indicator,r_led])      