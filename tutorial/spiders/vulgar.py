def build_list(file):
    list = []
    open_file = open(file, 'r')
    for line in open_file.readlines():
        list.append(line[0:-1])
    return list


