OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
creg c[16];
cx q[1],q[2];
h q[3];
x q[0];
h q[4];
x q[1];
cx q[3],q[4];
cx q[0],q[2];
h q[3];
h q[4];
cx q[1],q[4];
h q[3];
h q[0];
cx q[3],q[0];
h q[3];
h q[0];
x q[2];