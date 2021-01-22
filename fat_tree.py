# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 10:53:40 2021

@author: Sterling Abrahams
"""

import math
from collections import defaultdict

k = int(input('Enter number of ports for each switch, must be an even number: '))
        
class fatTree():
    
    CoreSwitchList = []
    CoreDict = defaultdict(lambda: [])
    AggSwitchList = []
    EdgeSwitchList = []
    EdgeDict = defaultdict(lambda: [])
    # Each pod will be a list of agg switches and edge switches
    # k/2 agg switchs and k/2 edge switches
    PodList = []
    HostList = []
    # a list that contains tuples of all the lists
    linkList = []
    
    def __init__(self, k):
        self.k = k
        self.iCoreLayerSwitch = int(pow((k//2),2)) 
        self.iAggLayerSwitch = int(k/2) * k
        self.iEdgeLayerSwitch = self.iAggLayerSwitch
        self.iHost = self.iEdgeLayerSwitch * 2 
        self.iPods = k
        self.createCoreLayerSwitch(self.iCoreLayerSwitch)
        self.createAggLayerSwitch(self.iAggLayerSwitch)
        self.createEdgeLayerSwitch(self.iEdgeLayerSwitch)
        self.createHost(self.iHost)
        self.createPod(self.iPods)
        self.createHost(self.iHost)
        self.createLink()
        
        
        
    def createCoreLayerSwitch(self, NUMBER):
        for x in range(1, NUMBER+1):
            PREFIX = "100"
            if x >= int(10):
                PREFIX = "10"
            self.CoreSwitchList.append(PREFIX + str(x))
    
    def createAggLayerSwitch(self, NUMBER):
        for x in range(1, NUMBER+1):
            PREFIX = "200"
            if x >= int(10):
                PREFIX = "20"
            self.AggSwitchList.append(PREFIX + str(x))
    
    def createEdgeLayerSwitch(self, NUMBER):
        for x in range(1, NUMBER+1):
            PREFIX = "300"
            if x >= int(10):
                PREFIX = "30"
            self.EdgeSwitchList.append(PREFIX + str(x))
            
    def createPod(self, NUMBER):
        podSize = int(k//2)
        def genPod(index):
            pod = []
            for i in range(index, index+podSize):
                pod.append(self.AggSwitchList[i])
                pod.append(self.EdgeSwitchList[i])
            return pod
           
        counter = 0
        for x in range(1, NUMBER+1):
            pod = genPod(counter)
            self.PodList.append(pod)
            counter += podSize
            
            
    
    def createHost(self, NUMBER):
        for x in range(1, NUMBER+1):
            PREFIX = "400"
            if x >= int(10):
                PREFIX = "40"
            self.HostList.append(PREFIX + str(x))
    
    def addLink(self, node1, node2):
        self.linkList.append((node1, node2))

    def createLink(self):
        # Each core switch must be connected to each pod
        # Each agg switch is connected to k/2 core switches
        aggCount = -1
        podSize = int(self.k/2)
        for i in range(self.iCoreLayerSwitch):
            if i % podSize == 0:
                aggCount += 1
            for j in range(aggCount, self.iAggLayerSwitch, podSize):
                self.addLink(self.CoreSwitchList[i], self.AggSwitchList[j])
                self.CoreDict[self.CoreSwitchList[i]].append(self.AggSwitchList[j])
                
        # Connect agg switches in each pod to edge switches in the pod
        for pod in self.PodList:
            aggSwitches = [switch for switch in pod if switch[0] == '2']
            edgeSwitches = [switch for switch in pod if switch[0] == '3']
            for aggswitch in aggSwitches:
                for edgeswitch in edgeSwitches:
                    self.addLink(aggswitch, edgeswitch)
                    
        # Connect each edge switch to k/2 servers
        pmcount = 0
        for i in range(self.iEdgeLayerSwitch):
            for j in range(pmcount, pmcount + podSize):
                self.addLink(self.EdgeSwitchList[i], self.HostList[j])
                self.EdgeDict[self.EdgeSwitchList[i]].append(self.HostList[j])
            pmcount += podSize
        
            
        
    
    def calc_dist(self, node1, node2):
        # Can use the IDs and pods to calculate distance on a case by case basis
     
        # First case, both nodes are hosts
        if node1[0] == '4' and node2[0] == '4':
            for edgeSwitch in self.EdgeSwitchList:
                if node1 in self.EdgeDict[edgeSwitch] and node2 in self.EdgeDict[edgeSwitch]:
                    return 2
            
            for pod in self.PodList:
                podCheck = []
                for switch in pod:
                    if switch[0] == '3':
                        for host in self.EdgeDict[switch]:
                            podCheck.append(host)
                if node1 in podCheck and node2 in podCheck:
                    return 4
            return 6
        
        # Second case, host and edge switch
        if node1[0] == '4' and node2[0] == '3':
            check1 = node1
            check2 = node2
            if check1 in self.EdgeDict[check2]:
                return 1
        
            key_list = list(self.EdgeDict.keys())
            val_list = list(self.EdgeDict.values())
            position = val_list.index(check1)
            edgesw = key_list(position)
            for pod in self.PodList:
                if edgesw in pod and check2 in pod:
                    return 3
            return 5
        if node1[0] == '3' and node2[0] == '4':
            check1 = node2
            check2 = node1
            
            if check1 in self.EdgeDict[check2]:
                return 1
        
            key_list = list(self.EdgeDict.keys())
            val_list = list(self.EdgeDict.values())
            for i in range(len(val_list)):
                if check1 in val_list[i]:
                    position = i
            edgesw = key_list[position]
            for pod in self.PodList:
                if edgesw in pod and check2 in pod:
                    return 3
            return 5
    
        
mytree = fatTree(k)
    

    
    
        
        
