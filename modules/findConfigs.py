from modules.db import getProgramInformations, checkDB, createTable, insertInTable
from modules.helperFunctions import getProgramInformationsDict, getProgramInformationsFromJsonDict
from modules.requestFunctions import getHid
from requests import get


def findImportantConfigs(files):
    important_configs = []
    for file in files:
        name = file['name']
        if name.count('cfn') > 0:
            important_configs.append(getProgramInformationsFromJsonDict(name, file['uid'], file))
        elif name.count('CFN') > 0:
            important_configs.append(getProgramInformationsFromJsonDict(name, file['uid'], file))
        elif name.count('conf') > 0:
            important_configs.append(getProgramInformationsFromJsonDict(name, file['uid'], file))
        elif name.count('Config') > 0:
            important_configs.append(getProgramInformationsFromJsonDict(name, file['uid'], file))
        elif name.count('cfg') > 0:
            important_configs.append(getProgramInformationsFromJsonDict(name, file['uid'], file))
    return important_configs


def findRemainingConfigs(included_files, db):
    remaining_configs = []
    if checkDB(db, ['remaining_configs']):
        table = db.table('remaining_configs')
        for row in table:
            remaining_configs.append(getProgramInformations(row))
    else:
        for uid in included_files:
            file = get('http://localhost:5000/rest/file_object/' + uid).json()
            name = getHid(file).split("/")[-1]
            if name.count('cfn') > 0:
                remaining_configs.append(getProgramInformationsDict(file, uid))
                table = createTable(db, 'remaining_configs')
                insertInTable(table, getProgramInformationsDict(file, uid))
            elif name.count('CFN') > 0:
                remaining_configs.append(getProgramInformationsDict(file, uid))
                table = createTable(db, 'remaining_configs')
                insertInTable(table, getProgramInformationsDict(file, uid))
            elif name.count('conf') > 0:
                remaining_configs.append(getProgramInformationsDict(file, uid))
                table = createTable(db, 'remaining_configs')
                insertInTable(table, getProgramInformationsDict(file, uid))
            elif name.count('Config') > 0:
                remaining_configs.append(getProgramInformationsDict(file, uid))
                table = createTable(db, 'remaining_configs')
                insertInTable(table, getProgramInformationsDict(file, uid))
            elif name.count('cfg') > 0:
                remaining_configs.append(getProgramInformationsDict(file, uid))
                table = createTable(db, 'remaining_configs')
                insertInTable(table, getProgramInformationsDict(file, uid))

    json = {'remaining_configs': [element for element in remaining_configs]}
    return json
