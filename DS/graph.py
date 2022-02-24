from copy import deepcopy
from match.graph import GraphSet
from match.match import readQasm
from DS.limit import MAX_QUBITS_NUM


class DAGGraph:
    def __init__(self, data_path):
        if data_path.endswith('.qasm'):
            data_path = data_path[:-5]

        circuit = readQasm(f'{data_path}.qasm', data_path + '.data')
        graph = GraphSet()
        graph.constrGraph(data_path + '.data')

        # origin Data Structure
        self.circuit = circuit
        self.data = graph
        
        self.gates = {}
        for gate in circuit.cirmapping:
            self.gates[gate.index] = gate
        self.qubits = set()
        for gate in self.gates.values():
            self.qubits |= set(gate.qlist)
        
        self.edges = graph.edges

    def reindex(self, patternGraph, matchedGraph, M):
        Mstr = M.Mstr

        # Step 0. prepare qubitsMap
        qubitsMap = {}
        indices = sorted(list(matchedGraph.gates.keys()))
        matchedGraphGates = {}
        for index in indices:
            matchedGraphGates[index] = matchedGraph.gates[index]
        for patternGate, matchedGate in \
            zip(patternGraph.gates.values(), matchedGraphGates.values()):
            for patternQubit, matchedQubit in \
                zip(patternGate.qlist, matchedGate.qlist):
                qubitsMap[patternQubit] = matchedQubit

        # Step 1. change gates
        for gate in self.gates.values():
            qlist = []
            for qubit in gate.qlist:
                qlist.append(qubitsMap[qubit])
            
            gate.qlist = qlist

            if len(qlist) == 2:
                gate.control = qubitsMap[gate.control]
                gate.target = qubitsMap[gate.target]
            
        # Step 2. change qubits
        self.qubits = set()
        for gate in self.gates.values():
            self.qubits |= set(gate.qlist)
        
        # Step 3. change edges
        for edge in self.edges:
            edge.label = qubitsMap[edge.label]

    def addIndexOffset(self, offset):
        # Step 1. update gates
        gates = {}
        for oldIndex, gate in self.gates.items():
            gate.index += offset
            gates[oldIndex + offset] = gate
        self.gates = gates

        # Step 2. update edges
        for edge in self.edges:
            edge.source += offset
            edge.target += offset

    def addEdge(self, edge):
        self.edges.add(edge)

    def saveQASM(self, path):
        if not path.endswith('.qasm'):
            path += '.qasm'

        # Header
        qasm = 'OPENQASM 2.0;\n'
        qasm += 'include "qelib1.inc";\n'
        qasm += f'qreg q[{MAX_QUBITS_NUM}];\n'
        qasm += f'creg c[{MAX_QUBITS_NUM}];\n'

        # Gates
        for gate in self.gates.values():
            qasm += f'{gate.type} q[{gate.qlist[0]}]'
            if len(gate.qlist) == 2:
                qasm += f',q[{gate.qlist[1]}]'
            qasm += ';\n'

        # save to file
        with open(path, 'w') as f:
            f.write(qasm)

    def __sub__(self, rhs):
        # Step 1. sub gates
        gates = {}
        for gate in self.gates.values():
            if gate.index not in rhs.gates:
                gates[gate.index] = gate
        self.gates = gates

        # Step 2. sub edges
        self.edges = self.edges - rhs.edges
        edges = set()
        for edge in self.edges:
            if edge.source not in rhs.gates and \
                edge.target not in rhs.gates:
                edges.add(edge)
        self.edges = edges

        # Step 3. update qubits
        qubits = set()
        for gate in self.gates.values():
            qubits |= set(gate.qlist)
        self.qubits = qubits

        return self

    def __add__(self, rhs):
        rhs = deepcopy(rhs)
        # Step 1. update index
        if len(rhs.gates) == 0:
            return self
        
        minIndex = min(rhs.gates.keys())
        offset = len(rhs.gates)

        ## Step 1.1 update gates
        gates = {}
        for oldIndex, gate in self.gates.items():
            if gate.index > minIndex:
                gate.index += offset
                gates[oldIndex + offset] = gate
            else:
                gates[oldIndex] = gate
        self.gates = gates

        ## Step 1.2 update edges
        for edge in self.edges:
            if edge.source > minIndex:
                edge.source += offset
            if edge.target > minIndex:
                edge.target += offset

        # Step 1. add gates
        for index, gate in rhs.gates.items():
            self.gates[index] = gate
        gates = self.gates
        self.gates = {}
        for k in sorted(gates.keys()):
            self.gates[k] = gates[k]

        # Step 2. add edges
        self.edges |= rhs.edges

        # Step 3. update qubits
        qubits = set()
        for gate in self.gates.values():
            qubits |= set(gate.qlist)
        self.qubits = qubits

        return self
