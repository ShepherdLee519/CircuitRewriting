#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     graph.py
# ROLE:     read graph from inputFile
# CREATED:  2015-11-28 20:55:11
# MODIFIED: 2015-12-04 09:43:50
from DS.base.Edge import Edge


class GraphSet:

    def __init__(self):
        self.__graphSet = []
        self.__vertexSet = []
        self.__edgeSet = []
    def constrGraph(self, inputFile):
        try:
            with open(inputFile, "r") as fin:
                lineNum = -1
                curVertexSet = {}
                curEdgeSet = {}
                for line in fin:
                    lineList = line.strip().split(" ")
                    if not lineList:
                        print("Class GraphSet __init__() line split error!")
                        exit()
                    # a new graph!
                    if lineList[0] == 't':
                        # write it to graphSet
                        if lineNum > -1:
                            currentGraph = (lineNum, curVertexSet, curEdgeSet)
                            self.__graphSet.append(currentGraph)
                            self.__vertexSet.append(curVertexSet)
                            self.__edgeSet.append(curEdgeSet)
                            # print("Class GraphSet __init__  __graphSet: ", self.__graphSet
                            # print("Class GraphSet __init__  __vertexSet: ", self.__vertexSet
                            # print("Class GraphSet __init__  __edgeSet: ", self.__edgeSet
                        lineNum += 1
                        curVertexSet = {}
                        curEdgeSet = []
                    elif lineList[0] == 'v':
                        if len(lineList) != 3:
                            print("Class GraphSet __init__() line vertex error!")
                            exit()
                        curVertexSet[int(lineList[1])] = lineList[2]
                    elif lineList[0] == 'e':
                        if len(lineList) != 4:
                            print("Class GraphSet __init__() line edge error!")
                            exit()
                        edge= Edge(int(lineList[1]),int(lineList[2]),int(lineList[3]))
                        curEdgeSet.append(edge)
                    else:
                        # empty line!
                        continue
        except IOError:
            print("Class GraphSet __init__() Cannot open Graph file: %s"%inputFile)
            exit()
    def constrGraphInSet(self, inputFile,nodes):
        try:
            with open(inputFile, "r") as fin:
                lineNum = -1
                curVertexSet = {}
                curEdgeSet = {}
                for line in fin:
                    lineList = line.strip().split(" ")
                    if not lineList:
                        print("Class GraphSet __init__() line split error!")
                        exit()
                    # a new graph!
                    if lineList[0] == 't':
                        # write it to graphSet
                        if lineNum > -1:
                            currentGraph = (lineNum, curVertexSet, curEdgeSet)
                            self.__graphSet.append(currentGraph)
                            self.__vertexSet.append(curVertexSet)
                            self.__edgeSet.append(curEdgeSet)
                            # print("Class GraphSet __init__  __graphSet: ", self.__graphSet
                            # print("Class GraphSet __init__  __vertexSet: ", self.__vertexSet
                            # print("Class GraphSet __init__  __edgeSet: ", self.__edgeSet
                        lineNum += 1
                        curVertexSet = {}
                        curEdgeSet = []
                    elif lineList[0] == 'v':
                        if len(lineList) != 3:
                            print("Class GraphSet __init__() line vertex error!")
                            exit()
                        if int(lineList[1])  in nodes:
                            curVertexSet[int(lineList[1])] = lineList[2]
                    elif lineList[0] == 'e':
                        if len(lineList) != 4:
                            print("Class GraphSet __init__() line edge error!")
                            exit()
                        if int(lineList[1]) in nodes or int(lineList[2]) in nodes:
                            edge = Edge(int(lineList[1]), int(lineList[2]), int(lineList[3]))
                            curEdgeSet.append(edge)
                    else:
                        # empty line!
                        continue
        except IOError:
            print("Class GraphSet __init__() Cannot open Graph file: ")
            exit()
    
    def graphSet(self,offset):
        return self.__graphSet[offset]
    def vertexSet(self,offset):
        return self.__vertexSet[offset]
    def setVertexSet(self,offset,vertexs):
        self.__vertexSet[offset]=vertexs
    def setEdgeSet(self,offset,edges):
        self.__edgeSet[offset]=edges
    def setGraphSet(self,offset,graph):
        self.__graphSet[offset]=graph
    def edgeSet(self,offset):
        return self.__edgeSet[offset]
    def curVSet(self, offset):
        if offset >= len(self.__vertexSet):
            print("Class GraphSet curVSet() offset out of index!" )
            exit()
        
        return self.__vertexSet[offset]
        
        
    def curESet(self, offset):
        if offset >= len(self.__edgeSet):
            print("Class GraphSet curESet() offset out of index!" )
            exit()
        
        return self.__edgeSet[offset]
    
      
    def curVESet(self, offset):
    
        if offset >= len(self.__vertexSet):
                print("Class GraphSet curVESet() offset out of index!%s"%offset )
                exit()

        vertexNum = self.__vertexSet[offset].keys()
        vertexNum=list(vertexNum)
        index=-1
        for i in vertexNum:
            if i >index:
                index=i
        result = [[] for i in range(index+1)]
        # print('result:',result)
            
        for edge in self.__edgeSet[offset]:
            result[edge.source].append(edge)
            result[edge.target].append(edge)
        return result
    

    def neighbor(self, offset, vertexIndex):
        if offset >= len(self.__vertexSet):
            print("Class GraphSet neighbor() offset out of index!" ) 
            exit()
        
        VESet = self.curVESet(offset)[vertexIndex]
        neighborSet = []
        for key in VESet:
            if key.target == vertexIndex and key.source not in neighborSet :
                neighborSet.append(key.source)
            if key.source == vertexIndex and key.target not in neighborSet:
                neighborSet.append(key.target)
        return neighborSet
    def computeTarget(self, offset, vertexIndex):
        if offset >= len(self.__vertexSet):
            print("Class GraphSet neighbor() offset out of index!")
            exit()
        neighborSet = []
        VESet = self.curVESet(offset)[vertexIndex]
        for key in VESet:
            if  key.source==vertexIndex and key.target not in neighborSet:
                neighborSet.append(key.target)
        return neighborSet
    def computeSource(self, offset, vertexIndex):
        if offset >= len(self.__vertexSet):
            print("Class GraphSet neighbor() offset out of index!")
            exit()
        neighborSet = []
        VESet = self.curVESet(offset)[vertexIndex]
        for key in VESet:
            if key.target == vertexIndex and key.source not in neighborSet :
                neighborSet.append(key.source)
        return neighborSet
    def edgesbetweentwonode(self, offset, vIndex1,vIndex2):
        if offset >= len(self.__vertexSet):
            print("Class GraphSet neighbor() offset out of index!")
            exit()

        VESet = self.curVESet(offset)
        aList1 = VESet[vIndex1]
        aList2 = VESet[vIndex2]
        neighborSet = []
        for i in range(len(aList1)):
            va1, va2 = aList1[i].strip().split(":")
            for i in range(len(aList2)):
                v1, v2 = aList2[i].strip().split(":")
                if va1 == v1 and va2 == v2:
                    neighborSet.append(aList2[i])
                elif va1 == v2 and va2 == v1:
                    neighborSet.append(aList2[i])
                else:
                    continue
        return neighborSet

    def __repr__(self) -> str:
        return f'graphSet: {self._GraphSet__graphSet}\n\nvertexSet: {self._GraphSet__graphSet}\n\nedgeSet: {self._GraphSet__edgeSet}'

    @property
    def edges(self):
        edgesSet = set()
        length = len(self.__edgeSet)
        for i in range(length):
            for edge in self.edgeSet(i):
                edgesSet.add(edge)
        
        return edgesSet
