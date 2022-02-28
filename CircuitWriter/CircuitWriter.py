from os import listdir
from os.path import isdir, splitext, basename

from common import Timer
from CircuitWriter.CircuitInfo import CircuitInfo
from PatternMatching import PatternMatching, jsonToQASM
from ReplaceSubgraph import ReplaceSubgraph

G_before_info = None
G_after_info = None

class CircuitWriter:

    def _solve(self, data_path, pattern_path):
        pattern_path, substitute_path = jsonToQASM(pattern_path)

        # # Algorithm 1: return mapping list M
        mappingList = PatternMatching(data_path, pattern_path)
        # # Algorithm 2: return rewritten graph Gr
        rewrittenGraph = ReplaceSubgraph(data_path, substitute_path, mappingList)

        return rewrittenGraph

    def _execute(self, data_path, pattern_path, output_path):
        global G_after_info

        filename = splitext(basename(data_path))[0]
        if output_path != None:
            output_filename = output_path + filename + '_result.qasm'
        else:
            output_filename = data_path

        if not isdir(pattern_path):
            rewrittenGraph = self._solve(data_path, pattern_path)
            rewrittenGraph.saveQASM(output_filename)
        else:
            isFirst = True
            for file_path in listdir(pattern_path):
                if splitext(file_path)[1] == '.json':
                    if isFirst:
                        data_path = self._execute(data_path, pattern_path + file_path, output_path)
                        isFirst = False
                    else:
                        self._execute(data_path, pattern_path + file_path, None)
        
        G_after_info = CircuitInfo(output_filename)

        return output_filename

    def execute(self, data_path, pattern_path, output_path):
        if isdir(data_path):
            for file_path in listdir(data_path):
                if splitext(file_path)[1] == '.qasm':
                    self.execute(data_path + file_path, pattern_path, output_path)
        else:
            with Timer(f'Solving <{data_path}>'):
                global G_before_info
                G_before_info = CircuitInfo(data_path)

                self._execute(data_path, pattern_path, output_path)

                print(f' - finished. (before: {G_before_info.size}, after: {G_after_info.size}, reduced: {G_before_info.size - G_after_info.size}({(G_before_info.size - G_after_info.size)/G_before_info.size * 100:.2f}%))')