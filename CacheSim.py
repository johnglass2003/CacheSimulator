import math
from timeit import default_timer as timer
import matplotlib.pyplot as plt
#------------------------------------------------Table Line-------------------------------------------------------#
class tableLine:
    def __init__(self, i, s, t, c):
        self.index = i
        self.set = s
        self.tag = t
        self.counter = c
    def hit(self):
        self.counter += 1
    def setTag(self, newTag):
        self.tag = newTag
#------------------------------------------------Direct Mapped Cache-------------------------------------------------------#
class directMappedCache:
    def __init__(self, size, lineSize):
        self.size = size
        self.lineSize = lineSize
        self.linesPerSet = 1
        self.numberOfLines = size // lineSize
        self.table = []
        for i in range(self.numberOfLines):
            self.table.append(tableLine(i, i, None, 0))

    def access(self,address):
        binary_string = bin(int(address,16))[2:].zfill(29)
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        lineSize = int(math.log(self.numberOfLines, 2))
        
        tag = binary_string[:(len(binary_string) - indexSize)]     
        line = binary_string[(len(binary_string) - indexSize):(len(binary_string) - indexSize + lineSize)]
        offset = binary_string[(len(binary_string) - offsetSize):]

        tag = int(tag, 2)
        line = int(line, 2)

        if self.table[line].tag == tag:
            self.table[line].hit()
            return 'Hit'
        else:
            self.table[line].setTag(tag)
            return 'Miss'
#------------------------------------------------Fully Associative Fifo Cache-------------------------------------------------------#
class fullyAssociativeCacheFifo:
    def __init__(self, size, lineSize):
        self.size = size
        self.lineSize = lineSize
        self.numberOfLines = size // lineSize
        self.table = []
        for i in range(self.numberOfLines):
            self.table.append(tableLine(i, 0, None, 0))

    def access(self,address):
        binary_string = bin(int(address,16))[2:].zfill(29)
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        
        tag = binary_string[:(len(binary_string) - indexSize)]       
        offset = binary_string[(len(binary_string) - offsetSize):]

        tag = int(tag, 2)

        for l in self.table:
            if l.tag == tag:
                l.hit()
                return 'Hit'
        for l in self.table:
            if l.tag is None:
                l.setTag(tag)
                return 'Miss'
        self.table[0].setTag(tag)
        return 'Miss' 
#------------------------------------------------Fully Associative Lru Cache-------------------------------------------------------#
class fullyAssociativeCacheLru:
    def __init__(self, size, lineSize):
        self.size = size
        self.lineSize = lineSize
        self.numberOfLines = size // lineSize
        self.table = []
        for i in range(self.numberOfLines):
            self.table.append(tableLine(i, 0, None, 0))

    def access(self,address):
        binary_string = bin(int(address,16))[2:].zfill(29)
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        
     
        
        tag = binary_string[:(len(binary_string) - indexSize)]       
        offset = binary_string[(len(binary_string) - offsetSize):]

        tag = int(tag, 2)

        lowestCount = 9999999
        lowestCountIndex = -1
        for i in range(len(self.table)):
            l = self.table[i]
            if l.tag == tag:
                l.hit()
                return 'Hit'
            if l.counter < lowestCount:
                lowestCount = l.counter
                lowestCountIndex = i
        for l in self.table:
            if l.tag is None:
                l.setTag(tag)
                return 'Miss'
        self.table[lowestCountIndex].setTag(tag)
        return 'Miss' 
