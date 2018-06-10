#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ptvsd
ptvsd.settrace(None, ('0.0.0.0', 18110))

from time import sleep
from random import random

def get_cpu_temp():
    cpu_temp_file = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = cpu_temp_file.read()
    cpu_temp_file.close()
    return float(cpu_temp)/1000

def measure_temp():
    """vcgencmd measure_temp"""
    print(get_cpu_temp())


def main():
    """docstring for main"""
    print("main start")
    ptvsd.wait_for_attach()
    for _ in range(0, 50):
        sleep(5)
        i = random()
        print(i)
        measure_temp()

    print("main done")
    
if __name__ == '__main__':
    main()