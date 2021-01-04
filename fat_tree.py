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
    HostList = []
    # a list that contains tuples of all the lists
    linkList = []
    
    def __init__(self, k):
        self.k = k
        self.iCoreLayerSwitch = k
        self.iAggLayerSwitch = k * 2
        self.iEdgeLayerSwitch = k * 2
        self.iHost = self.iEdgeLayerSwitch * 2 
        self.createCoreLayerSwitch(self.iCoreLayerSwitch)
        self.createAggLayerSwitch(self.iAggLayerSwitch)
        self.createEdgeLayerSwitch(self.iEdgeLayerSwitch)
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
    
    def createHost(self, NUMBER):
        for x in range(1, NUMBER+1):
            PREFIX = "400"
            if x >= int(10):
                PREFIX = "40"
            self.HostList.append(PREFIX + str(x))
    
    def addLink(self, node1, node2):
        self.linkList.append((node1, node2))

    def createLink(self):
        for x in range(0, self.iAggLayerSwitch, 2):
            self.addLink(self.CoreSwitchList[0], self.AggSwitchList[x])
            self.addLink(self.CoreSwitchList[1], self.AggSwitchList[x])
        for x in range(1, self.iAggLayerSwitch, 2):
            self.addLink(self.CoreSwitchList[2], self.AggSwitchList[x])
            self.addLink(self.CoreSwitchList[3], self.AggSwitchList[x])
        for x in range(0, self.iAggLayerSwitch, 2):
            self.addLink(self.AggSwitchList[x], self.EdgeSwitchList[x])
            self.addLink(self.AggSwitchList[x], self.EdgeSwitchList[x+1])
            self.addLink(self.AggSwitchList[x+1], self.EdgeSwitchList[x])
            self.addLink(self.AggSwitchList[x+1], self.EdgeSwitchList[x+1])
        for x in range(0, self.iEdgeLayerSwitch):
            ## limit = 2 * x + 1 
            self.addLink(self.EdgeSwitchList[x], self.HostList[2 * x])
            self.addLink(self.EdgeSwitchList[x], self.HostList[2 * x + 1])
            

mytree = fatTree(k)

            
    
        

    

    
    
        
        