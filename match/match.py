from glob import glob
import os
import sys

from DS.base.Edge import Edge
from DS.base.Gate import Gate
from DS.base.Mstr import M_
from match.graph import GraphSet
from match.map import Map
from match.vf import Vf


gMedium_path = './data/medium/'
gData_path = ''
gPattern_path = ''
gSubstitute_path = ''


class FileResult:
    def __init__(self):
        self.layers = []
        self.qlist = []
        self.lolist = []
        self.ngates = 0
        self.index = -1
        self.n2gates = 0
        self.cirmapping=[]
    
    def __repr__(self) -> str:
        return f'layers: {self.layers}\nqlist: {self.qlist}\nlolist: {self.lolist}\n' \
             + f'ngates: {self.ngates}\nn2gates: {self.n2gates}\nindex: {self.index}\n' \
             + f'cirmapping: {self.cirmapping}'


def readQasm( path,outpath):
    layers = []
    ngates = 0
    n2gates = 0
    if os.path.isdir(path):
        return
    # Open file
    results = FileResult()
    results.layers = layers
    f = open(path, "r")
    line = f.readline()
    line = line.strip()
    if not line.__eq__("OPENQASM 2.0;"):
        print('ERROR: first line of the file has to be: OPENQASM 2.0; %s' % path)
        sys.exit(-1)

    line = f.readline()
    line = line.strip()
    if not line.__eq__("include \"qelib1.inc\";"):
        print('ERROR: second line of the file has to be: include \"qelib1.inc\";')
        sys.exit(-1)
    line = f.readline()
    line = line.strip()
    n = -1
    if not line.startswith('qreg'):
        print('ERROR: failed to parse qasm file: ' + line)
        sys.exit(-1)
    n = int(line[7:len(line) - 2])

    line = f.readline()
    line = line.strip()
    if not line.startswith('creg'):
        print('ERROR: failed to parse qasm file: ' + line)
        sys.exit(-1)
    contents=[]
    last_layer = []
    last_position= []
    pre_result = outpath
    file = open(pre_result, mode='w+')
    file.write('t # 0\n')
    for i in range(20):
        last_layer.append(-1)
        last_position.append(-1)
    while True:
        line = f.readline().strip()
        if not line:
            break
        if line.__eq__(''):
            break
        g = Gate()
        g.index=ngates
        results.cirmapping.append(g)
        layer = 0
        position=0
        str = []
        str.append(line.split(' ')[0])
        str.extend(line.split(' ')[1].split(','))
        if len(str) == 3:
            g.type = str[0]
            g.control = int(str[1][2:len(str[1]) - 1])
            g.target = int(str[2][2:len(str[2]) - 2])
            g.qlist.append(int(str[1][2:len(str[1]) - 1]))
            g.qlist.append(int(str[2][2:len(str[2]) - 2]))
            layer = max(last_layer[g.target], last_layer[g.control]) + 1
            position=last_position[g.target]
            if position != -1:
                content = 'e %s %s %s\n' %(position, ngates,g.target)
                contents.append(content)
            position = last_position[g.control]
            if position != -1:
                content = 'e %s %s %s\n' % (position, ngates, g.control)
                contents.append(content)
            last_position[g.control] = ngates
            last_position[g.target] = ngates
            last_layer[g.target] = layer
            last_layer[g.control] = layer
            n2gates += 1
        elif len(str) == 2:
            if str[0].startswith('rz'):
                angle = float(str[0][3:len(str[0]) - 1])
                g.control = -1
                g.target = int(str[1][2:len(str[1]) - 2])
                g.qlist.append(int(str[1][2:len(str[1]) - 2]))
                g.type = 'rz'
                g.angle = angle
                position = last_position[g.target]
                if position != -1:
                    content = 'e %s %s %s\n' % (position, ngates,g.target)
                    contents.append(content)
                last_position[g.target] = ngates
            else:
                g.type = str[0]
                g.control = -1
                g.target = int(str[1][2:len(str[1]) - 2])
                g.qlist.append(int(str[1][2:len(str[1]) - 2]))
                layer = last_layer[g.target] + 1
                last_layer[g.target] = layer
                position = last_position[g.target]
                if position!= -1:
                    content = 'e %s %s %s\n' %(position, ngates,g.target)
                    contents.append(content)
                last_position[g.target] = ngates
        else:
            print("ERROR: could not read gate: " + line)
            sys.exit(-1)
        content='v %s %s\n'%(ngates,2)
        file.write(content)
        ngates += 1
        if len(layers) <= layer:
            layers.append([])
        layers[layer].append(g)
    results.ngates = ngates
    results.n2gates = n2gates
    for i in contents:
        file.write(i)

    file.write('t # -1')
    file.close()
    return results
