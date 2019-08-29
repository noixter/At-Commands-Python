
import serial
import time
import re


def setup(port, baud = int('9600'), apn = 'internet.movistar.com.co'):
        """Configuration of principal components of a module SIM53XX
           opens a serial port and returns a serial object 
           please indicate a port and a baudrate,
           configure parameters like: GPRS Connection,
           Socket TCP and APN... APN Defualt = internet.movistar.com.co
           Baudrate Default = 9600"""
        try:
            module = serial.Serial('/dev/tty{}'.format(port.upper(), '{}'.format(baud)))
            time.sleep(0.1)
            if module.isOpen():
                print ('Serial Port Available')
            else:
                print ('Serial Port not Available')
        except serial.SerialException:
            print ('Something goes wrong')
            module.close()
        try:
            module.write('AT+CGATT=1\r\n'.encode())
            time.sleep(0.01)
            module.write(('AT+CGDCONT=1,\"IP\",\"{}\"\r\n').format(apn).encode())           
            time.sleep(0.01)
            module.write(('AT+CGSOCKCONT=1,\"IP\",\"{}\"\r\n').format(apn).encode())
            module.write(('AT+CSOCKSETPN=1\r\n').encode())
            time.sleep(0.01)
            module.write(('AT+CGPSURL=\"supl.google.com:7276\"\r\n').encode())
            time.sleep(0.1)
            module.write(('AT+CGPSSSL=1\r\n').encode())
            time.sleep(0.1)
            #module.write(('AT+CGPS=1,3\r\n').encode())
            #time.sleep(0.2)
            #if _valid_gps(module):
            #    print ('GPS configurated')
            #else:
            #    print ('GPS not configurated')
            print ('SIM53XX Configurated!')
        except serial.SerialException:
            print ('Something failed during configuration\rPlase try again...')

        return module

def set_ipaddress(modulo):
        """Configuration of NET SOCKET and IPADDR
        Parameters: Serial Object"""

        print ('Configuring IP address...')

        modulo.write('AT+NETOPEN\r\n'.encode())

        if _valid_net(modulo):        
            try:
                modulo.write('AT+IPADDR\r\n'.encode())
                time.sleep(0.1)
            except serial.SerialException:
                print ('... Whitout IP address, try again')
            if _valid_ip(modulo):
                print ('IP address configurated')
            else:
                print ('IP not configurated')
        else:
            print ('Net Already configurated')
        
        data = _read_line(modulo)
        return data

def send_post(data, serial_object, host, url):
       """Send HTTP petition POST to indicated host
       parameters: data = formated JSON
       serial_object = serial module
       host = ip address from remote host
       url = web resource
       """
       datalen = len(data) + 4
        
       if _open_serv(host, serial_object):
            try:
                serial_object.write(('AT+CIPSEND=0,\r\n').encode())
                time.sleep(0.5)
                serial_object.write(('POST {} HTTP/1.1\r\n').format(url).encode())
                serial_object.write(('Host: {}\r\n').format(host).encode())
                serial_object.write(('Content-Type: application/json\r\n').encode())       
                serial_object.write(('Accept: */*\r\n').encode())
                serial_object.write(('Content-Length: {}\r\n').format(datalen).encode())
                serial_object.write(('\r\n').encode())
                serial_object.write(('\r\n').encode())
                serial_object.write(('{}\r\n').format(data).encode())
                serial_object.write(('\r\n').encode())
                serial_object.write(('\r\n').encode())
                serial_object.write(chr(26).encode())
                pat = re.compile('\+IPCLOSE: 0,1')
                if _valid_send(serial_object, pat):
                    print ('Data Send')
                else:
                    print ('Cannot send data')
            except serial.SerialException:
                print ('Something goes wrong')

