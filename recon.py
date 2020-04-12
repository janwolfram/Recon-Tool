import argparse
from modules.helperFunctions import *
from modules.searchWhitelist import searchInWhitelist, findConfigs, findOtherConfigs, setupDB, findImportantConfigs
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
    json['vendor'] = getVendor(res)
    json['device_class'] = getDeviceClass(res)
    json['release_date'] = getReleaseDate(res)
    json['version'] = getVerison(res)
    #json['crypto_material'] = getCryptoMaterial(res)

    crypto = {}
    for key in getCryptoMaterial(res):
        if key != 'SSLCertificate':
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


    software_components = getSoftwareComponents(res)
    sc = {}
    for key in software_components:
        arr = []
        liste = getSoftwareComponents(res)[key]
        for e in liste:
            f = get('http://localhost:5000/rest/file_object/' + e).json()
            arr.append(
                {'name': getHid(f).split("/")[-1], 'uid': e, 'exploit_mitigations': {'Canary': getExploitMitigation(f, 'Canary'),
                                                        'NX': getExploitMitigation(f, 'NX'),
                                                        'PIE': getExploitMitigation(f, 'PIE'),
                                                        'RELRO': getExploitMitigation(f, 'RELRO')}}
            )
        sc[key] = arr

    json['software_components'] = sc
    #json['software_components'] = getSoftwareComponents(res)

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
    important_configs = []
    for key in json['whitelist']:
        liste = json['whitelist'][key]
        for e in findImportantConfigs(liste):
            important_configs.append(e)

    json['important_configs'] = important_configs

    configs = findOtherConfigs(included_files, db)['configs']


    for el in important_configs:
        for i, e in enumerate(configs):
            if e['name'] == el['name']:
                configs.pop(i)

    json['configs'] = configs
    # test = findConfigs(loads(dumps(json["whitelist"])))
    # print(test)
    print(dumps(json, indent=4, sort_keys=False))
    # print(json)
    # findConfigs(loads(dumps(json["whitelist"])))
    json['vendor'] = getVendor(res)
    json['device_class'] = getDeviceClass(res)
    json['release_date'] = getReleaseDate(res)
    json['version'] = getVerison(res)

    print(colored('[+]', 'green'), colored('device_name:', 'blue'), json['device_name'])
    print(colored('[+]', 'green'), colored('vendor:', 'blue'), json['vendor'])
    print(colored('[+]', 'green'), colored('device_class:', 'blue'), json['device_class'])
    print(colored('[+]', 'green'), colored('release_date:', 'blue'), json['release_date'])
    print(colored('[+]', 'green'), colored('version:', 'blue'), json['version'])
    print('--------------------------------------------------------')
    print(colored('[+]', 'green'), colored('crypto_material:', 'yellow'))
    for key in json['crypto_material']:
        print(colored('\n[+]', 'green'), colored('key:', 'blue'), colored(key, 'red'))
        print(colored('--------------------------------------------------------', 'red'))
        liste = json['crypto_material'][key]
        if key == 'SSLCertificate':
            for e in liste:
                print(colored('\n[+]', 'green'), colored('name:', 'blue'), e['name'])
                print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
        else:
            for i, e in enumerate(liste):
                print(colored('\n[+]', 'green'), colored('name:', 'blue'), e['name'])
                print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
                for i, material in enumerate(e['material']):
                    if i < 2:
                        print(material)
                        if i < 1 and i != len(liste) - 1:
                            print(colored('--------------------------------------------------------', 'white'))
                    else:
                        break
                if i != len(e['material']) - 1:
                    left = (len(e['material']) - 1) - i
                    print(colored('[+]', 'green'), colored(str(left) + ' elements left', 'red'),
                          colored('[use interactive mode to see all]', 'yellow'))
                if i != len(liste) - 1:
                    print(colored('--------------------------------------------------------', 'blue'))
        print(colored('--------------------------------------------------------', 'red'))

    # print(json['crypto_material']['SSLCertificate'][0]['material'][0])

    print(colored('\n[+]', 'green'), colored('software_components:\n', 'yellow'))
    for key in json['software_components']:
        print(colored('--------------------------------------------------------', 'red'))
        print(colored('[+]', 'green'), colored('key:', 'blue'), colored(key + '\n', 'red'))
        liste = json['software_components'][key]
        for i, e in enumerate(liste):
            if i < 10:
                print(colored('[+]', 'green'), colored('name:', 'blue'), e['name'])
                print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
                print(colored('[+]', 'green'), colored('exploit_mitigations:', 'blue'))
                print(colored('    ->', 'green'), colored('Canary:', 'blue'), e['exploit_mitigations']['Canary'])
                print(colored('    ->', 'green'), colored('NX:', 'blue'), e['exploit_mitigations']['NX'])
                print(colored('    ->', 'green'), colored('PIE:', 'blue'), e['exploit_mitigations']['PIE'])
                print(colored('    ->', 'green'), colored('RELRO:', 'blue'), e['exploit_mitigations']['RELRO'])
                if i != len(liste) - 1:
                    print(colored('--------------------------------------------------------', 'blue'))
            else:
                break
        if i != len(liste) - 1:
            left = len(liste) - 10
            print(colored('[+]', 'green'), colored(str(left) + ' elements left', 'red'),
                  colored('[use interactive mode to see all]', 'yellow'))
        print(colored('--------------------------------------------------------\n', 'red'))

    print(colored('\n[+]', 'green'), colored('whitelist:\n', 'yellow'))
    for key in json['whitelist']:
        print(colored('--------------------------------------------------------', 'red'))
        liste = json['whitelist'][key]
        if len(liste) > 0:
            print(colored('[+]', 'green'), colored('key:', 'blue'), colored(key + '\n', 'red'))
        else:
            print(colored('[-]', 'red'), colored('key:', 'blue'), colored(key, 'red'))
        for i, e in enumerate(liste):
            print(colored('[+]', 'green'), colored('name:', 'blue'), e['name'])
            print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
            print(colored('[+]', 'green'), colored('exploit_mitigations:', 'blue'))
            print(colored('    ->', 'green'), colored('Canary:', 'blue'), e['exploit_mitigations']['Canary'])
            print(colored('    ->', 'green'), colored('NX:', 'blue'), e['exploit_mitigations']['NX'])
            print(colored('    ->', 'green'), colored('PIE:', 'blue'), e['exploit_mitigations']['PIE'])
            print(colored('    ->', 'green'), colored('RELRO:', 'blue'), e['exploit_mitigations']['RELRO'])
            if i != len(liste) - 1:
                print(colored('--------------------------------------------------------', 'blue'))
        print(colored('--------------------------------------------------------\n', 'red'))

    print(colored('\n[+]', 'green'), colored('important_configs:\n', 'yellow'))
    for i, e in enumerate(json['important_configs']):
        print(colored('[+]', 'green'), colored('name:', 'blue'), e['name'])
        print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
        print(colored('[+]', 'green'), colored('exploit_mitigations:', 'blue'))
        print(colored('    ->', 'green'), colored('Canary:', 'blue'), e['exploit_mitigations']['Canary'])
        print(colored('    ->', 'green'), colored('NX:', 'blue'), e['exploit_mitigations']['NX'])
        print(colored('    ->', 'green'), colored('PIE:', 'blue'), e['exploit_mitigations']['PIE'])
        print(colored('    ->', 'green'), colored('RELRO:', 'blue'), e['exploit_mitigations']['RELRO'])
        if i != len(json['important_configs']) - 1:
            print(colored('--------------------------------------------------------', 'blue'))

    print(colored('\n[+]', 'green'), colored('remaining_configs:\n', 'yellow'))
    for i, e in enumerate(json['configs']):
        print(colored('[+]', 'green'), colored('name:', 'blue'), e['name'])
        print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
        print(colored('[+]', 'green'), colored('exploit_mitigations:', 'blue'))
        print(colored('    ->', 'green'), colored('Canary:', 'blue'), e['exploit_mitigations']['Canary'])
        print(colored('    ->', 'green'), colored('NX:', 'blue'), e['exploit_mitigations']['NX'])
        print(colored('    ->', 'green'), colored('PIE:', 'blue'), e['exploit_mitigations']['PIE'])
        print(colored('    ->', 'green'), colored('RELRO:', 'blue'), e['exploit_mitigations']['RELRO'])
        if i != len(json['configs']) - 1:
            print(colored('--------------------------------------------------------', 'blue'))


    print(f'Time taken: {time() - start_first}')


if __name__ == '__main__':
    main()
