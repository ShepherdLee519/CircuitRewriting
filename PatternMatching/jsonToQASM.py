import json, os
from DS.limit import MAX_QUBITS_NUM


def convertJSONtoQASM(data):
    # Header
    qasm = 'OPENQASM 2.0;\n'
    qasm += 'include "qelib1.inc";\n'
    qasm += f'qreg q[{MAX_QUBITS_NUM}];\n'
    qasm += f'creg c[{MAX_QUBITS_NUM}];\n'

    for gate in data:
        # eg. ['cx', [0, 1]] or ["x", [1]]
        string = gate[0] + ' '
        for qubit in gate[1]:
            string += f'q[{qubit}],'
        string = string[:-1] + ';'
        string += '\n'

        qasm += string
        
    return qasm


def saveQASM(qasm, qasm_path):
    with open(qasm_path, 'w') as file:
        file.write(qasm)


def jsonToQASM(json_path, qasm_dir='./data/pattern/qasm/'):
    patternname = (os.path.basename(json_path))[:-5]

    with open(json_path, 'r') as file:
        data = json.load(file)

        src_qasm = convertJSONtoQASM(data['src'])
        dst_qasm = convertJSONtoQASM(data['dst'])

        pattern_path = qasm_dir + patternname + '.qasm'
        substitute_path = qasm_dir + patternname + '_substitute.qasm'
        saveQASM(src_qasm, pattern_path)
        saveQASM(dst_qasm, substitute_path)

        return pattern_path, substitute_path