#------------------------------------------------Set Associative Fifo Cache-------------------------------------------------------#
class setAssociativeCacheFifo:
    def __init__(self, size, lineSize, linesPerSet):
        self.size = size
        self.lineSize = lineSize
        self.linesPerSet = linesPerSet
        self.numberOfLines = size // lineSize
        self.numberOfSets = self.numberOfLines / self.linesPerSet
        
        self.table = []
        for i in range(self.numberOfLines):
            self.table.append(tableLine(i, (i//self.linesPerSet), None, 0))

    def access(self,address):
        binary_string = bin(int(address,16))[2:].zfill(29)
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        setSize = int(math.log(self.numberOfSets,2))
        
        
        
        tag = binary_string[:(len(binary_string) - indexSize)]  
        s = binary_string[(len(binary_string) - indexSize):(len(binary_string) - indexSize + setSize)]     
        offset = binary_string[(len(binary_string) - indexSize + setSize):]

        tag = int(tag, 2)
        s = int(s, 2)

        startingIndex = s * self.linesPerSet

        for i in range(self.linesPerSet):
            if self.table[startingIndex + i].tag == tag:
                self.table[startingIndex + i].hit()
                return 'Hit'     
        for l in self.table:
            if l.tag is None:
                l.setTag(tag)
                return 'Miss'
        self.table[0].setTag(tag)
        return 'Miss' 

#------------------------------------------------Set Associative Fifo Cache-------------------------------------------------------#
class setAssociativeCacheLru:
    def __init__(self, size, lineSize, linesPerSet):
        self.size = size
        self.lineSize = lineSize
        self.linesPerSet = linesPerSet
        self.numberOfLines = size // lineSize
        self.numberOfSets = self.numberOfLines / self.linesPerSet
        
        self.table = []
        for i in range(self.numberOfLines):
            self.table.append(tableLine(i, (i//self.linesPerSet), None, 0))

    def access(self,address):
        binary_string = bin(int(address,16))[2:].zfill(29)
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        setSize = int(math.log(self.numberOfSets,2))
        
    
        
        tag = binary_string[:(len(binary_string) - indexSize)]  
        s = binary_string[(len(binary_string) - indexSize):(len(binary_string) - indexSize + setSize)]     
        offset = binary_string[(len(binary_string) - indexSize + setSize):]

        tag = int(tag, 2)
        s = int(s, 2)

        startingIndex = s * self.linesPerSet

        lowestCount = 9999999
        lowestCountIndex = -1

        for i in range(self.linesPerSet):
            if self.table[startingIndex + i].tag == tag:
                self.table[startingIndex + i].hit()
                return 'Hit'     
            if self.table[startingIndex + i].counter < lowestCount:
                lowestCount = self.table[startingIndex + i].counter
                lowestCountIndex = i
        for l in self.table:
            if l.tag is None:
                l.setTag(tag)
                return 'Miss'
        self.table[lowestCountIndex].setTag(tag)
        return 'Miss' 

dMC1 = directMappedCache(512, 64)
dMC2 = fullyAssociativeCacheFifo(512, 64)
dMC3 = fullyAssociativeCacheLru(512, 64)
dMC4 = setAssociativeCacheFifo(512, 64, 2)
dMC5 = setAssociativeCacheLru(512, 64, 2)

dMC1Times = []
dMC2Times = []
dMC3Times = []
dMC4Times = []
dMC5Times = []

t1 = 0
t2 = 0
t3 = 0
t4 = 0
t5 = 0

accessNums = [512,1024, 2048, 4096, 8192]

f = open('gcc.trace') # Open file on read mode
lines = f.read().splitlines() # List with stripped line-breaks
f.close() # Close file

for line in lines:
    if len(line) < 2:
        continue
    lineSplit = line.split()
    start = timer()
    dMC1.access(lineSplit[1][2:])
    end = timer()
    t1 += (end - start)

    start = timer()
    dMC2.access(lineSplit[1][2:])
    end = timer()
    t2 += (end - start)

    start = timer()
    dMC3.access(lineSplit[1][2:])
    end = timer()
    t3 += (end - start)

    start = timer()
    dMC4.access(lineSplit[1][2:])
    end = timer()
    t4 += (end - start)

    start = timer()
    dMC5.access(lineSplit[1][2:])
    end = timer()
    t5 += (end - start)

dMC1 = directMappedCache(1024, 64)
dMC2 = fullyAssociativeCacheFifo(1024, 64)
dMC3 = fullyAssociativeCacheLru(1024, 64)
dMC4 = setAssociativeCacheFifo(1024, 64, 2)
dMC5 = setAssociativeCacheLru(1024, 64, 2)

dMC1Times.append(t1)
dMC2Times.append(t2)
dMC3Times.append(t3)
dMC4Times.append(t4)
dMC5Times.append(t5)

t1 = 0
t2 = 0
t3 = 0
t4 = 0
t5 = 0

for line in lines:
    lineSplit = line.split()

    start = timer()
    dMC1.access(lineSplit[1][2:])
    end = timer()
    t1 += (end - start)

    start = timer()
    dMC2.access(lineSplit[1][2:])
    end = timer()
    t2 += (end - start)

    start = timer()
    dMC3.access(lineSplit[1][2:])
    end = timer()
    t3 += (end - start)


    start = timer()
    dMC4.access(lineSplit[1][2:])
    end = timer()
    t4 += (end - start)


    start = timer()
    dMC5.access(lineSplit[1][2:])
    end = timer()
    t5 += (end - start)
    

dMC1 = directMappedCache(2048, 64)
dMC2 = fullyAssociativeCacheFifo(2048, 64)
dMC3 = fullyAssociativeCacheLru(2048, 64)
dMC4 = setAssociativeCacheFifo(2048, 64, 2)
dMC5 = setAssociativeCacheLru(2048, 64, 2)

dMC1Times.append(t1)
dMC2Times.append(t2)
dMC3Times.append(t3)
dMC4Times.append(t4)
dMC5Times.append(t5)

t1 = 0
t2 = 0
t3 = 0
t4 = 0
t5 = 0

for line in lines:
    lineSplit = line.split()

    start = timer()
    dMC1.access(lineSplit[1][2:])
    end = timer()
    t1 += (end - start)

    start = timer()
    dMC2.access(lineSplit[1][2:])
    end = timer()
    t2 += (end - start)
    

    start = timer()
    dMC3.access(lineSplit[1][2:])
    end = timer()
    t3 += (end - start)
    

    start = timer()
    dMC4.access(lineSplit[1][2:])
    end = timer()
    t4 += (end - start)
    

    start = timer()
    dMC5.access(lineSplit[1][2:])
    end = timer()
    t5 += (end - start)
    

dMC1 = directMappedCache(4096, 64)
dMC2 = fullyAssociativeCacheFifo(4096, 64)
dMC3 = fullyAssociativeCacheLru(4096, 64)
dMC4 = setAssociativeCacheFifo(4096, 64, 2)
dMC5 = setAssociativeCacheLru(4096, 64, 2)

dMC1Times.append(t1)
dMC2Times.append(t2)
dMC3Times.append(t3)
dMC4Times.append(t4)
dMC5Times.append(t5)

t1 = 0
t2 = 0
t3 = 0
t4 = 0
t5 = 0

for line in lines:
    lineSplit = line.split()

    start = timer()
    dMC1.access(lineSplit[1][2:])
    end = timer()
    t1 += (end - start)
    

    start = timer()
    dMC2.access(lineSplit[1][2:])
    end = timer()
    t2 += (end - start)
    

    start = timer()
    dMC3.access(lineSplit[1][2:])
    end = timer()
    t3 += (end - start)
    

    start = timer()
    dMC4.access(lineSplit[1][2:])
    end = timer()
    t4 += (end - start)
    

    start = timer()
    dMC5.access(lineSplit[1][2:])
    end = timer()
    t5 += (end - start)
    

dMC1 = directMappedCache(8192, 64)
dMC2 = fullyAssociativeCacheFifo(8192, 64)
dMC3 = fullyAssociativeCacheLru(8192, 64)
dMC4 = setAssociativeCacheFifo(8192, 64, 2)
dMC5 = setAssociativeCacheLru(8192, 64, 2)

dMC1Times.append(t1)
dMC2Times.append(t2)
dMC3Times.append(t3)
dMC4Times.append(t4)
dMC5Times.append(t5)

t1 = 0
t2 = 0
t3 = 0
t4 = 0
t5 = 0

for line in lines:
    lineSplit = line.split()

    start = timer()
    dMC1.access(lineSplit[1][2:])
    end = timer()
    t1 += (end - start)
    

    start = timer()
    dMC2.access(lineSplit[1][2:])
    end = timer()
    t2 += (end - start)
    

    start = timer()
    dMC3.access(lineSplit[1][2:])
    end = timer()
    t3 += (end - start)


    start = timer()
    dMC4.access(lineSplit[1][2:])
    end = timer()
    t4 += (end - start)


    start = timer()
    dMC5.access(lineSplit[1][2:])
    end = timer()
    t5 += (end - start)


dMC1Times.append(t1)
dMC2Times.append(t2)
dMC3Times.append(t3)
dMC4Times.append(t4)
dMC5Times.append(t5)

t1 = 0
t2 = 0
t3 = 0
t4 = 0
t5 = 0

names = ['Direct Mapped', 'Fully Associative Fifo', 'Fully Associative Lru', 'Set Associative Fifo', 'Set Associative Lru']

plt.figure()
x1,x2,y1,y2 = plt.axis()
plt.axis((x1,x2,0,8))

plt.subplot(321)
plt.plot(accessNums, dMC1Times)
plt.subplot(322)
plt.plot(accessNums, dMC2Times)
plt.subplot(323)
plt.plot(accessNums, dMC3Times)
plt.subplot(324)
plt.plot(accessNums, dMC2Times)
plt.subplot(325)
plt.plot(accessNums, dMC3Times)
plt.suptitle('Categorical Plotting')
plt.show()