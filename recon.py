import argparse
from modules.helperFunctions import *
from modules.searchWhitelist import searchInWhitelist, findConfigs, findOtherConfigs, setupDB
from requests import get
from json import loads, dumps
from time import time
from tinydb import TinyDB
from modules.db import *


def setupArgparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--uid", help="uid of firmware", required=True)
    return parser.parse_args()


def main():
    json = {}
    start_first = time()
    args = setupArgparse()
    res = get('http://localhost:5000/rest/firmware/' + args.uid + '?summary=true').json()

    json['device_name'] = getDeviceName(res)
    json['crypto_material'] = getCryptoMaterial(res)

    keys = []
    for key in getCryptoMaterial(res):
        keys.append(key)




    json['software_components'] = getSoftwareComponents(res)

    index_filesystems = []
    for i, key in enumerate(list(getFileType(res).keys())):
        if key.count('filesystem/ext2') > 0:
            index_filesystems.append(i)
        elif key.count('filesystem/squashfs') > 0:
            index_filesystems.append(i)
        elif key.count('filesystem/cramfs') > 0:
            index_filesystems.append(i)

    included_files = []
    for index in index_filesystems:
        file_system = list(getFileType(res).values())[
            index][0]
        file_system = get('http://localhost:5000/rest/file_object/' + file_system + '?summary=true').json()
        for element in getIncludedFiles(file_system):
            included_files.append(element)

    if len(included_files) == 0:
        for element in getUnpacked(res):
            included_files.append(element)

    db = setupDB(args.uid)
    json["whitelist"] = searchInWhitelist(included_files, db)
    json['configs'] = findOtherConfigs(included_files, db)['configs']
    # test = findConfigs(loads(dumps(json["whitelist"])))
    # print(test)
    print(dumps(json, indent=8, sort_keys=False))
    # findConfigs(loads(dumps(json["whitelist"])))

    print(f'Time taken: {time() - start_first}')


if __name__ == '__main__':
    main()
