from simulator import simulator
from collections import deque
from basicComponents import activeList, freeList, integerQueue, \
     regMapTable, register, instruction, ALU, insrBuffer, FPunit, FPqueue, addressQueue, SLunit

class interface:
    def __init__(self):
        self.insr_queue = deque()
        self.numInsr = 0
        self.finished_queue = deque()
        self.rawString = []
        self.l = 30
        
    def setNumInsr(self, num):
        self.numInsr = num
        
    def loadTestInsr(self, filename):
        f = open(filename, 'r')
        index = 0
        for line in f:
            #rawStr = f.readline()
            self.rawString.append(line.strip('\n'))
            l = line.split()
            insr_type = l[0]
            if (insr_type == 'I') or (insr_type == 'A') or (insr_type == 'M'):
                args = [int(l[3]), int(l[2]), int(l[1])]
            elif insr_type == 'S':
                args = [int(l[2]), int(l[1]), l[4]]
            elif insr_type == 'L':
                args = [int(l[2]), int(l[1]), l[4]]
            
            self.insr_queue.append(instruction(insr_type, args, index))
            index = index + 1
            
        self.setNumInsr(len(self.insr_queue))
        return len(self.insr_queue)
    
    def test(self):
        sim = simulator()
        #finished_insr = deque()
        sim.setInsrSet(self.insr_queue)
        #for i in range(10):
        i = 0
        #print self.numInsr
        while (len(self.finished_queue) < self.numInsr):
        #while i<10:
            print 'clock index:', i
            finished = sim.oneClock()
            if finished != None:
                for j in range(len(finished)):
                    self.finished_queue.append(finished[j])
            #print len(self.finished_queue), self.numInsr
            i = i+1
    
    def printInsrStats(self, filename):
        f = open(filename, 'w')
        for i in range(len(self.finished_queue)):
            l = self.rawString[i].split()
            insr = self.finished_queue[i]
            strToPrint = self.rawString[i] + ' '* (self.l - len(self.rawString[i]))
            insr_type = insr.getType()
            args = insr.getArgs()
            if (insr_type == 'I') or (insr_type == 'A') or (insr_type == 'M'):    
                strToAdd = l[1] + '(' + str(args[1].getTag()) + ')' +' '* 3 + l[2] + '(' + str(args[2].getTag()) + ')' + ' '* 3 + l[3] + '(' + str(args[0].getTag()) + ')'
            elif (insr_type == 'S'):
                strToAdd = l[1] + '(' + str(args[1].getTag()) + ')' +' '* 3 + l[2] + '(' + str(args[0].getTag()) + ')' +' '* 3+ l[3] + '(xx)'
            elif (insr_type == 'L'):
                strToAdd = l[1] + '(' + str(args[1].getTag()) + ')' + ' '* 3+ l[2] + '(' + str(args[0].getTag()) + ')' +' '* 3+ l[3] + '(xx)'
            elif (insr_type == 'B'):
                pass
            strToPrint = strToPrint + strToAdd + '\n'
            f.write(strToPrint)
        f.close()
            
    def printHistory(self, filename):
        f = open(filename, 'w')
        for i in range(len(self.finished_queue)):
            insr = self.finished_queue[i]
            strToPrint = self.rawString[i] + ' '* (self.l - len(self.rawString[i]))             
            history = insr.getHistory()
            for j in range(len(history)):
                strToPrint = strToPrint + history[j] + '|' + ' '
            strToPrint = strToPrint + '\n'
            #strToPrint = str(insr.getHistory()) + '\n'
            f.write(strToPrint)
            print insr.getHistory()
        f.close()
            
            
        