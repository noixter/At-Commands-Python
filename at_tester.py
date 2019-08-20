#!/urs/bin/env python3

import serial
import time
# para enviar el Ctrl-Z
from curses import ascii

#modulo.open()
NET = False
IN_COMMANDS = ['AT+CIPSEND=0,','AT+CHTTPACT']

def reading():
    global modulo
    datos = ''
    while modulo.inWaiting() > 0:
        time.sleep(0.5)
        datos += modulo.readline().decode()
    return datos

def setup_module():
    modulo = serial.Serial('/dev/ttyUSB2')
    modulo.reset_input_buffer()
    modulo.reset_input_buffer()
    if modulo.isOpen():
        print ('Serial port Available')
        return modulo
    else:
        return print ('Serial port not Available')

def write_command(command):
    global modulo
    global NET
    try:
        if not NET:
            commando = ('{}'.format(command) + '\r\n').encode()
            modulo.write(commando)
            print ('Command Write...')
        else:
            modulo.write(command)
    except serial.SerialException:
        print ('Something goes wront')

def net_command():
    global modulo
    global NET
    executing = True
    while executing is True:
        print ('Write HTTP Petition')
        print ('Write \'SEND\' to go out')
        command = capture_command()
        if command != 'SEND':
            commando = ('{}'.format(command) + '\r\n').encode()
            modulo.write(commando)
        else:
            print ('Sending...')
            modulo.write(('\r\n').encode())
            modulo.write(('\r\n').encode())
            modulo.write(chr(26).encode())
            executing = False
            NET = False

def capture_command():
    global modulo
    global NET
    print ('Write the AT Command you want! ')
    command = input('>>> ')
    if NET:
        return command
    else:
        return command.upper()

def validating(command):
    global NET
    global IN_COMMANDS

    ingress = [comm for comm in IN_COMMANDS if comm in command]
    if ingress:
        NET = True
    else:
        NET = False
    

def closing_port():
    global modulo
    print ('Closing Port, Thank You')
    modulo.close()
    if modulo.isOpen():
        modulo.close()
    else:
        pass

def _welcome():
    print ('WELCOME SERIAL AT COMMAND SIM5360E COMMUNICATOR')
    print ('*' * 50)
    print ('Let\'s Begin')
    print ('Write \'EXIT\' for go out')

if __name__=='__main__':
   _welcome()
   modulo = setup_module()
   exit = True
   while exit is True :
       info = capture_command()
       if info != 'EXIT':
          validating(info)
          if NET:
              command = ('{}'.format(info) + '\r\n').encode()
              write_command(command)
              net_command()
              time.sleep(1)
              read = reading()
              print (read)
          else:
       	      write_command(info)
              time.sleep(1)
              read = reading()
              print(read)
       else:
           closing_port()
           exit = False
