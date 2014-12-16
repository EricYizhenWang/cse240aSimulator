from basicComponents import instruction, activeList, regMapTable
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
    
def testSimulator_1():
    sim = simulator()
    insr_queue = deque()
    insr_counter = 0
    for i in range(30):
        #insr = instruction('I', [1, 1, 1], insr_counter)
        #insr_queue.append(insr)
        #insr_counter = insr_counter+1
        
        insr = instruction('A', [i+1, i+1, i+1], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1
        
        insr = instruction('M', [i+1, i+1, i+1], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1        
        
    sim.setInsrSet(insr_queue)
    for i in range(50):
        print 'clock index:', i
        sim.oneClock()
        
def testSimulator_2():
    sim = simulator()
    insr_queue = deque()
    insr_counter = 0
    for i in range(10):
        #insr = instruction('I', [1, 1, 1], insr_counter)
        #insr_queue.append(insr)
        #insr_counter = insr_counter+1
        
        insr = instruction('A', [i+1, i+1, i+1], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1
        
        insr = instruction('M', [i+2, i+2, i+2], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1        
        
    insr = insr_queue[0]
    sim.setInsrSet(insr_queue)
    for i in range(20):
        print 'clock index:', i
        sim.oneClock()
        #print insr.getHistory()


def testSimulator_4():
    sim = simulator()
    insr_queue = deque()
    insr_counter = 0
    for i in range(2):
        insr = instruction('S', [1, 1, 10], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1
        
        insr = instruction('L', [1, 1, 1], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1
        
        insr = instruction('A', [i+1, i+1, i+1], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1
        
        insr = instruction('M', [i+2, i+2, i+2], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1        
        
    sim.setInsrSet(insr_queue)
    insr = insr_queue[0]
    for i in range(30):
        print 'clock index:', i
        sim.oneClock()
        #print insr.getHistory(), 'history 00'
        

def testSimulator_3():
    sim = simulator()
    insr_queue = deque()
    insr_counter = 0
    for i in range(100):
        insr = instruction('S', [1, 1, 10], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1
        
        insr = instruction('L', [1, 1, 1], insr_counter)
        insr_queue.append(insr)
        insr_counter = insr_counter+1     
        
    sim.setInsrSet(insr_queue)
    insr = insr_queue[0]
    for i in range(100):
        print 'clock index:', i
        sim.oneClock()
        #print insr.getHistory(), 'history 00'