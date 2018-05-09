from lor_lib.parser.constants import *


def type_to_string(s):
    """
    return string type variable
    :param s: any variable
    :return: string
    """
    if type(s) == type(1):
        return integer()
    elif type(s) == type("string"):
        return string()
    elif type(s) == type(("abc", 1)):
        return tuple_str()
    else:
        return none()


def string_to_type(t):
    """
    return function type t
    :param t: string type
    :return: function
    """
    if t == integer():
        return int
    elif t == string():
        return str
    elif t == tuple_str():
        return tuple
    else:
        return None


def save_dict(d, path_to_file):
    """
    :param d: dict
    :param path_to_file:
    :return: boolean
    save dict object to filesystem. Return True if saved or False if File Not Found
    """
    try:
        f = open(path_to_file, "w")
        for key in d.keys():
            tmp = type_to_string(d[key])
            if tmp == "tuple":
                f.writelines(tmp + ":" + key + ":")
                for elem in d[key]:
                    f.writelines(type_to_string(elem) + ":")
                for elem in d[key]:
                    f.writelines(str(elem) + ":")
                f.writelines("\n")
            else:
                f.writelines(tmp + ":" + str(key) + ":" + str(d[key]) + "\n")
        f.close()
        return True
    except FileNotFoundError:
        return False


def load_dict(path_to_file):
    """
    :param path_to_file: str
    :return: None or dict
    load dict object in filesystem. Return dict if object loaded else return None
    """
    d = {}
    try:
        f = open(path_to_file, "r")
        for line in f.readlines():
            tmp = line.strip().split(":")
            if tmp[0] == "tuple":
                count_elems = (len(tmp) - 3) // 2
                l = []
                for i in range(count_elems):
                    l.append(string_to_type(tmp[2 + i])(tmp[2 + count_elems + i]))
                d[tmp[1]] = tuple(l)
            else:
                d[tmp[1]] = string_to_type(tmp[0])(tmp[2])
        f.close()
        return d
    except FileNotFoundError:
        return None
