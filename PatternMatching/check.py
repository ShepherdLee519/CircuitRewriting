from DS.graph import DAGGraph


def reCheckM(mappingList, data_path, pattern_path):
    originGraph = DAGGraph(data_path)
    patternGraph = DAGGraph(pattern_path)

    filteredMappingList = []
    for mapping in mappingList:
        flag = True
        qubitsMap = {}
        for i, string in enumerate(mapping.Mstr):
            gateIndex = int(string.split(':')[1])
            gate = originGraph.gates[gateIndex]
            patternGate = patternGraph.gates[i]

            for realQubit, patternQubit in zip(gate.qlist, patternGate.qlist):
                if patternQubit in qubitsMap:
                    if qubitsMap[patternQubit] != realQubit:
                        flag = False
                        break
                else:
                    qubitsMap[patternQubit] = realQubit            

            if not flag:
                break
        if flag:
            filteredMappingList.append(mapping)

    return filteredMappingList, patternGraph