from melsecNet import MelsecNet
from pprint import pprint
import json, sys


def main():
    # step#0 : load line/machine config with json
    baseInfo = json.load(open('machinesInfo.json'))
    machines = baseInfo.keys()

    for v in baseInfo:
        print baseInfo[v]
    # for v in machines:
    #     print v
    #     print jsonInfo[v]

    # step#1: load main window
    # step#2 : generate New instacne for machines
    # step#3 : monitoring bit for each machine

    # plc = MelsecNet(baseInfo[machines[0]])
    # result = plc.openMelsecNet()
    # if result != 0:
    #     print "melsec open error# " + str(result) + " >> " + baseInfo[machines[0]]["nick"]
    #     print plc.channel, plc.network, plc.station, hex(plc.startAddress), plc.length
    #     # ReSetBoard()
    #     # ReadBlock_B()
    #     plc.writeBlock()
    #     # weadBlock_W(enmValueTypes.ASC)
    #     # for a in readBlock_W(enmValueTypes.I2):
    #     #     print a
    #     # setBit()
    #     # resetBit()
    #     plc.closeMelsecNet()

if __name__ == '__main__':
    main()