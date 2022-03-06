OPENQASM 2.0;
include "qelib1.inc";
qreg q[32];
creg c[32];
x q[1];
cx q[0],q[1];
x q[1];
