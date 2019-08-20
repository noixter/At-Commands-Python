
import serial
import time
import re
import at_commands


modulo = serial.Serial('/dev/ttyUSB2', 115200)
#sSerie.open()
try:
    #com = 'AT+IPADDR'
    com = 'AT+IPADDR'
    command = ('{}'.format(com) + '\r\n').encode()
    print ('Enviando')
    datos= ''
    modulo.write(command)
    time.sleep(1)
    result = re.compile('\+IPADDR:')
    result2 = re.compile('ERROR')
    searching = False
    while not searching:
        while modulo.inWaiting() > 0:
            datos += modulo.readline().decode()
            if result.search(datos):
                print ('IP-')
                searching = True
            elif result2.search(datos):
                print ('NOT IP-')
                searching = True
                break
    print (datos)	

except ValueError:
    print ("Oops! se ha producido un error ...")

finally:
    modulo.close()
