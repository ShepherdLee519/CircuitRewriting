OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
creg c[16];
h q[3];
cx q[2],q[4];
x q[0];
h q[4];
x q[1];
cx q[3],q[0];
h q[0];
cx q[4],q[0];