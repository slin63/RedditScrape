def build_list(file):
    """Creates a list given a file with elements separated by newlines."""
    list = []
    open_file = open(file, 'r')
    for line in open_file.readlines():
        list.append(line[0:-1])
    return list


def search_list(string, l):
    """Searches a list for a selected string. Returns true if the string is found, false otherwise"""
    string = string.lower()
    for word in l:
        if string.find(word) != -1:
            return True
    return False


def assign_to_item(item, key_list, arg_list):
    """Given a scrapy.Item(), list of keys for the item, and list of definitions for those keys,
    assigns each key its respective definition."""
    i = item
    count = 0
    for e in key_list:
        try:
            i[e] = arg_list[count]
            count += 1
        except IndexError:
            i[e] = None
    return i


def clean_newlines(text_list):
    """Simply removes indexes containing [\n]'s from a list."""
    remove_list = []
    for e in text_list:
        if e.find('\n') != -1:
            remove_list.append(e)
    for e in remove_list:
        text_list.remove(e)
    return text_list


def merge_lists(text_list):
    """Concatenates all string elements within a list to form a single string."""
    new_string = ""
    for e in text_list:
        new_string += (e + ' ')
    return [(new_string[0:-1])]  # [0:-1] to remove the extra whitespace at the end


def clean_textlist(text_list):
    return merge_lists(clean_newlines(text_list))