def domstrlist(mstr:list):
    res=[]
    for m in mstr:
        v1,v2=m.strip().split(':')
        res.append(int(v1))
    return res
def domdictlist(mstr:list):
    res=[]
    for m in mstr:
        res.append(m)
    return res
def valuelist(mstr:list):
    res=[]
    for m in mstr:
        v1,v2=m.strip().split(':')
        res.append(int(v2))
    return res
def eqlist(sour:list,target):
    if len(sour)==0 and len(target)==0:
        return True
    if len(sour)==0 or len(target)==0:
        return False
    if len(sour)!= len(target):
        return False
    for p in target:
        if p in sour:
            pass
        else:
            return False
    return True
def FeasibilityRules(f1,f2,mstr,msem):
    global gData_path
    global gPattern_path
    vf2 = Vf()
    Co = readQasm(f'{gData_path}.qasm', f'{gData_path}.data')
    Cp = readQasm(f'{gPattern_path}.qasm', f'{gPattern_path}.data')
    if not vf2.vertexIsomorphism(mstr, Co.cirmapping, Cp.cirmapping):
        return False
    vf2.setorigin(GraphSet())
    vf2.getoriginal().constrGraph(f1)
    vf2.setsub(GraphSet())
    vf2.getsub().constrGraph(f2)
    result = {}
    result = vf2.dfsMatch(0, 0, result,msem)
    if len(result) == len(vf2.getsub().curVSet(0)):
        print("Match! %s %d-th graph isomorphism %s %d-th graph!" % (f2, 0, f1, 0))
        print(result)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return True
    else:
        print("Mismatch! %s %d-th graph isomerism %s %d-th graph!" % (f2, 0, f1, 0))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return False

def computeTlist(Sin,Sout,inpath,outpath):
    Cs = readQasm(inpath, outpath)
    for i in range(len(Cs.cirmapping)):
        if Cs[i].control != -1 and Cs[i].control not in Sin:
            Sin.append(Cs[i].control)
        if Cs[i].target not in Sin:
            Sin.append(Cs[i].target)

    for i in range(len(Cs) - 1, 0, -1):
        if Cs[i].control != -1 and Cs[i].control not in Sout:
            Sout.append(Cs[i].control)
        if Cs[i].target not in Sout:
            Sout.append(Cs[i].target)

def edgeInSet(key,T,type):
    if type:
        #type=1 Tout
        if key.target in  T:
            return True
    else:
        #type=0 Tin
        if key.target in T:
            return True
    return False


def computeSinSout(Sin,Sout,Cs,indexes):
    qlist = []
    for i in indexes:
        flag = True
        if Cs.cirmapping[i].control != -1 and Cs.cirmapping[i].control not in qlist:
            qlist.append(Cs.cirmapping[i].control)
            Sin.append(i)
            flag = False
        if Cs.cirmapping[i].target not in qlist:
            qlist.append(Cs.cirmapping[i].target)
            if flag:
                Sin.append(i)
    qlist = []
    for i in range(len(indexes)-1, -1, -1):
        flag = True
        if Cs.cirmapping[indexes[i]].control != -1 and Cs.cirmapping[indexes[i]].control not in qlist:
            qlist.append(Cs.cirmapping[indexes[i]].control)
            Sout.append(indexes[i])
            flag = False
        if Cs.cirmapping[indexes[i]].target not in qlist:
            qlist.append(Cs.cirmapping[indexes[i]].target)
            if flag:
                Sout.append(indexes[i])

