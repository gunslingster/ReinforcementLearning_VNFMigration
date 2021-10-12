from classes import *
from utils import *
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
info_files = 'information_files'
input_files = 'input_files'
output_files = 'output_files'

dir1 = os.path.join(dir_path, info_files)
dir2 = os.path.join(dir_path, input_files)
dir3 = os.path.join(dir_path, output_files)

for num_vnf in range(1, 10, 2):
    for count in range(1, 11):
        flow_network = FlowNetwork(8, num_vnf, 1)
        f = f'{num_vnf}vnf_simulation{count}.txt'
        output = f'output{num_vnf}{count}.txt'
        path1 = os.path.join(dir1, f)
        path2 = os.path.join(dir2, f)
        path3 = os.path.join(dir3, f)
        flow_network.gen_output_file(path2)
        flow_network.gen_information_file(path1)
        os.system(f'./cs2.exe < {path2} > {path3}')
        vnf_mapping = extract_mcf(path3)
        mcf = 1
        for vnf, backup in vnf_mapping.items():
            vnf = get_key_from_value(flow_network.node_mapping ,vnf)
            backup = get_key_from_value(flow_network.node_mapping,backup)
            vnf_failure = flow_network.failure_probabilities[vnf]
            backup_failure = flow_network.failure_probabilities[backup]
            mcf *= 1 - vnf_failure * backup_failure
        with open(path1, 'a') as f:
            f.write(f'SFC availability via MCF: {mcf}\n')


    
