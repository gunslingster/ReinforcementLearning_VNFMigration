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
        


