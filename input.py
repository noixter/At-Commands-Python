#!/usr/bin/env python 3

input_commands=['AT+CMGS','AT+CIPSEND=0,','AT+CHTTP']

command = input('Write a command: ')

found = [comm for comm in input_commands if comm in command]

if not found:
    print ('not founded')
else:
    print ('founded')
