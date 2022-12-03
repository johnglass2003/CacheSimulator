# CacheSimulator
Simulation for Cache Performance
John Glass Cache Simulator

This Cache Simulator has been made using Python including timeit and matplotlib.pyplot

(Fifo means First In First Out and Lru means Least Recently Used)

To create a Cache, here are the class names and their constructor natures:
  Direct Mapped Cache: directMappedCache(Cache Size, Line Size)
  Fully Associative Fifo Cache: fullyAssociativeCacheFifo(Cache Size, Line Size)
  Fully Associative Lru Cache: fullyAssociativeCacheLru(Cache Size, Line Size)
  N - Way Set Associative Fifo Cache: directMappedCache(Cache Size, Line Size, Lines Per Set)
  N - Way Set Associative Fifo Cache: directMappedCache(Cache Size, Line Size, Lines Per Set)
 
Each of these Caches have an access method with one paramter being the address to be accessed. If it is a hit, the cache's hit counter member variable is increased,
and the line's counter is increased.

The Miss handling is dependant on the Cache Type.

PyPlot is implemented after the tests are run and the data for the plots is collected. I have implemented Hit Rate vs Cache Size, Total Access Time vs Cache Size,
and Miss Rate vs Associativity

Thank You!
