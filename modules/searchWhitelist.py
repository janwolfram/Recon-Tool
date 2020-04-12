from modules.loadData import readWhitelist
from modules.helperFunctions import *
from requests import get
from json import loads, dumps
from tinydb import TinyDB
from modules.db import *


def setupDB(uid):
    return TinyDB('db/' + uid + 'json')


def checkDB(db, whitelist):
    db_filled = False
    for element in whitelist:
        if len(db.table(element)) > 0:
            db_filled = True
    return db_filled


def searchInWhitelist(included_files, db):
    whitelist = readWhitelist()
    founded_programs_whitelist = []
    db_exist = checkDB(db, whitelist)
    for element in whitelist:
        element_found = False
        programs = [element]
        if db_exist:
            table = db.table(element)
            element_found = True
            for row in table:
                programs.append({'name': row['name'], 'uid': row['uid'],
                                 'exploit_mitigations': {'Canary': row['Canary'],
                                                         'NX': row['NX'],
                                                         'PIE': row['PIE'],
                                                         'RELRO': row['RELRO']}})
        else:
            for file in included_files:
                f = get('http://localhost:5000/rest/file_object/' + file).json()
                if hasPrintableStrings(f):
                    if hasStrings(f):
                        for string in getStrings(f):
                            if string.count(element) > 0:
                                programs.append({'name': getHid(f).split("/")[-1], 'uid': file,
                                                 'exploit_mitigations': {'Canary': getExploitMitigation(f, 'Canary'),
                                                                         'NX': getExploitMitigation(f, 'NX'),
                                                                         'PIE': getExploitMitigation(f, 'PIE'),
                                                                         'RELRO': getExploitMitigation(f, 'RELRO')}})
                                table = db.table(element)
                                table.insert({'name': getHid(f).split("/")[-1],
                                              'uid': file,
                                              'Canary': getExploitMitigation(f, 'Canary'),
                                              'NX': getExploitMitigation(f, 'NX'),
                                              'PIE': getExploitMitigation(f, 'PIE'),
                                              'RELRO': getExploitMitigation(f, 'RELRO')})
                                element_found = True
                                break
        if element_found:
            founded_programs_whitelist.append(programs)

    json = {}
    for i, list_ in enumerate(founded_programs_whitelist):
        tmp = list_.copy()
        name = tmp[0]
        tmp.pop(0)
        json[name] = [element for element in tmp]

    return json


def findConfigs(tree):
    for program in tree:
        for index in tree[program]:
            if index['name'].count('cfn') > 0:
                print(index['name'])
            elif index['name'].count('CFN') > 0:
                print(index['name'])
            elif index['name'].count('conf') > 0:
                print(index['name'])
            elif index['name'].count('Config') > 0:
                print(index['name'])
            else:
                None


