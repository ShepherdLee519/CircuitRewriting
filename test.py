from CircuitWriter import CircuitWriter

# data_path = './data/origin/example5.qasm'
data_path = './data/origin/'
pattern_path = './data/pattern/'
output_path = './data/result/'


circuitWriter = CircuitWriter()
circuitWriter.execute(data_path, pattern_path, output_path)
