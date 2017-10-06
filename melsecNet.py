from ctypes import *
import string


DEFAULT_OPEN_MODE = -1  # No mode set

MNET_PATH = c_int32()  # path

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

enmValueTypes = enum(ASC=0, I2=1, I4=2)
enmDeviceTypes = enum(DevX=1, DevY=2, DevD=13, DevZ=20, DevR=22, DevB=23, DevW=24)

melsecLib = WinDLL('Mmscl32.dll')  # stdcall
mdOpen = melsecLib['mdOpen']
mdClose = melsecLib['mdClose']
mdBdRst = melsecLib['mdBdRst']
mdReceiveEx = melsecLib['mdReceiveEx']
mdSendEx = melsecLib['mdSendEx']
mdDevSetEx = melsecLib['mdDevSetEx']
mdDevRstEx = melsecLib['mdDevRstEx']

mdOpen.restype = c_ushort
mdClose.restype = c_ushort
mdBdRst.restype = c_ushort
mdReceiveEx.restype = c_int32
mdSendEx.restype = c_int32
mdDevSetEx.restype = c_int32
mdDevRstEx.restype = c_int32

mdOpen.argtypes = [c_int32, c_int32, POINTER(c_int32)]
mdClose.argtypes = [c_int32]
mdBdRst.argtypes = [c_int32]
mdReceiveEx.argtypes = [c_int32, c_int32, c_int32, c_int32, c_int32, POINTER(c_ushort), POINTER(c_ushort)]
mdSendEx.argtypes = [c_int32, c_int32, c_int32, c_int32, c_int32, POINTER(c_ushort), POINTER(c_ushort)]
mdDevSetEx.argtypes = [c_int32, c_int32, c_int32, c_int32, c_int32]
mdDevRstEx.argtypes = [c_int32, c_int32, c_int32, c_int32, c_int32]


class MelsecNet(object):
    """Mmscl32 Warpper Class"""
    
    rx = (c_ushort * 2)()  # read buffer
    preRx = (c_ushort * 64)()  # backup pre values

    def __init__(self, plc):
        self.channel = plc["channel"]
        self.network = plc["network"]  # fixed >> Network number = 1 if test = 0
        self.station = plc["station"]  # 0xFF  # fixed >> Station number = 255 ECS own
        self.start_address = int(plc["start_address"], 16) & 0xFFF0  # ADDRESS_MASK = 0xFFF0  # address must divide 0xF is 0
        self.length = c_ushort(plc["read_length"])  # byte *2= 16 bit = 1 word

    def open_melsec(self):
        return mdOpen(self.channel, DEFAULT_OPEN_MODE, byref(MNET_PATH))

    def close_melsec(self):
        return mdClose(MNET_PATH)

    def reset_board(self):
        return mdBdRst(MNET_PATH)
    
    def set_bit(self, devAddress):
        return mdDevSetEx(MNET_PATH, self.network, self.station, enmDeviceTypes.DevB, devAddress)

    def reset_bit(self, devAddress):
        return mdDevRstEx(MNET_PATH, self.network, self.station, enmDeviceTypes.DevB, devAddress)

    def write_block(self, devAddress, wLength, data):
        return mdSendEx(MNET_PATH, self.network, self.station, enmDeviceTypes.DevW, devAddress, byref(wLength), data)

    def read_block(self, devAddress, wLength):  # read DevW
        length = c_ushort(wLength)
        rxbuffer = (c_ushort * length)()
        result = mdReceiveEx(MNET_PATH, self.network, self.station, enmDeviceTypes.DevW, devAddress, byref(length), rxbuffer)
        return result, rxbuffer

    def monitor_bit(self):   # bit monitoring loop
        result = mdReceiveEx(MNET_PATH, self.network, self.station, enmDeviceTypes.DevB, self.start_address, byref(self.length), self.rx)
        return result, self.rx


def main():
    pass
    # plc = MelsecNet(plc)
    # result = plc.openMelsecNet()
    # if result != 0:
    #     print "mdOpen Error " + str(result) + '\n' + "Check Network, Station"

if __name__ == '__main__':
    main()
