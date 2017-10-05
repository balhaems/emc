#-*-coding:utf-8-*-
## autopep8 --in-place --aggressive --aggressive <filename>
from melsecNet import MelsecNet
import json

def main():
    # step#0 : load line/machine config with json
    # step#1: load main window
    # step#2 : generate New instacne for machines
    # step#3 : monitoring bit for each machine

    plc = MelsecNet()
    if plc.openMelsecNet() == 0:
        # ReSetBoard()
        # ReadBlock_B()
        plc.writeBlock()
        # weadBlock_W(enmValueTypes.ASC)
        # for a in readBlock_W(enmValueTypes.I2):
        #     print a
        # setBit()
        # resetBit()
        plc.closeMelsecNet()

if __name__ == '__main__':
    main()