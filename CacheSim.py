import math
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
        self.table[lowestCountIndex].setTag(tag)
        return 'Miss' 
#------------------------------------------------Set Associative Fifo Cache-------------------------------------------------------#
class SetAssociativeCacheFifo:
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

f = open('read01.trace') # Open file on read mode
lines = f.read().splitlines() # List with stripped line-breaks
f.close() # Close file

dMC = fullyAssociativeCacheLru(512, 64)

for line in lines:
    lineSplit = line.split()
    print(dMC.access(lineSplit[1][2:]))

for l in dMC.table:
    print(l.index)
    print(l.tag)