def findOtherConfigs(included_files, db):
    db_exist = checkDB(db, ['configs'])
    configs = []
    if db_exist:
        table = db.table('configs')
        for row in table:
            configs.append({'name': row['name'], 'uid': row['uid'],
                            'exploit_mitigations': {'Canary': row['Canary'],
                                                    'NX': row['NX'],
                                                    'PIE': row['PIE'],
                                                    'RELRO': row['RELRO']}})
    else:
        for file in included_files:
            f = get('http://localhost:5000/rest/file_object/' + file).json()
            name = getHid(f).split("/")[-1]
            if name.count('cfn') > 0:
                configs.append({'name': name, 'uid': file,
                                'exploit_mitigations': {'Canary': getExploitMitigation(f, 'Canary'),
                                                        'NX': getExploitMitigation(f, 'NX'),
                                                        'PIE': getExploitMitigation(f, 'PIE'),
                                                        'RELRO': getExploitMitigation(f, 'RELRO')}})
                table = db.table('configs')
                table.insert({'name': name,
                              'uid': file,
                              'Canary': getExploitMitigation(f, 'Canary'),
                              'NX': getExploitMitigation(f, 'NX'),
                              'PIE': getExploitMitigation(f, 'PIE'),
                              'RELRO': getExploitMitigation(f, 'RELRO')})
            elif name.count('CFN') > 0:
                configs.append({'name': name, 'uid': file,
                                'exploit_mitigations': {'Canary': getExploitMitigation(f, 'Canary'),
                                                        'NX': getExploitMitigation(f, 'NX'),
                                                        'PIE': getExploitMitigation(f, 'PIE'),
                                                        'RELRO': getExploitMitigation(f, 'RELRO')}})
                table = db.table('configs')
                table.insert({'name': name,
                              'uid': file,
                              'Canary': getExploitMitigation(f, 'Canary'),
                              'NX': getExploitMitigation(f, 'NX'),
                              'PIE': getExploitMitigation(f, 'PIE'),
                              'RELRO': getExploitMitigation(f, 'RELRO')})
            elif name.count('conf') > 0:
                configs.append({'name': name, 'uid': file,
                                'exploit_mitigations': {'Canary': getExploitMitigation(f, 'Canary'),
                                                        'NX': getExploitMitigation(f, 'NX'),
                                                        'PIE': getExploitMitigation(f, 'PIE'),
                                                        'RELRO': getExploitMitigation(f, 'RELRO')}})
                table = db.table('configs')
                table.insert({'name': name,
                              'uid': file,
                              'Canary': getExploitMitigation(f, 'Canary'),
                              'NX': getExploitMitigation(f, 'NX'),
                              'PIE': getExploitMitigation(f, 'PIE'),
                              'RELRO': getExploitMitigation(f, 'RELRO')})
            elif name.count('Config') > 0:
                configs.append({'name': name, 'uid': file,
                                'exploit_mitigations': {'Canary': getExploitMitigation(f, 'Canary'),
                                                        'NX': getExploitMitigation(f, 'NX'),
                                                        'PIE': getExploitMitigation(f, 'PIE'),
                                                        'RELRO': getExploitMitigation(f, 'RELRO')}})
                table = db.table('configs')
                table.insert({'name': name,
                              'uid': file,
                              'Canary': getExploitMitigation(f, 'Canary'),
                              'NX': getExploitMitigation(f, 'NX'),
                              'PIE': getExploitMitigation(f, 'PIE'),
                              'RELRO': getExploitMitigation(f, 'RELRO')})
            elif name.count('cfg') > 0:
                configs.append({'name': name, 'uid': file,
                                'exploit_mitigations': {'Canary': getExploitMitigation(f, 'Canary'),
                                                        'NX': getExploitMitigation(f, 'NX'),
                                                        'PIE': getExploitMitigation(f, 'PIE'),
                                                        'RELRO': getExploitMitigation(f, 'RELRO')}})
                table = db.table('configs')
                table.insert({'name': name,
                              'uid': file,
                              'Canary': getExploitMitigation(f, 'Canary'),
                              'NX': getExploitMitigation(f, 'NX'),
                              'PIE': getExploitMitigation(f, 'PIE'),
                              'RELRO': getExploitMitigation(f, 'RELRO')})

    json = {'configs': [element for element in configs]}

    return json

def findImportantConfigs(files):
    configs = []
    for file in files:
        name = file['name']
        if name.count('cfn') > 0:
            configs.append({'name': name, 'uid': file['uid'],
                            'exploit_mitigations': {'Canary': file['exploit_mitigations']['Canary'],
                                                    'NX': file['exploit_mitigations']['NX'],
                                                    'PIE': file['exploit_mitigations']['PIE'],
                                                    'RELRO': file['exploit_mitigations']['RELRO']}})

        elif name.count('CFN') > 0:
            configs.append({'name': name, 'uid': file,
                            'exploit_mitigations': {'Canary': file['exploit_mitigations']['Canary'],
                                                    'NX': file['exploit_mitigations']['NX'],
                                                    'PIE': file['exploit_mitigations']['PIE'],
                                                    'RELRO': file['exploit_mitigations']['RELRO']}})

        elif name.count('conf') > 0:
            configs.append({'name': name, 'uid': file['uid'],
                            'exploit_mitigations': {'Canary': file['exploit_mitigations']['Canary'],
                                                    'NX': file['exploit_mitigations']['NX'],
                                                    'PIE': file['exploit_mitigations']['PIE'],
                                                    'RELRO': file['exploit_mitigations']['RELRO']}})

        elif name.count('Config') > 0:
            configs.append({'name': name, 'uid': file['uid'],
                            'exploit_mitigations': {'Canary': file['exploit_mitigations']['Canary'],
                                                    'NX': file['exploit_mitigations']['NX'],
                                                    'PIE': file['exploit_mitigations']['PIE'],
                                                    'RELRO': file['exploit_mitigations']['RELRO']}})

        elif name.count('cfg') > 0:
            configs.append({'name': name, 'uid': file['uid'],
                            'exploit_mitigations': {'Canary': file['exploit_mitigations']['Canary'],
                                                    'NX': file['exploit_mitigations']['NX'],
                                                    'PIE': file['exploit_mitigations']['PIE'],
                                                    'RELRO': file['exploit_mitigations']['RELRO']}})

    return configs