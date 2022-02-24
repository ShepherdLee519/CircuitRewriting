from PatternMatching import PatternMatching, jsonToQASM
from ReplaceSubgraph import ReplaceSubgraph


class CircuitWriter:
    def execute(self, data_path, pattern_path):
        pattern_path, substitute_path = jsonToQASM(pattern_path)

        # # Algorithm 1: return mapping list M
        mappingList = PatternMatching(data_path, pattern_path)

        # # Algorithm 2: return rewritten graph Gr
        rewrittenGraph = ReplaceSubgraph(data_path, substitute_path, mappingList)

        return rewrittenGraph