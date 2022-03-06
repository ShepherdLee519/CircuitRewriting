from CircuitWriter import CircuitWriter

# data_path = './data/origin/'
data_path = './data/benchmark/test/'
pattern_path = './data/pattern/'
output_path = './data/result/'


circuitWriter = CircuitWriter()
circuitWriter.execute(data_path, pattern_path, output_path)
