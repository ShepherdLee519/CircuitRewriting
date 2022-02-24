from CircuitWriter import CircuitWriter

data_path = './data/origin/example3.qasm'
pattern_path = './data/pattern/pattern3.json'


circuitWriter = CircuitWriter()
result = circuitWriter.execute(data_path, pattern_path)
result.saveQASM('result.qasm')