def generateGraph(M:M_,e1,e2,f1,f2):
    out1 = open(e1, 'w+')
    out1.write('t # 0\n')
    out2 = open(e2, 'w+')
    out2.write('t # 0\n')
    for m in M.Mstr:
        v1, v2 = m.strip().split(':')
        out1.write('v %s %s\n' % (int(v2), 2))
        out2.write('v %s %s\n' % (v1, 2))
    vf2 = Vf()
    vf2.setorigin(GraphSet())
    vf2.getoriginal().constrGraph(f1)
    vf2.setsub(GraphSet())
    vf2.getsub().constrGraph(f2)
    originaledges = vf2.getoriginal().curESet(0)
    subedges = vf2.getsub().curESet(0)
    for i in range(len(originaledges)):
        va1 = originaledges[i].source
        va2 = originaledges[i].target
        oridom = valuelist(M.Mstr)
        if int(va1) in oridom and int(va2) in oridom:
            M.Msem[0].append(originaledges[i])
            out1.write('e %s %s %s\n' % (int(va1), int(va2), originaledges[i].label))

    for i in range(len(subedges)):

        va1 = subedges[i].source
        va2 = subedges[i].target
        oridom = domstrlist(M.Mstr)
        if int(va1) in oridom and int(va2) in oridom:
            M.Msem[1].append(subedges[i])
            out2.write('e %s %s %s\n' % (va1, va2, subedges[i].label))
        pass
    out1.write('t # -1')
    out2.write('t # -1')
    out1.close()
    out2.close()

def substitute(Gs,Gr,Cs,Cr,Sin,q1,q,j):
    for gate in Cr:
        if  gate.index==j and (gate.control == q or gate.target == q) :
            for k in Sin:
                if Cs is None or len(Cs)==0:
                    return
                for l in Cs.cirmapping:
                    if l.index == k and (l.control == q1 or l.target == q1):
                        edge = Edge(j, k, q)
                        Gr.curESet(0).append(edge)
                        if l.control == q1:
                            l.control = 1
                        Cr.append(l)
    Gr.curVSet(0).extend(Gs.curVSet(0))


def computeCandidate(i, j, Go, Gp,result):
    curMap = Map(result)
    # test usage!
    # print("in dfsMatch() curMap.subMap() : ", curMap.subMap())
    # print("in dfsMatch() curMap.subMap() length: ", len(curMap.subMap()))
    # print("in dfsMatch() self.__sub.curVSet(i) : ", Gp.curVSet(i))
    # print("in dfsMatch() self.__sub.curVSet(i) length: ", len(Gp.curVSet(i)))

    subMNeighbor = curMap.neighbor(i, Gp, 0, True)
    gMNeighbor = curMap.neighbor(j, Go, 1, True)

    if not (subMNeighbor and gMNeighbor):
        print("Class Vf dfsMatch(), subMNeighbor or gMNeighbor is empty!")
        exit()

    subNMNeighbor = curMap.neighbor(i, Gp, 0, False)
    gNMNeighbor = curMap.neighbor(j, Go, 1, False)
    # print("in dfsMatch() subNMNeighbor: ", subNMNeighbor
    # print("in dfsMatch() gNMNeighbor: ", gNMNeighbor

    # notice, choose one vertex in subGraphNeighbor is ok
    while (len(subNMNeighbor) > 1):
        subNMNeighbor.pop()

    vf2 = Vf()
    pairs = vf2.candidate(subNMNeighbor, gNMNeighbor)
    return pairs

