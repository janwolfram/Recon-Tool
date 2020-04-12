from modules.helperFunctions import getProgramInformationsDict
from modules.loadData import loadWhitelist
from modules.requestFunctions import *
from requests import get
from modules.db import *


def searchWithWhitelist(included_files, db):
    whitelist = loadWhitelist()
    founded_programs_whitelist = []
    for element in whitelist:
        element_found = False
        programs = [element]
        if checkDB(db, whitelist):
            table = db.table(element)
            element_found = True
            for row in table:
                programs.append(getProgramInformations(row))
        else:
            for uid in included_files:
                file = get('http://localhost:5000/rest/file_object/' + uid).json()
                if hasPrintableStrings(file):
                    if hasStrings(file):
                        for string in getStrings(file):
                            if string.count(element) > 0:
                                programs.append(getProgramInformationsDict(file, uid, None))
                                table = createTable(db, element)
                                insertInTable(table, getProgramInformationsDict(file, uid, None))
                                element_found = True
                                break
                            else:
                                createTable(db, element)
        if element_found:
            founded_programs_whitelist.append(programs)

    json = {}
    for i, element in enumerate(founded_programs_whitelist):
        element_list = element.copy()
        name = element_list[0]
        element_list.pop(0)
        json[name] = [element for element in element_list]
    return json


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