import os
from utils import convert_to_csv

datafile = open('data.txt', 'w')
file_dir = os.path.join(os.getcwd(), 'information_files')
for i in range(1,10,2):
    datafile.write(f'Simulation results for {i} VNF: \n\n\n')
    for filename in os.listdir(file_dir):
        if int(filename[0]) == i:
            f = open(os.path.join(file_dir, filename), 'r')
            content = f.readlines()
            for line in content:
                if 'SFC' in line:
                    datafile.write(line + '\n')
            datafile.write('\n')

datafile.close()
convert_to_csv('data.txt')











