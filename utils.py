import re

def extract_mcf(output_file):
    mapping = {}
    with open(output_file) as f:
        for i in range(15):
            next(f)
        for line in f:
            info = line.split()
            if info[0] == 'c':
                continue
            if info[1] == '0':
                continue
            if info[2] == '1':
                continue
            if info[3] == '1':
                mapping[int(info[1])] = int(info[2])
    return mapping

def get_key_from_value(dictionary, value):
    for key,val in dictionary.items():
        if val == value:
            return key
 
def convert_to_csv(data_file):
    f  = open(data_file, 'r')
    lines = f.readlines()
    output = open('data.csv', 'w')
    for line in lines:
        if 'MCF' in line and 'SFC' in line:
            data = re.search('0\..*', line).group()
            output.write(data + '\n')
        elif 'SFC' in line:
            data = re.search('0\..*', line).group()
            output.write(data + ', ')
        else:
            continue






