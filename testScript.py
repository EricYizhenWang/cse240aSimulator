from instruction import instruction
from activeList import activeList

from regMapTable import regMapTable

from simulator import simulator
from collections import deque

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
    
def testSimulator():
    sim = simulator()
    insr_queue = deque()
    insr_counter = 0
    for i in range(10):
        insr = instruction('I', [1, 1, 1], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1
        
        insr = instruction('A', [i+1, i+1, i+1], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1
        
    sim.setInsrSet(insr_queue)
    for i in range(10):
        print 'clock index:', i
        sim.oneClock()
