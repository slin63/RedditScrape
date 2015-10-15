def build_list(file):
    """Creates a list given a file with elements separated by newlines."""
    list = []
    open_file = open(file, 'r')
    for line in open_file.readlines():
        list.append(line[0:-1])
    return list

# list = build_list('vulgar')


def search_list(string, l):
    """Searches a list for a selected string. Returns true if the string is found, false otherwise"""
    string = string.lower()
    for word in l:
        if string.find(word) != -1:
            return True
    return False

# print search_list('FUCK', l)

