
import serial
import time
import re
import at_commands


modulo = serial.Serial('/dev/ttyUSB2', 115200)
data = '{\"Name\": \"Mic-6814\", \"CO\": \"0.14\", \"NO2\": \"0.01\", \"NH3\": \"0.03\",\"lat\":"0",\"lon\":\"1\"}'
#sSerie.open()
try:
    #com = 'AT+IPADDR'
    modulo.write('AT+CIPOPEN=0,"TCP","104.154.21.179",80\r\n'.encode())
    time.sleep(2)
    modulo.write(('AT+CIPSEND=0,\r\n').encode())
    time.sleep(0.5)
    modulo.write('POST /sensors HTTP/1.1\r\n'.encode())
    modulo.write('Host: 104.154.21.179\r\n'.encode())
    modulo.write('Content-Type: application/json\r\n'.encode())
    modulo.write(('Accept: */*\r\n').encode())
    modulo.write('Content-Length: {}\r\n'.format(len(data)+4).encode())
    modulo.write('\r\n'.encode())
    modulo.write('\r\n'.encode())
    modulo.write('{}'.format(data).encode())
    modulo.write('\r\n'.encode())
    modulo.write('\r\n'.encode())
    modulo.write(chr(26).encode())
    print ('Enviando')
    datos= ''
    time.sleep(1)
    result = re.compile('\+IPCLOSE: 0,1')
    result2 = re.compile('ERROR')
    searching = False
    while not searching:
        while modulo.inWaiting() > 0:
            datos += modulo.readline().decode()
            if result.search(datos):
                print ('Conected')
                searching = True
            elif result2.search(datos):
                print ('NOT Conected')
                searching = True
                break
    print (datos)	

except ValueError:
    print ("Oops! se ha producido un error ...")

finally:
    modulo.close()
