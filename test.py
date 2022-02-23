from PatternMatching import PatternMatching
from ReplaceSubgraph import ReplaceSubgraph

data_path = './data/origin/example3.qasm'
pattern_path = './data/pattern/pattern3.qasm'
substitute_path = './data/pattern/substitute3.qasm'


# # Algorithm 1: return mapping list M
mappingList = PatternMatching(data_path, pattern_path)

# # Algorithm 2: return rewritten graph Gr
rewrittenGraph = ReplaceSubgraph(data_path, substitute_path, mappingList)
rewrittenGraph.saveQASM('result.qasm')