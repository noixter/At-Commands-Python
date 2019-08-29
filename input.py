import pynmea2

msg = pynmea2.parse('$GPGGA,0439.690603,N,07404.012174,W,270819,204027.0,2549.4,,')
print (msg)
