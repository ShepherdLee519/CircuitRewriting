
class CircuitInfo:
    def __init__(self, path):
        self.ops = []

        with open(path, 'r') as file:
            next(file) # OPENQASM 2.0;
            next(file) # include "qelib1.inc";
            next(file) # qreg q[16];
            next(file) # creg c[16];

            for row in file:
                self.ops.append(row.strip())

    @property
    def size(self):
        return len(self.ops)