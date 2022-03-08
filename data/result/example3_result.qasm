OPENQASM 2.0;
include "qelib1.inc";
qreg q[32];
h q[3];
cx q[3],q[0];
cx q[0],q[3];
h q[0];
