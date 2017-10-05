from ctypes import *
import string


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)


class MelsecNet(object):
    """Mmscl32 Warpper Class"""
    ADDRESS_MASK = 0xFFF0  # address must divide 0xF is 0
    MODE = -1 # No mode set

    network = 0 # fixed >> Network number = 1 if test = 0
    station = 0xFF # fixed >> Station number = 255 ECS own
    mnet = c_int32() # path
    devAddress = 0x0C00 & ADDRESS_MASK # start address
    length = c_ushort(4) # byte *2= 16 bit = 1 word
    rx = (c_ushort * 2)() # read buffer
    preRx = (c_ushort * 64)() # backup pre values

    enmDeviceTypes = enum(
        DevX=1,
        DevY=2,
        DevD=13,
        DevZ=20,
        DevR=22,
        DevB=23,
        DevW=24)
    enmChannels = enum(MNET1=151, MNET2=152, MNET3=153, MNET4=154)
    enmValueTypes = enum(ASC=0, I2=1, I4=2)

    def __init__(self):
        self.melsecLib = WinDLL('Mmscl32.dll')  # stdcall

        self.mdOpen = self.melsecLib['mdOpen']
        self.mdOpen.restype = c_ushort
        self.mdOpen.argtypes = [c_int32, c_int32, POINTER(c_int32)]

        self.mdBdRst = self.melsecLib['mdBdRst']
        self.mdBdRst.restype = c_ushort
        self.mdBdRst.argtypes = [c_int32]

        self.mdReceiveEx = self.melsecLib['mdReceiveEx']
        self.mdReceiveEx.restype = c_int32
        self.mdReceiveEx.argtypes = [
            c_int32,
            c_int32,
            c_int32,
            c_int32,
            c_int32,
            POINTER(c_ushort),
            POINTER(c_ushort)]

        self.mdSendEx = self.melsecLib['mdSendEx']
        self.mdSendEx.restype = c_int32
        self.mdSendEx.argtypes = [
            c_int32,
            c_int32,
            c_int32,
            c_int32,
            c_int32,
            POINTER(c_ushort),
            POINTER(c_ushort)]

        self.mdDevSetEx = self.melsecLib['mdDevSetEx']
        self.mdDevSetEx.restype = c_int32
        self.mdDevSetEx.argtypes = [c_int32, c_int32, c_int32, c_int32, c_int32]

        self.mdDevRstEx = self.melsecLib['mdDevRstEx']
        self.mdDevRstEx.restype = c_int32
        self.mdDevRstEx.argtypes = [c_int32, c_int32, c_int32, c_int32, c_int32]

        self.mdClose = self.melsecLib['mdClose']
        self.mdClose.restype = c_ushort
        self.mdClose.argtypes = [c_int32]

    def openMelsecNet(self):
        result = self.mdOpen(self.enmChannels.MNET1, self.MODE, byref(self.mnet))
        if (result != 0):
            print "mdOpen Error " + str(result) + '\n' + "Check Net#, St# >>  GoodBye App Exit"
        return result

    def readBlock_B(self):   # monitoring loop
        result = mdReceiveEx(
            self.mnet,
            self.network,
            self.station,
            self.enmDeviceTypes.DevB,
            self.devAddress,
            byref(self.length),
            self.rx)
        if (result != 0):
            print "ReadBlock_B Error " + str(result)
        else:
            for i, r in enumerate(rx):
                # print i, r ^ preRx[i] # xor >> bitChange
                print hex(self.devAddress + (i * 0x10)), string.zfill(bin(r)[2:], 16)
            # preRx = rx # bit status backup
        return result

    def readBlock_W(self, valueType):
        result = mdReceiveEx(
            self.mnet,
            self.network,
            self.station,
            self.enmDeviceTypes.DevW,
            self.devAddress,
            byref(self.length),
            self.rx)
        if (result != 0):
            print "ReadBlock_W Error " + str(result)
            return (lambda: None, lambda: '')[self.enmValueTypes.ASC == valueType]()

        if valueType == self.enmValueTypes.ASC:
            strValue = ''
            for i, r in enumerate(rx):
                # print hex(devAddress + i), r, chr(r)
                strValue += chr(r)
            return strValue
        else:
            return rx

    def writeBlock(self):
        # rx[0]=123
        # rx[1]=321
        result = mdSendEx(
            self.mnet,
            self.network,
            self.station,
            self.enmDeviceTypes.DevW,
            self.devAddress,
            byref(self.length),
            self.rx)
        if (result != 0):
            print "WriteBlock Error " + str(result)
        return result

    def resetBoard(self):
        result = self.mdBdRst(self.mnet)
        return result

    def setBit(self):
        result = self.mdDevSetEx(
            self.mnet,
            self.network,
            self.station,
            self.enmDeviceTypes.DevB,
            self.devAddress)
        return result

    def resetBit(self):
        result = self.mdDevRstEx(
            self.mnet,
            self.network,
            self.station,
            self.enmDeviceTypes.DevB,
            self.devAddress)
        return result

    def closeMelsecNet(self):
        result = self.mdClose(self.mnet)
        return result


def main():
    plc = MelsecNet()
    plc.openMelsecNet()
    print plc.enmChannels.MNET1
    print plc.ADDRESS_MASK
    print plc.MODE


if __name__ == '__main__':
    main()
