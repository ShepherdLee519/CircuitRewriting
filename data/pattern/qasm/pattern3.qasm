OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
creg c[16];
x q[1];
cx q[0],q[1];
x q[1];
