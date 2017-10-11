from melsecNet import MelsecNet
from pprint import pprint
import json


def main():
    # step#0 : load line/machine config with json
    baseInfo = json.load(open('machinesInfo.json'))
    machines = baseInfo.keys()

    # for v in baseInfo:
    #     print baseInfo[v]['bit_list']
    # for v in machines:
    #     print v
    #     print jsonInfo[v]

    # step#1: load main window
    # step#2 : generate New instacne for machines
    # step#3 : monitoring bit for each machine

    plc = MelsecNet(baseInfo[machines[0]])
    exec baseInfo['cim']['bit_list']['0x0C00'].encode('ascii', 'ignore')
    # result = plc.open_melsec()
    if result != 0:
        print "melsec open error# " + str(result) + " >> " + baseInfo[machines[0]]["nick"]
    #     print plc.channel, plc.network, plc.station, hex(plc.startAddress), plc.length
    #     # ReSetBoard()
    #     # ReadBlock_B()
    #     plc.writeBlock()
    #     # weadBlock_W(enmValueTypes.ASC)
    #     # for a in readBlock_W(enmValueTypes.I2):
    #     #     print a
    #     # setBit()
    #     # resetBit()
        plc.close_melsec()

if __name__ == '__main__':
    main()