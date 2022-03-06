from CircuitWriter import CircuitInfo

path = './data/origin/example5.qasm'

circuitInfo = CircuitInfo(path)
print(circuitInfo.size)