def get_gpscoors(modulo):
    modulo.write('AT+CGPSHOT\r\n'.encode())
    time.sleep(0.1)
    gps = ''
    lat = 0
    lon = 0
    search = False
    pat = re.compile('\+CAGPSINFO:')
    pat1 = re.compile('([0-9]+),(-[0-9]+)')
    while not search:
        while modulo.inWaiting() > 0:
            gps += modulo.readline().decode()
            print ('Obtaining GPS Coordenates')
            if pat.search(gps):
                search = True

    print (gps)
    match = pat1.search(gps)
    if match:
        lat = int(match.group(1))
        lon = int(match.group(2))
        
    lat /= 100000000
    lon /= 100000000

    return lat,lon
 
def triangulation(modulo):
    modulo.write('AT+CASSISTLOC=1\r\n'.encode())
    time.sleep(0.1)
    pat = re.compile('([0-9]+.[0-9]+),-([0-9]+.[0-9]+)')
    pat1 = re.compile('\+CASSISTLOC:')
    search = False
    res = ''
    print ('Calculating...')
    while not search:
        while modulo.inWaiting() > 0:
            res += modulo.readline().decode()
            if pat1.search(res):
                search = True

    match = pat.search(res)
    if match:
        lat = float(match.group(1))
        lon = float(match.group(2))
    else:
        print ('No se encontraron Coordenadas')


    return lat, lon


                
def _read_line(modulo, pat = re.compile('')):
        import re
        res = ''
        while modulo.inWaiting() > 0:
            res += modulo.readline().decode()
            if pat.search(res):
                return res

def _valid_net(modulo):
            import re
            pattern = re.compile('\+NETOPEN: 0')
            pattern1 = re.compile('ERROR')
            result = ''
            time.sleep(0.5)
            searching = False
            while not searching:
                while modulo.inWaiting() > 0:
                    result += modulo.readline().decode()
                    print ('Leyendo...')
                    if pattern.search(result):
                       print ('True')
                       return True
                       searching = True
                    elif pattern1.search(result):
                       print ('False')
                       searching = True
                       return False


def _valid_ip(modulo):
            searching = False
            result = ''
            pat = re.compile('\+IPADDR:')
            pat1 = re.compile('\+IP ERROR:') 
            while not searching:
                while modulo.inWaiting() > 0:
                    result += modulo.readline().decode()
                    if pat.search(result):
                        searching = True
                        return True
                    elif pat1.search(result):
                        searching = True
                        return False
            else:
                print ('Network not open')
                return False


    
def _valid_send(serial_object, pat):
        res=''
        searching = False
        while not searching:
            while serial_object.inWaiting() > 0:
                res += serial_object.readline().decode()
                if pat.search(res):
                    return True
                    searching = True
        return False

def _valid_gps(modulo):
    res = ''
    searching = False
    pat = re.compile('\+CGPS: 0')
    while not searching:
        while modulo.inWaiting() > 0:
            res += modulo.readline().decode()
            print ('Configurando GPS...')
            if pat.search(res):
                searching = True
                return True
            else:
                continue

def _open_serv(host, serial_object):
        searching = False
        result = ''
        try:
            serial_object.write('AT+CIPOPEN=0,\"TCP\",\"{}\",80\r\n'.format(host).encode())
            time.sleep(0.3)
        except serial.SerialException:
            print ('Some Error Occur')
        
        pat = re.compile('\+CIPOPEN: 0,0')
        while not searching:
            while serial_object.inWaiting() > 0:
                result += serial_object.readline().decode()
                if pat.search(result):
                    print ('Opening...')
                    searching = True
                    return True


def _welcome():
        print ('WELCOME TO AT_COMMAND PROGRAM')
        print ('*' * 50)
        print ('Choose from the following option')
        print ('Write \'EXIT\' to go out')
        print ('[T]est AT Commands')
        print ('[C]onfigure GPRS')
        print ('[S]end Data')

def _capture_command():

        print ('Write a AT command')
        command = input('>>> ')
        return command.upper()


def _closing_module(modulo):

        if modulo.isOpen():
             print ('Closing Module')
             modulo.close()
        else:
             print ('Module already close')


if __name__ == '__main__':

    modulo = setup('USB2', '115000')
    print (modulo)
    data = set_ipaddress()
    print (data)
    print ('Terminado')