def computeTinTout(Tin, Tout, Gr, Cr, M:M_, g):
    gin = []
    gout = []
    computeSinSout(gin, gout, Cr, list(g.curVSet(0).keys()))
    for key in gin:
        v1Neighbor = Gr.computeSource(0, key)
        for vertex in v1Neighbor:
            Tin.append(vertex)
    for key in gout:
        v1Neighbor = Gr.computeTarget(0, key)
        for vertex in v1Neighbor:
            Tout.append(vertex)

def qlist(g:GraphSet,Cg:list):
    res=[]
    for key in g.curVSet(0):
        for l in Cg:
            if key ==l.index:
                if l.control != -1 and l.control not in res:
                    res.append(l.control)
                if Cg[key].target not in res:
                    res.append(l.target)
    return res


def qlistbyindex(qs,C:list):
    res=[]
    if C.cirmapping[qs].control != -1 and C.cirmapping[qs].control not in res:
        res.append(C.cirmapping[qs].control)
    if C.cirmapping[qs].target not in res:
        res.append(C.cirmapping[qs].target)
    return res
def edgelabel():
    pass


def adjustGraphIndex(Gr,Cr,fromindex,index):
    vset = list(Gr.curVSet(0).keys())
    Vset = {}

    for k in range(len(vset)-1,-1,-1):
        if vset[k] > fromindex:
            Vset[vset[k] + index] = '2'
            Cr.cirmapping[index].index = vset[k] + index
        else:
            Vset[vset[k]] = '2'
    Vset2=sorted(Vset)
    Vset1={}
    for i in Vset2:
        Vset1[i]=Vset[i]
    Gr.setVertexSet(0, Vset1)
    for k in Gr.curESet(0):
        v1=k.source
        v2=k.target
        if int(v1) > fromindex:
            v1 = int(v1) + index
        if int(v2) > fromindex:
            v2 = int(v2) + index
        k.source=v1
        k.target=v2


class PaternMatch:
    def __init__(self):
        self.mapping=[]

    def patternMatch(self, f1, f2, Go: GraphSet, Gp: GraphSet, M: M_):
        dommstr = domstrlist(M.Mstr)

        if eqlist(dommstr, domdictlist(Gp.vertexSet(0))):
            self.mapping.append(M)
            print('success: ',M.Mstr)
        else:
            submap= {}
            if len(M.Mstr)>0:
                for p in M.Mstr:
                    v1, v2 = p.strip().split(':')
                    submap[int(v1)] = int(v2)
            P = computeCandidate(0, 0, Go, Gp,submap)
            for p in P:
                M1=M_(M.Mstr, M.Msem)
                if p in M.Mstr:
                    continue
                M.Mstr.append(str(p))
                global gMedium_path
                e1 = gMedium_path + 'original.txt'
                e2 = gMedium_path + 'sub.txt'
                generateGraph(M,e1,e2,f1,f2)
                flag=FeasibilityRules(e1,e2,M.Mstr,list(M.Msem))
                if flag:
                    self.patternMatch(f1,f2,Go,Gp,M)
                M=M1

        return self.mapping


################################################


def match(data_path, pattern_path):
    if data_path.endswith('.qasm'):
        data_path = data_path[:-5]
    if pattern_path.endswith('.qasm'):
        pattern_path = pattern_path[:-5]
    
    global gData_path
    global gPattern_path
    gData_path = data_path
    gPattern_path = pattern_path

    Co = readQasm(f'{data_path}.qasm', data_path + '.data')
    Cp = readQasm(f'{pattern_path}.qasm', pattern_path + '.data')
    pm = PaternMatch()

    Go = GraphSet()
    Go.constrGraph(data_path + '.data')
    Gp = GraphSet()
    Gp.constrGraph(pattern_path + '.data')

    M = M_([],[])
    pm = PaternMatch()

    stdout = sys.stdout
    sys.stdout = None
    res = pm.patternMatch(data_path + '.data', pattern_path + '.data', Go, Gp, M)
    sys.stdout = stdout
    
    return res



