import serial
import time
from scripts import demo


def init(port, baud_rate, timeout):
    print(" - port:" + port)  # 设备端口
    print(" - baud_rate:" + str(baud_rate))  # 波特率
    print(" - timeout:" + str(timeout))  # timeout
    try:
        com = serial.Serial(port, baud_rate, timeout=timeout)
    except serial.serialutil.SerialException as e:
        print(" - Error:" + repr(e))
        return
    print(" - byte_size:" + str(com.bytesize))  # 比特大小
    print(" - break_condition:" + str(com.break_condition))  # 校验位

    if com.isOpen():
        print(" - status:OK")
    else:
        print(" - status:FAIL")
        return

    demo.run(com)

    put = bytes([0x57, 0XAB, 0X00, 0X02, 0X08, 0X00, 0X00, 0X04, 0X00, 0X00, 0X00, 0X00, 0X00, 0X10])
    com.write(put)
    time.sleep(1)
    put = bytes([0X57, 0XAB, 0X00, 0X02, 0X08, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X0C])
    com.write(put)

# com.close()
# 57 AB 00 02 08 00 00 04 00 00 00 00 00 10
# 57 AB 00 02 08 00 00 00 00 00 00 00 00 0C
