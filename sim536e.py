import serial
import time
import re
import at_commands


modulo = at_commands.setup('USB2','115200')
data = at_commands.set_ipaddress(modulo)
lat, lon = at_commands.triangulation(modulo)
time.sleep(0.5)
datos = '{\"Name\": \"Mic-6814\", \"CO\": \"0.14\", \"NO2\": \"0.01\", \"NH3\": \"0.03\"}'
print (lat,lon)
print (len(datos))
at_commands.send_post(datos, modulo, 'iot-tech.co', '/sensors')
print (data)
#sSerie.open()
#try:
 #   com = 'AT+IPADDR'
    #com = 'AT+CIPOPEN=0,\"TCP\",\"190.147.52.171\",80'
  #  command = ('{}'.format(com) + '\r\n').encode()
   # print ('Enviando')
   # datos= ''
   # modulo.write(command)
   # time.sleep(1)
   # result = re.compile('\+IPADDR:')
    #searching = True
    #while modulo.inWaiting() > 0 and searching == True:
     #   datos += modulo.readline().decode()
      #  if result.search(datos):
      #      print ('terminado')
       #     searching = False

    #print (datos)
    #if result.search(datos):
     #   print ('Terminado')
    #else:
     #   print ('No encontrado')

#except ValueError:
#    print ("Oops! se ha producido un error ...")

#finally:
at_commands._closing_module(modulo)
