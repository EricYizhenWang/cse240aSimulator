from instruction import instruction
from activeList import activeList
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

