#-*-coding:utf-8-*-
from ctypes import *
import sys
import string

addressMask = 0xFFF0

MNET    = c_int32() #path
channel = c_int32(151)
mode    = c_int32(-1)
network = c_int32(0)     #fixed >> Network number = 1 if test = 0
station = c_int32(0xFF)  #fixed >> Station number = 255 ECS own
devType = c_int32(23) #DevB = 23, DevW = 24
devNo   = c_int32(0x0C00 & addressMask)   #start address
length  = c_ushort(64) # byte *2
rx      = (c_ushort * 32)() # read buffer
preRx   = (c_ushort * 32)() # backup pre values

melsec  = WinDLL('Mmscl32.dll')            #stdcall
# melsec = cdll.LoadLibrary('Mmscl32.dll') #cdecl
_mdOpen = melsec['mdOpen']
_mdOpen.restype = c_ushort
_mdOpen.argtypes = [c_int32, c_int32, POINTER(c_int32)]

_mdBdRst = melsec['mdBdRst']
_mdBdRst.restype = c_ushort
_mdBdRst.argtypes = [c_int32]

_mdReceiveEx = melsec['mdReceiveEx']
_mdReceiveEx.restype = c_int32
_mdReceiveEx.argtypes = [c_int32, c_int32, c_int32, c_int32, c_int32, POINTER(c_ushort), POINTER(c_ushort)]

_mdSendEx = melsec['mdSendEx']
_mdSendEx.restype = c_int32
_mdSendEx.argtypes = [c_int32, c_int32, c_int32, c_int32, c_int32, POINTER(c_ushort), POINTER(c_ushort)]

_mdDevSetEx = melsec['mdDevSetEx']
_mdDevSetEx.restype = c_int32
_mdDevSetEx.argtypes = [c_int32, c_int32, c_int32, c_int32, c_int32]

_mdDevRstEx = melsec['mdDevRstEx']
_mdDevRstEx.restype = c_int32
_mdDevRstEx.argtypes =  [c_int32, c_int32, c_int32, c_int32, c_int32]

_mdClose = melsec['mdClose']
_mdClose.restype = c_ushort
_mdClose.argtypes = [c_int32]

def OpenMelsecNet():
    result = _mdOpen(channel, mode, byref(MNET))
    if (result != 0):
        print "mdOpen Error " + str(result) + '\n' + "Check Net#, St# >>  GoodBye App Exit"
    return result

def ReadBlock():
    result = _mdReceiveEx(MNET, network, station, devType, devNo, byref(length), rx)
    if (result != 0):
        print "mdReceiveEx Error " + str(result)
    else:
        for i, r in enumerate(rx):
            print i, r ^ preRx[i]
            # print i, string.zfill(bin(r)[2:],16)
        preRx = rx # bit status backup
    return result

def WriteBlock():
    result = _mdDevSetEx(MNET, network, station, devType, devNo, byref(length), rx)
    if (result != 0):
        print "mdDevSetEx Error " + str(result)
    return result
    

def CloseMelsecNet():
    result = _mdClose(MNET)

def main():
    if OpenMelsecNet() == 0:
        ReadBlock()
        CloseMelsecNet()

if __name__ == '__main__':
    main()