import copy
from DS.base.Edge import Edge
from DS.graph import DAGGraph
from DS.limit import MAX_QUBITS_NUM


def MatchedGraph(originGraph, M):
    matchedEdges = M.Msem[0]
    matchedGraph = copy.deepcopy(originGraph)

    # Step 1. update edges
    matchedGraph.edges = set(matchedEdges)

    # Step 2. update gates
    matchedGatesIndices = set()
    for edge in matchedEdges:
        matchedGatesIndices.add(edge.source)
        matchedGatesIndices.add(edge.target)
    
    matchedGates = {}
    for index in matchedGatesIndices:
        if index not in matchedGraph.gates:
            return False, None
        
        matchedGates[index] = matchedGraph.gates[index]
    matchedGraph.gates = matchedGates

    # Step 3. update qubits
    qubits = set()
    for gate in matchedGates.values():
        qubits |= set(gate.qlist)

    matchedGraph.qubits = qubits

    return True, matchedGraph


def InstantiateGraph(patternGraph, matchedGraph, substitutionGraph, M):
    # will update qubits/gates/edges
    adjustSubstitutionGraph = copy.deepcopy(substitutionGraph)
    adjustSubstitutionGraph.reindex(patternGraph, matchedGraph, M)

    return adjustSubstitutionGraph


def ComputeSio(substitutionGraph):
    Sin = [-1 for i in range(MAX_QUBITS_NUM)]
    Sout = [-1 for i in range(MAX_QUBITS_NUM)]

    gates = list(substitutionGraph.gates.values())
    for qubit in substitutionGraph.qubits:
        for gate in gates:
            if qubit in gate.qlist:
                Sin[qubit] = gate.index
                break
        
        for gate in gates[::-1]:
            if qubit in gate.qlist:
                Sout[qubit] = gate.index
                break

    return Sin, Sout

def ComputeTio(graph, matchedGraph):
    Tin = [-1 for i in range(MAX_QUBITS_NUM)]
    Tout = [-1 for i in range(MAX_QUBITS_NUM)]

    gates = list(matchedGraph.gates.values())

    # Compute Tin
    inGatesIndices = []
    for edge in graph.edges:
        if graph.gates[edge.target] in gates:
            if graph.gates[edge.source] not in gates:
                inGatesIndices.append(edge.source)

    for index in inGatesIndices:
        gate = graph.gates[index]
        for qubit in gate.qlist:
            Tin[qubit] = gate.index

    # Compute Tout
    outGatesIndices = []
    for edge in graph.edges:
        if graph.gates[edge.source] in gates:
            if graph.gates[edge.target] not in gates:
                outGatesIndices.append(edge.target)

    for index in outGatesIndices:
        gate = graph.gates[index]
        for qubit in gate.qlist:
            Tout[qubit] = gate.index

    return Tin, Tout

def adjustTout(Tout, minIndex, offset):
    Tout_ = []
    for index in Tout:
        if index > minIndex:
            Tout_.append(index + offset)
        else:
            Tout_.append(index)
    
    return Tout_

def adjustMappingList(mappingList, start, minIndex, offset):
    for i in range(start, len(mappingList)):
        M = mappingList[i]

        # Step 1 change Mstr
        newMstr = []
        for string in M.Mstr:
            a, b = string.split(':')
            b = int(b)
            if b > minIndex:
                b += offset
            newMstr.append(f'{a}:{b}')
        
        for j, string in enumerate(newMstr):
            M.Mstr[j] = newMstr[j] 

        # Step 2 change Msem
        edges = M.Msem[0]
        for edge in edges:
            if edge.source > minIndex:
                edge.source += offset
            if edge.target > minIndex:
                edge.target += offset


def MakeEdge(gateSource, gateTarget):
    if gateSource.index > gateTarget.index:
        gateSource, gateTarget = gateTarget, gateSource

    label = list(set(gateSource.qlist) & set(gateTarget.qlist))[0]
    edge = Edge(gateSource.index, gateTarget.index, label)

    return edge



def ReplaceSubgraph(data_path, substitute_path, mappingList):
    mappingList, patternGraph = mappingList
    originGraph = DAGGraph(data_path)
    substitutionGraph = DAGGraph(substitute_path)

    replacedGraph = originGraph

    for i, M in enumerate(mappingList):
        # M = <Mstr, Msem>
        # Step 0. prepare graphs
        ok, matchedGraph = MatchedGraph(replacedGraph, M)
        if not ok:
            continue

        adjustedSubstitutionGraph = InstantiateGraph(patternGraph, matchedGraph, substitutionGraph, M)

        # Step 1. compute Tin/Tout before modify graph
        Tin, Tout = ComputeTio(replacedGraph, matchedGraph)

        # Step 2. Calculate Cr = Cr - g + Gs
        ## Step 2.1 Calculate Cr - g(replacedGraph - matchedGraph)
        replacedGraph = replacedGraph - matchedGraph

        ## Step 2.2 Calculate Cr + Gs(replacedGraph + substitutionGraph)
        minIndex = min(matchedGraph.gates.keys())
        adjustedSubstitutionGraph.addIndexOffset(minIndex)
        replacedGraph = replacedGraph + adjustedSubstitutionGraph

        ## Step 2.3 compute Sin/Sout and adjust Tout after modifying
        Sin, Sout = ComputeSio(adjustedSubstitutionGraph)
        # adjust Tout
        Tout = adjustTout(Tout, minIndex, offset=len(adjustedSubstitutionGraph.gates))
        adjustMappingList(mappingList, i + 1, minIndex, offset=len(adjustedSubstitutionGraph.gates))

        # Step 3. add new edges
        for qubit in matchedGraph.qubits:
            if qubit in adjustedSubstitutionGraph.qubits:
                if Tin[qubit] != -1:
                    replacedGraph.addEdge(
                        MakeEdge(
                            adjustedSubstitutionGraph.gates[Sin[qubit]],
                            replacedGraph.gates[Tin[qubit]]
                        )
                    ) # MakeEdge(Sin[q], Tin[q])
                
                if Tout[qubit] != -1:
                    replacedGraph.addEdge(
                        MakeEdge(
                            adjustedSubstitutionGraph.gates[Sout[qubit]],
                            replacedGraph.gates[Tout[qubit]]
                        )
                    ) # MakeEdge(Sout[q], Tout[q])
            else:
                if Tin[qubit] != -1 and Tout[qubit] != -1:
                    replacedGraph.addEdge(
                        MakeEdge(
                            replacedGraph.gates[Tin[qubit]],
                            replacedGraph.gates[Tout[qubit]]
                        )
                    ) # MakeEdge(Tin[q], Tout[q])
        # End for qubit in matchedGraph.qubits
    # End for M in mappingList:

    return replacedGraph