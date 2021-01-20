# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 10:53:40 2021

@author: Sterling Abrahams
"""

# Implementation of a fat tree topology 


k = int(input('Enter number of ports for each switch, must be an even number: '))
        
class fatTree():
    
    CoreSwitchList = []
    AggSwitchList = []
    EdgeSwitchList = []
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
            pmcount += podSize
        
            
        
    
    def calc_dist(node1, node2):
        pass
        
            

mytree = fatTree(k)

            
    
        

    

    
    
        
        
