#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, serial

com = serial.Serial('COM3', 9600, timeout=1)

print(" - Hid control By hunzsig @date:20200521!")
print(" - Name:" + com.name)  # 设备名称
print(" - Port:" + com.port)  # 设备端口
print(" - BaudRate:" + str(com.baudrate))  # 波特率
print(" - ByteSize:" + str(com.bytesize))  # 比特大小
print(" - BreakCondition:" + str(com.break_condition))  # 校验位

if com.isOpen():
    print(" - Open:OK")
else:
    sys.exit()

print(" - Ready")

# com.close()
# 57 AB 00 02 08 00 00 04 00 00 00 00 00 10
# 57 AB 00 02 08 00 00 00 00 00 00 00 00 0C
