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
        self.hit = 0
        self.size = size
        self.lineSize = lineSize
        self.linesPerSet = 1
        self.numberOfLines = size // lineSize
        self.table = []
        for i in range(self.numberOfLines):
            self.table.append(tableLine(i, i, None, 0))

    def access(self,address):
        binary_string = bin(int(address,16))[2:].zfill(32)
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
            self.hit += 1
            return 'Hit'
        else:
            self.table[line].setTag(tag)
            return 'Miss'
#------------------------------------------------Fully Associative Fifo Cache-------------------------------------------------------#
class fullyAssociativeCacheFifo:
    def __init__(self, size, lineSize):
        self.hit = 0
        self.size = size
        self.lineSize = lineSize
        self.numberOfLines = size // lineSize
        self.table = []
        for i in range(self.numberOfLines):
            self.table.append(tableLine(i, 0, None, 0))

    def access(self,address):
        binary_string = bin(int(address,16))[2:].zfill(32)
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        
        tag = binary_string[:(len(binary_string) - indexSize)]       
        offset = binary_string[(len(binary_string) - offsetSize):]

        tag = int(tag, 2)

        for l in self.table:
            if l.tag == tag:
                l.hit()
                self.hit += 1
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
        self.hit = 0
        self.size = size
        self.lineSize = lineSize
        self.numberOfLines = size // lineSize
        self.table = []
        for i in range(self.numberOfLines):
            self.table.append(tableLine(i, 0, None, 0))

    def access(self,address):
        binary_string = bin(int(address,16))[2:].zfill(32)
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
                self.hit += 1
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
        self.hit = 0
        self.size = size
        self.lineSize = lineSize
        self.linesPerSet = linesPerSet
        self.numberOfLines = size // lineSize
        self.numberOfSets = self.numberOfLines / self.linesPerSet
        
        self.table = []
        for i in range(self.numberOfLines):
            self.table.append(tableLine(i, (i//self.linesPerSet), None, 0))

    def access(self,address):
        binary_string = bin(int(address,16))[2:].zfill(32)
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
                self.hit += 1
                return 'Hit'     
        for i in range(self.linesPerSet):
            if self.table[startingIndex + i].tag is None:
                self.table[startingIndex + i].setTag(tag)
                return 'Miss'
        self.table[startingIndex].setTag(tag)
        return 'Miss' 

#------------------------------------------------Set Associative Fifo Cache-------------------------------------------------------#
class setAssociativeCacheLru:
    def __init__(self, size, lineSize, linesPerSet):
        self.hit = 0
        self.size = size
        self.lineSize = lineSize
        self.linesPerSet = linesPerSet
        self.numberOfLines = size // lineSize
        self.numberOfSets = self.numberOfLines / self.linesPerSet
        
        self.table = []
        for i in range(self.numberOfLines):
            self.table.append(tableLine(i, (i//self.linesPerSet), None, 0))

    def access(self,address):
        binary_string = bin(int(address,16))[2:].zfill(32)
        offsetSize = int(math.log(self.lineSize, 2))
        indexSize = int(math.log(self.size, 2))
        setSize = int(math.log(self.numberOfSets,2))
        
    
        
        tag = binary_string[:(len(binary_string) - indexSize)]  
        s = binary_string[(len(binary_string) - indexSize):(len(binary_string) - indexSize + setSize)]     
        offset = binary_string[(len(binary_string) - setSize):]

        tag = int(tag, 2)
        s = int(s, 2)

        startingIndex = s * self.linesPerSet

        lowestCount = 9999999
        lowestCountIndex = -1

        for i in range(self.linesPerSet):
            if self.table[startingIndex + i].tag == tag:
                self.table[startingIndex + i].hit()
                self.hit += 1
                return 'Hit'     
            if self.table[startingIndex + i].counter < lowestCount:
                lowestCount = self.table[startingIndex + i].counter
                lowestCountIndex = i
        for i in range(self.linesPerSet):
            if self.table[startingIndex + i].tag is None:
                self.table[startingIndex + i].setTag(tag)
                return 'Miss'
        self.table[startingIndex + lowestCountIndex].setTag(tag)
        return 'Miss' 

c = 0

dMC1Times = []
dMC2Times = []
dMC3Times = []
dMC4Times = []
dMC5Times = []

directMiss = []
twoMiss= []
fourmiss = []
eightMiss = []

hr1 = []
hr2 = []
hr3 = []
hr4 = []
hr5 = []

accessNums = [256, 512, 1024, 2048]

associativityNums = ['One-Way', 'Two-Way', 'Four-Way', 'Eight-Way']

f = open('gcc.trace') # Open file on read mode
lines = f.read().splitlines() # List with stripped line-breaks
f.close() # Close file



dMC1 = directMappedCache(256, 32)
dMC2 = fullyAssociativeCacheFifo(256, 32)
dMC3 = fullyAssociativeCacheLru(256, 32)
dMC4 = setAssociativeCacheFifo(256, 32, 2)
dMC5 = setAssociativeCacheLru(256, 32, 2)

t1 = 0
t2 = 0
t3 = 0
t4 = 0
t5 = 0

for line in lines:
    c += 1
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

hr1.append(dMC1.hit / c)
hr2.append(dMC2.hit / c)
hr3.append(dMC3.hit / c)
hr4.append(dMC4.hit / c)
hr5.append(dMC5.hit / c)
    

dMC1 = directMappedCache(512, 32)
dMC2 = fullyAssociativeCacheFifo(512, 32)
dMC3 = fullyAssociativeCacheLru(512, 32)
dMC4 = setAssociativeCacheFifo(512, 32, 2)
dMC5 = setAssociativeCacheLru(512, 32, 2)

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

hr1.append(dMC1.hit / c)
hr2.append(dMC2.hit / c)
hr3.append(dMC3.hit / c)
hr4.append(dMC4.hit / c)
hr5.append(dMC5.hit / c)

dMC1 = directMappedCache(1024, 32)
dMC2 = fullyAssociativeCacheFifo(1024, 32)
dMC3 = fullyAssociativeCacheLru(1024, 32)
dMC4 = setAssociativeCacheFifo(1024, 32, 2)
dMC5 = setAssociativeCacheLru(1024, 32, 2)

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

hr1.append(dMC1.hit / c)
hr2.append(dMC2.hit / c)
hr3.append(dMC3.hit / c)
hr4.append(dMC4.hit / c)
hr5.append(dMC5.hit / c)

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



dMC1 = directMappedCache(2048, 32)
dMC2 = fullyAssociativeCacheFifo(2048, 32)
dMC3 = fullyAssociativeCacheLru(2048, 32)
dMC4 = setAssociativeCacheFifo(2048, 32, 2)
dMC5 = setAssociativeCacheLru(2048, 32, 2)

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
    
hr1.append(dMC1.hit / c)
hr2.append(dMC2.hit / c)
hr3.append(dMC3.hit / c)
hr4.append(dMC4.hit / c)
hr5.append(dMC5.hit / c)

dMC1Times.append(t1)
dMC2Times.append(t2)
dMC3Times.append(t3)
dMC4Times.append(t4)
dMC5Times.append(t5)







dMC1 = directMappedCache(512, 32)
dMC2 = setAssociativeCacheFifo(512, 32, 2)
dMC3 = setAssociativeCacheFifo(512, 32, 4)
dMC4 = setAssociativeCacheFifo(512, 32, 8)

for line in lines:
    lineSplit = line.split()
    dMC1.access(lineSplit[1][2:])
    dMC2.access(lineSplit[1][2:])
    dMC3.access(lineSplit[1][2:])
    dMC4.access(lineSplit[1][2:])

directMiss.append(1 - dMC1.hit / c)
twoMiss.append(1 - dMC2.hit / c)
fourmiss.append(1 - dMC3.hit / c)
eightMiss.append(1 - dMC4.hit / c)
dMC1 = directMappedCache(1024, 32)
dMC2 = setAssociativeCacheFifo(1024, 32, 2)
dMC3 = setAssociativeCacheFifo(1024, 32, 4)
dMC4 = setAssociativeCacheFifo(1024, 32, 8)

for line in lines:
    lineSplit = line.split()
    dMC1.access(lineSplit[1][2:])
    dMC2.access(lineSplit[1][2:])
    dMC3.access(lineSplit[1][2:])
    dMC4.access(lineSplit[1][2:])

directMiss.append(1 - dMC1.hit / c)
twoMiss.append(1 - dMC2.hit / c)
fourmiss.append(1 - dMC3.hit / c)
eightMiss.append(1 - dMC4.hit / c)
dMC1 = directMappedCache(2048, 32)
dMC2 = setAssociativeCacheFifo(2048, 32, 2)
dMC3 = setAssociativeCacheFifo(2048, 32, 4)
dMC4 = setAssociativeCacheFifo(2048, 32, 8)

for line in lines:
    lineSplit = line.split()
    dMC1.access(lineSplit[1][2:])
    dMC2.access(lineSplit[1][2:])
    dMC3.access(lineSplit[1][2:])
    dMC4.access(lineSplit[1][2:])

directMiss.append(1 - dMC1.hit / c)
twoMiss.append(1 - dMC2.hit / c)
fourmiss.append(1 - dMC3.hit / c)
eightMiss.append(1 - dMC4.hit / c)



names = ['Direct Mapped', 'Fully Associative Fifo', 'Fully Associative Lru', 'Set Associative Fifo', 'Set Associative Lru']

fig = plt.figure(0, figsize=(2, 6))
fig.tight_layout(pad=5.0)

ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)
ax3 = fig.add_subplot(323)
ax4 = fig.add_subplot(324)
ax5 = fig.add_subplot(325)

ax1.set_xlabel("Cache Size (Bytes)")
ax1.set_ylabel("Hit Rate (Hits / Total Accesses)")
ax2.set_xlabel("Cache Size (Bytes)")
ax2.set_ylabel("Hit Rate (Hits / Total Accesses)")
ax3.set_xlabel("Cache Size (Bytes)")
ax3.set_ylabel("Hit Rate (Hits / Total Accesses)")
ax4.set_xlabel("Cache Size (Bytes)")
ax4.set_ylabel("Hit Rate (Hits / Total Accesses)")
ax5.set_xlabel("Cache Size (Bytes)")
ax5.set_ylabel("Hit Rate (Hits / Total Accesses)")

ax1.set_title('Direct Mapped', y=1.0, pad=-14)
ax2.set_title('Fully Associative (FIFO)', y=1.0, pad=-14)
ax3.set_title('Fully Associative (LRU)', y=1.0, pad=-14)
ax4.set_title('Set Associative (FIFO)', y=1.0, pad=-14)
ax5.set_title('Set Associative (LRU)', y=1.0, pad=-14)

ax1.plot(accessNums, hr1)
ax2.plot(accessNums, hr2)
ax3.plot(accessNums, hr3)
ax4.plot(accessNums, hr4)
ax5.plot(accessNums, hr5)

print(hr1)
print(hr2)
print(hr3)
print(hr4)
print(hr5)

plt.suptitle('Hit Rate vs Cache Size')



#------------------------------------------------------#
fig = plt.figure(1, figsize=(2, 6))
fig.tight_layout(pad=5.0)

ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)
ax3 = fig.add_subplot(323)
ax4 = fig.add_subplot(324)
ax5 = fig.add_subplot(325)

ax1.set_xlabel("Cache Size (Bytes)")
ax1.set_ylabel("Total Access Time (Seconds)")
ax2.set_xlabel("Cache Size (Bytes)")
ax2.set_ylabel("Total Access Time (Seconds)")
ax3.set_xlabel("Cache Size (Bytes)")
ax3.set_ylabel("Total Access Time (Seconds)")
ax4.set_xlabel("Cache Size (Bytes)")
ax4.set_ylabel("Total Access Time (Seconds)")
ax5.set_xlabel("Cache Size (Bytes)")
ax5.set_ylabel("Total Access Time (Seconds)")

ax1.set_title('Direct Mapped', y=1.0, pad=-14)
ax2.set_title('Fully Associative (FIFO)', y=1.0, pad=-14)
ax3.set_title('Fully Associative (LRU)', y=1.0, pad=-14)
ax4.set_title('Set Associative (FIFO)', y=1.0, pad=-14)
ax5.set_title('Set Associative (LRU)', y=1.0, pad=-14)


ax1.plot(accessNums, dMC1Times)
ax2.plot(accessNums, dMC2Times)
ax3.plot(accessNums, dMC3Times)
ax4.plot(accessNums, dMC4Times)
ax5.plot(accessNums, dMC5Times)

print(dMC1Times)
print(dMC2Times)
print(dMC3Times)
print(dMC4Times)
print(dMC5Times)

plt.suptitle('Total Access Time vs Cache Size')

#------------------------------------------------------#
plt.figure(2, figsize=(2, 6))

row1 = [directMiss[0],twoMiss[0], fourmiss[0], eightMiss[0]]
row2 = [directMiss[1],twoMiss[1], fourmiss[1], eightMiss[1]]
row3 = [directMiss[2],twoMiss[2], fourmiss[2], eightMiss[2]]

plt.plot(associativityNums, row1, label="512")
plt.plot(associativityNums, row2, label="1024")
plt.plot(associativityNums, row3, label="2048")

print(row1)
print(row2)
print(row3)

plt.legend()


plt.ylabel('Miss Rate (1 - hits / total accesses)')
plt.xlabel('Associativity')

plt.suptitle('Miss Rate vs Associativity')

plt.show()