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
        path1 = os.path.join(dir1, f)
        path2 = os.path.join(dir2, f)
        flow_network.gen_output_file(path2)
        flow_network.gen_information_file(path1)


    