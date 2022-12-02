import math
from timeit import default_timer as timer
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
        binary_string = bin(int(address,16))[2:]
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        lineSize = int(math.log(self.numberOfLines, 2))
        
        print(binary_string)
        
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
        binary_string = bin(int(address,16))[2:]
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        
        print(binary_string)
        
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
        binary_string = bin(int(address,16))[2:]
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        
        print(binary_string)
        
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
        binary_string = bin(int(address,16))[2:]
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        setSize = int(math.log(self.numberOfSets,2))
        
        print(binary_string)
        
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
        binary_string = bin(int(address,16))[2:]
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        setSize = int(math.log(self.numberOfSets,2))
        
        print(binary_string)
        
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

f = open('read01.trace') # Open file on read mode
lines = f.read().splitlines() # List with stripped line-breaks
f.close() # Close file

dMC1 = directMappedCache(512, 64)
dMC2 = fullyAssociativeCacheFifo(512, 64)
dMC3 = fullyAssociativeCacheLru(512, 64)
dMC4 = setAssociativeCacheFifo(512, 64, 2)
dMC5 = setAssociativeCacheLru(512, 64, 2)

for line in lines:
    lineSplit = line.split()

    start = timer()
    dMC1.access(lineSplit[1][2:])
    end = timer()
    print(end - start)

    start = timer()
    dMC2.access(lineSplit[1][2:])
    end = timer()
    print(end - start)

    start = timer()
    dMC3.access(lineSplit[1][2:])
    end = timer()
    print(end - start)

    start = timer()
    dMC4.access(lineSplit[1][2:])
    end = timer()
    print(end - start)

    start = timer()
    dMC5.access(lineSplit[1][2:])
    end = timer()
    print(end - start)

for l in dMC1.table:
    print(l.index)
    print(l.tag)
for l in dMC2.table:
    print(l.index)
    print(l.tag)
for l in dMC3.table:
    print(l.index)
    print(l.tag)
for l in dMC4.table:
    print(l.index)
    print(l.tag)
for l in dMC5.table:
    print(l.index)
    print(l.tag)