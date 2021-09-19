from fat_tree import fatTree
import random

k = int(input('Enter number of ports for each switch, must be an even number: '))

mytree = fatTree(k)
# n1 = input('Please enter first node: ')
# n2 = input('Please enter second node: ')
# print('Distance between nodes is : {}'.format(mytree.calc_dist(n1,n2)))

# # Random distance testing for nodes in teh fat tree
# def distanceCheck(episodes, tree):
#     for i in range(episodes):
#         node1 = random.choice(tree.allNodes)
#         node2 = random.choice(tree.allNodes)
#         distance = mytree.calc_dist(node1, node2)
#         print("Distance between {} and {}: {}".format(node1, node2, distance))

# distanceCheck(100, mytree)

l = int(input('Enter l, the number of VM pairs: '))
m = int(input('Enter m, the number of VNFs: '))
f = int(input('Enter f, the frequency of the link: '))

# Generate l random vm pairs from the hosts
def genVM(l):
    vm_pairs = []
    for i in range(l):
        vm1 = random.choice(mytree.HostList)
        vm2 = random.choice(mytree.HostList)
        vm_pairs.append([vm1,vm2])
    return vm_pairs

vm_pairs = genVM(l)
print('VM pairs: {}'.format(vm_pairs))

# VNFS must be a switch in the network
available_switches = mytree.CoreSwitchList + mytree.AggSwitchList + mytree.EdgeSwitchList

# Choose m random VNFs from the available switches
def chooseVNF(m):
    vnf_route = []
    for i in range(m):
        vnf = random.choice(available_switches)
        vnf_route.append(vnf)
        available_switches.remove(vnf)
    return vnf_route

vnf_list = chooseVNF(m)
print('VNF nodes: {}'.format(vnf_list))

# This function will generate routes
# A route starts from the first host in a vm pair
# Then traverses to each VNF
# The end node is the second host in the vnf pair
def get_routes():
    routes = []
    for pair in vm_pairs:
        route = []
        route.append(pair[0])   # Start vm
        route += vnf_list       # VNFs to traverse
        route.append(pair[1])   # End vm
        routes.append(route)
    return routes

all_routes = get_routes()

def calc_cost(routes):
    """
    Calculate the cost of each route in routes through the
    fat tree network.

    Parameters
    ----------
    routes : A list containing multiple lists, routes trhough the network.

    Returns
    -------
    costs: An array containing the cost for each route.

    """
    costs = []
    for route in routes:
        cost = 0
        for i in range(0, len(route)-1):
            cost += mytree.calc_dist(route[i], route[i+1])
        print('The cost along route {}: {}'.format(route, cost))
        costs.append(cost)
    return costs

calc_cost(all_routes)





