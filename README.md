# At-Commands-Python
Python module for at commands SIM5360 functions (In working)

at_commands.py consolides function for works with SIM5360e module.

Other modules are for test purpose only and can't make anything with at_commands.py

Import module and create anobject with the same name:

E.g module = at_commands.setup() # for create a serial module preconfigurated for operates the SIM5360e

Please Examine functions:

  - setup()
  - set_ipaddres()
  - send_post()
  
Other functions like _valid_ip() and _read_line() are private and works only inside of at_commands.py
