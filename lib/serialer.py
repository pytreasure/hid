import serial
import time
import scripts.koei_sango.process as koei_sango
import scripts.pop_kart.process as pop_kart


def init(port, script):
    print(" - script:" + script)  # 设备端口
    print(" - port:" + port)  # 设备端口
    try:
        com = serial.Serial(port, 9600, timeout=1)
    except serial.serialutil.SerialException as e:
        print(" - Error:" + repr(e))
        return
    print(" - baud_rate:" + str(com.baudrate))  # 波特率
    print(" - byte_size:" + str(com.bytesize))  # 比特大小
    print(" - break_condition:" + str(com.break_condition))  # 校验位

    if com.isOpen():
        print(" - status:OK")
    else:
        print(" - status:FAIL")
        return

    # 执行对应的脚本
    eval(script + ".Run(com)")
