"""
Created on Tue Jan 12 10:25:27 2021

@author: sabrahams
"""

# Implementation of a fat tree topology 

import math
import random

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
        self.podSize = int(k/2)
        self.iCoreLayerSwitch = int(pow(k/2,2))
        self.hostsPerPod = self.iCoreLayerSwitch
        self.iAggLayerSwitch = int(k/2) * k
        self.iEdgeLayerSwitch = self.iAggLayerSwitch
        self.iHost = self.iEdgeLayerSwitch * self.podSize
        self.iPods = k
        self.createCoreLayerSwitch(self.iCoreLayerSwitch)
        self.createAggLayerSwitch(self.iAggLayerSwitch)
        self.createEdgeLayerSwitch(self.iEdgeLayerSwitch)
        self.createHost(self.iHost)
        self.createPod(self.iPods)
        self.allNodes = self.CoreSwitchList + self.AggSwitchList + self.EdgeSwitchList + self.HostList
        print('Core Switches:')
        print(self.CoreSwitchList)
        print('Aggregation Switches: ')
        print(self.AggSwitchList)
        print('Edge Switches: ')
        print(self.EdgeSwitchList)
        print('Pods:')
        print(self.PodList)
        print('Hosts:')
        print(self.HostList)
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
        
            
        
    
    def calc_dist(self, node1, node2):
        # Can use the IDs and pods to calculate distance on a case by case basis
        
        # Both nodes are the same
        if node1 == node2:
            return 0
     
        # Case 1: host-host
        if node1[0] == '4' and node2[0] == '4':
            # Both hosts are connected to the same edge switch
            if math.ceil(int(node1[2:]) / self.podSize) == math.ceil(int(node2[2:]) / self.podSize): 
                return 2
            # Both hosts are connected ot the same pod
            if math.ceil(int(node1[2:]) / self.hostsPerPod) == math.ceil(int(node2[2:]) / self.hostsPerPod): 
                return 4
            # Both hosts are in different pods
            return 6
        
        # Case 2: host-edge
        if node1[0] == '4' and node2[0] == '3' or node1[0] == '3' and node2[0] == '4':
            check1 = node1[2:] if node1[0] == '4' else node2[2:]
            check2 = node1[2:] if node1[0] == '3' else node2[2:]
            
            # Host connected to edge
            if math.ceil(int(check1) / self.podSize) == int(check2):
                return 1
            # Host connected to edge within same pod
            if math.ceil(int(check1) / self.hostsPerPod) == math.ceil(int(check2) / self.podSize):
                return 3
            return 5
                                                                          
        # Case 3: host-agg
        # Distance is 2 if host connected to that pod, or 4 if not
        if node1[0] == '4' and node2[0] == '2' or node1[0] == '2' and node2[0] == '4':
            check1 = node1[2:] if node1[0] == '4' else node2[2:]
            check2 = node1[2:] if node1[0] == '2' else node2[2:]
            
            if math.ceil(int(check1) / self.hostsPerPod) == math.ceil(int(check2) / self.podSize):
                return 2
            return 4
            
            
        
        # Case 4: host-core
        # Distance is always 3
        if node1[0] == '4' and node2[0] == '1' or node1[0] == '1' and node2[0] == '4':
            return 3
            
        # Case 5: edge-edge
        # Distance is 2 if in same pod, 4 if not
        if node1[0] == '3' and node2[0] == '3':
            if math.ceil(int(node1[2:]) / self.podSize) == math.ceil(int(node2[2:]) / self.podSize):
                return 2
            else:
                return 4
        
        # Case 6: edge-agg
        # Distance is 1 if in the same pod, 3 if not
        if node1[0] == '3' and node2[0] == '2' or node1[0] == '2' and node2[0] == '3':
            if math.ceil(int(node1[2:]) / self.podSize) == math.ceil(int(node2[2:]) / self.podSize):
                return 1
            else:
                return 3
        
        # Case 7: edge-core
        # Distance always 2
        if node1[0] == '3' and node2[0] == '1' or node1[0] == '1' and node2[0] == '3':
            return 2
        
        # Case 8: agg-agg
        # Distance is 2 if they are in the same pod, or connected to the same core switch, otherwise distance is 4
        if node1[0] == '2' and node2[0] == '2':
            if int(node1[2:]) % self.podSize == int(node2[2:]) % self.podSize or math.ceil(int(node1[2:]) / self.podSize) == math.ceil(int(node2[2:]) / self.podSize):
                return 2
            else:
                return 4
        
        # Case 9: agg-core
        # Distance is 1 if they are directely connected, 3 if not
        if node1[0] == '2' and node2[0] == '1':
            if math.ceil(int(node2[2:]) / self.podSize) == self.podSize:
                if int(node1[2:]) % (self.podSize) == 0:
                    return 1
            if int(node1[2:]) % (self.podSize) == math.ceil(int(node2[2:]) / self.podSize):
                return 1
            else:
                return 3
        if node1[0] == '1' and node2[0] == '2':
            if math.ceil(int(node1[2:]) / self.podSize) == self.podSize:
                if int(node2[2:]) % (self.podSize) == 0:
                    return 1
            if int(node2[2:]) % (self.podSize) == math.ceil(int(node1[2:]) / self.podSize):
                return 1
            else:
                return 3
        
        # Case 10: core-core
        # Distance is 2 if they are connected to the same agg switches, 4 if not
        if node1[0] == '1'and node2[0] == '1':
            if math.ceil(int(node1[2:]) / self.podSize) == math.ceil(int(node2[2:]) / self.podSize):
                return 2
            else:
                return 4
            
            
            
mytree = fatTree(k)
n1 = input('Please enter first node: ')
n2 = input('Please enter second node: ')
print('Distance between nodes is : {}'.format(mytree.calc_dist(n1,n2)))

# Random distance testing
def distanceCheck(episodes, tree):
    for i in range(episodes):
        node1 = random.choice(tree.allNodes)
        node2 = random.choice(tree.allNodes)
        distance = mytree.calc_dist(node1, node2)
        print("Distance between {} and {}: {}".format(node1, node2, distance))
    
distanceCheck(100, mytree)

