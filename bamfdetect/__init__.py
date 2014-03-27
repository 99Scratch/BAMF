from sys import path
import modules
import modules.common
from os import listdir
from os.path import isfile, isdir, join, abspath, dirname

path.append(dirname(abspath(__file__)))


def get_version():
    return "1.1.0"


def get_loaded_modules():
    l = []
    for m in modules.common.Modules.list:
        l.append(m.get_metadata())
    return l


def scan_file_data(file_content, module_filter, only_detect):
    """

    @param file_content:
    @param module_filter:
    @param only_detect:
    @return:
    """
    for m in modules.common.Modules.list:
        if module_filter is not None and m.get_module_name() not in module_filter:
            continue
        if m.is_bot(file_content):
            results = {}
            if not only_detect:
                results["information"] = m.get_bot_information(file_content)
            results["type"] = m.get_bot_name()
            results["module"] = m.get_module_name()
            results["description"] = m.get_metadata().description
            return results
    return None


def scan_paths(paths, only_detect, recursive, module_filter):
    """
    Scans paths for known bots and dumps information from them

    @rtype : dict
    @param paths: list of paths to check for files
    @param only_detect: only detect known bots, don't process configuration information
    @param recursive: recursively traverse folders
    @param module_filter: if not None, only modules in list will be used
    @return: dictionary of file to dictionary of information for each file
    """
    results = {}
    while len(paths) != 0:
        file_path = abspath(paths[0])
        del paths[0]
        if isfile(file_path):
            with open(file_path, mode='rb') as file_handle:
                file_content = file_handle.read()
                r = scan_file_data(file_content, module_filter, only_detect)
                if r is not None:
                    results[file_path] = r
        elif isdir(file_path):
            for p in listdir(file_path):
                p = join(file_path, p)
                if isfile(p) or (isdir(p) and recursive):
                    paths.append(p)
    return results