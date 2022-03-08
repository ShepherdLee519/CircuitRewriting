from CircuitWriter import CircuitWriter

# data_path = './data/origin/example4.qasm'
data_path = './data/origin/'
pattern_path = './data/pattern/'
output_path = './data/result/'
stat_path = './'

circuitWriter = CircuitWriter()
circuitWriter.execute(
    data_path, 
    pattern_path, 
    output_path, 

    stat_path=stat_path, 
    metric='cycle'
)
