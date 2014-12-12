from instruction import instruction
from activeList import activeList

from regMapTable import regMapTable
def testActiveList_1():
    a = activeList()
    i1 = instruction('I', [], 0)
    i2 = instruction('L', [], 1)
    a.addInstruction(i1)
    a.addInstruction(i2)
    a.graduateInstruction()
    print len(a.getContent())
    a.setInsrDoneBit(i2)
    a.graduateInstruction()
    print len(a.getContent())
    a.setInsrDoneBit(i1)
    a.graduateInstruction()
    print len(a.getContent())
    a.graduateInstruction()
    print len(a.getContent())
    
def testRegTable_1():
    reg_map = regMapTable()
    print reg_map.getNumFreeReg()
    for i in range(32):
        reg_map.assignNewMapping(1)
    print reg_map.getNumFreeReg()
    for i in range(32):
        reg_map.assignNewMapping(2)
    print reg_map.getNumFreeReg
    
    print reg_map.getMapping(1).getTag()
    print reg_map.getMapping(2).getTag()
    

