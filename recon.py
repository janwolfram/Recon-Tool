import argparse
from modules.helperFunctions import *
from modules.searchWhitelist import searchInWhitelist, findConfigs, findOtherConfigs, setupDB
from requests import get
from json import loads, dumps
from time import time
from tinydb import TinyDB
from modules.db import *
from termcolor import colored


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
    #json['crypto_material'] = getCryptoMaterial(res)

    crypto = {}
    for key in getCryptoMaterial(res):
        test = [e for e in res['firmware']['analysis']['crypto_material']['summary'][key]]
        hallo = []
        for uid in test:
            tree = get('http://localhost:5000/rest/file_object/' + uid).json()
            test2 = getMaterials(tree, key)
            f = get('http://localhost:5000/rest/file_object/' + uid).json()
            material = []
            for i, e in enumerate(test2):
                material.append(e)
            hallo.append({'name': getHid(f).split("/")[-1], 'uid': uid,
                          'material': material})
        crypto[key] = hallo

    json['crypto_material'] = crypto



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
    print(dumps(json, indent=4, sort_keys=False))
    # print(json)
    # findConfigs(loads(dumps(json["whitelist"])))

    print(colored('[+]', 'green'), colored('device_name', 'blue'))
    print(json['crypto_material']['SSLCertificate'][0]['material'][0])

    print(f'Time taken: {time() - start_first}')


if __name__ == '__main__':
    main()
