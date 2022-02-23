#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     vf.py
# ROLE:     vf2 algorithm
# CREATED:  2015-11-28 20:55:11
# MODIFIED: 2015-12-05 11:58:12

import sys
import os

from DS.base.Edge import Edge
from match.graph import GraphSet
from match.map import Map

class Vf:

    __origin = None
    __sub = None
    def vertexIsomorphism(self,Mstr:set,Co:list,Cp:list):
        for p in Mstr:
            v1,v2=p.strip().split(':')
            if Co[int(v2)].type==Cp[int(v1)].type and len(Co[int(v2)].qlist) ==len(Cp[int(v1)].qlist) and Co[int(v2)].angle==Cp[int(v1)].angle:
                continue
            else:
                return False
        return True

    def candidate(self, subMNeighbor, gMNeighbor):
        if not (subMNeighbor and gMNeighbor):
            print("Class Vf candidate() arguments value error! subMNeighbor or gMNeighbor is empty!" )
            exit()
        if not (isinstance(subMNeighbor, list) and isinstance(gMNeighbor, list)):
            print("Class Vf candidate() arguments type error! type list expected!" )
            exit()
        if not all(isinstance(x, int) for x in subMNeighbor):
            print("Class Vf candidate() arguments type error! int in subMNeighbor list expected!" )
        if not all(isinstance(x, int) for x in gMNeighbor):
            print("Class Vf candidate() arguments type error! int in gMNeighbor list expected!" )

        pairs = []
        for i in range(len(subMNeighbor)):
            for j in range(len(gMNeighbor)):
                string = str(subMNeighbor[i]) + ":" + str(gMNeighbor[j])
                pairs.append(string)
                # print(string)
        return pairs

    #type = 0, pre; type = 1, succ
    def preSucc(self, vertexNeighbor, map, type):
        #vertexNeighbor and map can be empty
        if not (isinstance(vertexNeighbor, list) and isinstance(map, list)):
            print("Class Vf preSucc() arguments type error! vertexNeighbor and map expected list!" )
            exit()
        if not (type == 0 or type == 1):
            print("Class Vf preSucc() arguments value error! type expected 0 or 1!" )
           
        result = []
        #succ
        if type:
            for vertex in vertexNeighbor:
                if vertex not in map:                   
                    result.append(vertex)
        #pre
        else:
            for vertex in vertexNeighbor:
                if vertex in map:
                    result.append(vertex)
        return result
    
    #type = 0, __sub; type = 1, __origin
    def edgeLabel(self, offset, index1, index2, type):
        res=[]
        if type:
            for key in self.__origin.curESet(offset):
                if key.source==index1 and key.target==index2:
                    res.append(key.label)
        else:
            for key in self.__sub.curESet(offset)  :
                if key.source==index1 and key.target==index2:
                    res.append(key.label)
        return res

    
    def isMatchInV2Succ(self, j, vertex, edge, v2, v2Succ,msem):
        for i in edge:
            for succ in v2Succ:
                vLabel = self.__origin.curVSet(j)[succ]
                eLabel = self.edgeLabel(j, int(v2), int(succ), 1)
                if len(msem[0])==len(msem[1]) and vLabel == vertex :
                    mp=self.labelmapping(msem, i, 0)
                    if mp==-1:
                        return False
                    else:
                        if mp not in eLabel:
                            return False
        return True

    # type = 0, __sub; type = 1, __origin
    def labelmapping(self,msem,label,type):
        if type:
            for m in range(len(msem[1])):
                if len(msem[0])==len(msem[1]) and msem[1][m].label == label:
                    print(len(msem[0]),len(msem[1]))
                    return msem[0][m].label
        else:
            for m in range(len(msem[0])):
                if len(msem[0])==len(msem[1]) and msem[0][m].label == label:
                    return msem[1][m].label
        return -1

    def isMeetRules(self, v1, v2, i, j, result, subMap, gMap, subMNeighbor, gMNeighbor,msem):
        #test usage!
        # print("-------------------------------------------")
        # print("in isMeetRules() v1: %d, v2: %d" %(v1, v2))
        # print("in isMeetRules() result: ", result)
        # print("in isMeetRules() subMap: ", subMap)
        # print("in isMeetRules() gMap: ", gMap)
        # print("in isMeetRules() subMNeighbor: ", subMNeighbor)
        # print("in isMeetRules() gMNeighbor: ", gMNeighbor)

        
        #compare label of v1 and v2
        subVSet = self.__sub.curVSet(i)
        gVSet = self.__origin.curVSet(j)
        

        if subVSet[v1] != gVSet[v2]:
            #print("vertex label different!"
            return False
            
        #notice, when result is empty, first pair should be added when their vertexLabels are the same!
        if not result:
            return True
        
        
        v1Neighbor = self.__sub.neighbor(i, v1)
        v2Neighbor = self.__origin.neighbor(j, v2)
                
        v1Pre = self.preSucc(v1Neighbor, subMap, 0)
        v1Succ = self.preSucc(v1Neighbor, subMap, 1)
        v2Pre = self.preSucc(v2Neighbor, gMap, 0)
        v2Succ = self.preSucc(v2Neighbor, gMap, 1)


        #test usage!
        # print("in isMeetRules() v1Neighbor: ", v1Neighbor)
        # print("in isMeetRules() v2Neighbor: ", v2Neighbor    )
        # print("in isMeetRules() v1Pre: ", v1Pre)
        # print("in isMeetRules() v2Pre: ", v2Pre)
        # print("in isMeetRules() v1Succ: ", v1Succ)
        # print("in isMeetRules() v2Succ: ", v2Succ)


        #3,4 rule
        if(len(v1Pre) > len(v2Pre)):
            #print("len(v1Pre) > len(v2Pre)!"
            return False
                
        for pre in v1Pre:
            if result[pre] not in v2Pre:
                #print("v1Pre not in v2Pre!")
                return False
            for el in self.edgeLabel(i, int(pre), int(v1), 0):
                v2labels=self.edgeLabel(j, result[pre], v2, 1)
                if self.labelmapping(msem, el, 1) not in v2labels:
                    return False




        if(len(v1Succ) > len(v2Succ)):
            print("len(v1Succ) > len(v2Succ)!")
            return False
                
        for succ in v1Succ:
            vertex = self.__sub.curVSet(i)[succ]
            edge = self.edgeLabel(i, int(v1), int(succ), 0)
            flag = self.isMatchInV2Succ(j, vertex, edge, v2, v2Succ, msem)
            if not flag:
                print("not self.isMatchInV2Succ()")
                return False


        
        #5,6 rules
        len1 = len(set(v1Neighbor) & set(subMNeighbor))
        len2 = len(set(v2Neighbor) & set(gMNeighbor))
        if len1 > len2:
            #print("5,6 rules mismatch!"
            return False
            
        #7 rule     
        len1= len(set(self.__sub.curVSet(i).keys()) - set(subMNeighbor) - set(v1Succ))
        len2 = len(set(self.__origin.curVSet(j).keys()) - set(gMNeighbor) - set(v2Succ))
        if len1 > len2:
            #print("7 rule mismatch!"
            return False        
            
        return True

    def dfsMatch(self, i, j, result,msem):
        # print("in dfsMatch() result: ", result
        if not isinstance(result, dict):
            print("Class Vf dfsMatch() arguments type error! result expected dict!")

        curMap = Map(result)

        # test usage!
        # print("in dfsMatch() curMap.subMap() : ", curMap.subMap())
        # print("in dfsMatch() curMap.subMap() length: ", len(curMap.subMap()))
        # print("in dfsMatch() self.__sub.curVSet(i) : ", self.__sub.curVSet(i))
        # print("in dfsMatch() self.__sub.curVSet(i) length: ", len(self.__sub.curVSet(i)))
        if curMap.isCovered(self.__sub.curVSet(i)):
            print("yes!")
            return result

        subMNeighbor = curMap.neighbor(i, self.__sub, 0, True)
        gMNeighbor = curMap.neighbor(j, self.__origin, 1, True)

        if not (subMNeighbor and gMNeighbor):
            print("Class Vf dfsMatch(), subMNeighbor or gMNeighbor is empty!")
            exit()

        subNMNeighbor = curMap.neighbor(i, self.__sub, 0, False)
        gNMNeighbor = curMap.neighbor(j, self.__origin, 1, False)
        # print("in dfsMatch() subNMNeighbor: ", subNMNeighbor
        # print("in dfsMatch() gNMNeighbor: ", gNMNeighbor

        # notice, choose one vertex in subGraphNeighbor is ok
        while (len(subNMNeighbor) > 1):
            subNMNeighbor.pop()

        # test usage!
        # print("Class Vf dfsMatch() curMap.subMap(): ", curMap.subMap())
        # print("Class Vf dfsMatch() curMap.gMap(): ", curMap.gMap())
        # print("Class Vf dfsMatch() subMNeighbor: ", subMNeighbor)
        # print("Class Vf dfsMatch() gMNeighbor: ", gMNeighbor)
        # print("Class Vf dfsMatch() result: ", result)
        # pairs = self.candidate(subMNeighbor, gMNeighbor)
        # print("Class Vf dfsMatch() pairs: ", pairs)

        pairs = self.candidate(subNMNeighbor, gNMNeighbor)
        if not pairs:
            return result

        for pair in pairs:
            v1, v2 = pair.strip().split(":")
            flag=self.isMeetRules(int(v1), int(v2), i, j, result, curMap.subMap(), curMap.gMap(), subMNeighbor, gMNeighbor,msem)
            if (flag):
                result[int(v1)] = int(v2)

                self.dfsMatch(i, j, result,msem)
                # notice, it's important to return result when len(result) == len(self.__sub.curVSet(i))
                # otherwise it will continue to pop
                if len(result) == len(self.__sub.curVSet(i)):
                    return result
                result.pop(int(v1))
        return result
    def setorigin(self,graph):
        self.__origin =graph
    def setsub(self,graph):
        self.__sub =graph
    def getoriginal(self):
        return self.__origin
    def getsub(self):
        return self.__sub
   
