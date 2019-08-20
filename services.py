#!/usr/bin/env python3

import serial
import time
import re

HOST = '190.147.52.171'
URL = '/sensors'
NET = False

def setup_module():
    try:
        modulo = serial.Serial('/dev/ttyUSB2', 115200)
        if modulo.isOpen():
            print ('Serial Port Availabe')
        else: 
            print ('Serial Port not Open')
    except serial.SerialException:
        print ('Something goes Wrong, please validate serial port')
        modulo.close()

    return modulo

def setup_net():

    global HOST, NET

    print ('Configuring GPRS...')
    try:
        modulo.write(('AT+NETOPEN\r\n').encode())
        time.sleep(0.1)
        modulo.write(('AT+IPADDR\r\n').encode())
        time.sleep(0.1)
        if validating('\+IPADDR: '):
            print ('Open server')
            modulo.write(('AT+CIPOPEN=0,\"TCP\",\"{}\",80\r\n').format(HOST).encode())
            time.sleep(1)
            NET = True
        else:
            print ('Server not Open')
    except serial.SerialException:
        print ('GPRS configuring Failed')
        NET = False

def read_line():
    global modulo

    data = ''

    while modulo.inWaiting() > 0:
        data += modulo.readline().decode()

    return data

def send_data(data):
    global modulo
    global URL
    print ('sending data...')

    datalen = len(data) + 4

    print ('POST petition')

    try:
        modulo.write(('AT+CIPSEND=0,\r\n').encode())
        time.sleep(0.3)
        modulo.write(('POST {} HTTP/1.1\r\n').format(URL).encode())
        modulo.write(('Host: 190.147.52.171\r\n').encode())
        modulo.write(('Content-Type: application/json\r\n').encode())
        modulo.write(('Accept: */*\r\n').encode())
        modulo.write(('Content-Length: {}\r\n').format(datalen).encode())
        modulo.write(('\r\n').encode())
        modulo.write(('\r\n').encode())
        modulo.write(('{}').format(data).encode())
        modulo.write(('\r\n').encode())
        modulo.write(('\r\n').encode())
        modulo.write(chr(26).encode())
        time.sleep(0.5)
        if validating('\+IPCLOSE: 0,1'):
             print ('Data Sent')
             print ('*' * 50)
             print (read_line())
        else:
             print ('Some error Occur')
    except ValueError:
        print ('Something goes wrong')

def _welcome():
    print ('WELCOME TO AT_COMMAND PROGRAMM')
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


def _closing_module():
    global modulo

    if modulo.isOpen():
        print ('Closing Module')
        modulo.close()
    else:
        print ('Module already close')

def validating(res):
    global modulo

    datos = ''
    result = re.compile('{}'.format(res))
    searching = True
    while modulo.inWaiting() > 0 and searching == True:
        datos += modulo.readline().decode()
        if result.search(datos):
           return True
           searching = False
           print ('validado')

if __name__ == '__main__':
    _welcome()
    modulo = setup_module()
    executing = True
    while executing == True:
        comm = _capture_command()
        if comm == 'EXIT':
            _closing_module()
            executing = False
        elif comm == 'T':
            print ('Texting Commands!')
            comm1 = _capture_command()
            modulo.write(('{}'.format(comm1) + '\r\n').encode())
            time.sleep(0.1)
            print (read_line())
        elif comm == 'S':
            data = input('write the data you want to send: ')
            send_data(data)
        elif comm == 'C':
            if NET:
                print ('Net already configurated')
            else:
                print ('Configurating!')
                setup_net()
        else:
            print('Invalid Command')


