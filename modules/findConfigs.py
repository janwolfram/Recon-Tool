from modules.db import getProgramInformations, checkDB, createTable, insertInTable
from modules.helperFunctions import getProgramInformationsFromJson, getProgramInformationsFromDict
from modules.loadData import loadData
from modules.requestFunctions import getHid
from requests import get


def findImportantConfigs(files, configs):
    important_configs = []
    for file in files:
        name = file['name']
        if name.count('cfn') > 0:
            important_configs.append(getProgramInformationsFromDict(name, file['uid'], file))
        elif name.count('CFN') > 0:
            important_configs.append(getProgramInformationsFromDict(name, file['uid'], file))
        elif name.count('conf') > 0:
            important_configs.append(getProgramInformationsFromDict(name, file['uid'], file))
        elif name.count('Config') > 0:
            important_configs.append(getProgramInformationsFromDict(name, file['uid'], file))
        elif name.count('cfg') > 0:
            important_configs.append(getProgramInformationsFromDict(name, file['uid'], file))
    for config in configs:
        if isImportantConfig(config):
            important_configs.append(config)
    return important_configs


def isImportantConfig(config):
    lookingFor = loadData('configs')
    for element in lookingFor:
        if config['name'].count(element) > 0:
            return True
    return False


def findConfigs(included_files, db):
    configs = []
    if checkDB(db, ['configs']):
        table = db.table('configs')
        for row in table:
            configs.append(getProgramInformations(row))
    else:
        for uid in included_files:
            file = get('http://localhost:5000/rest/file_object/' + uid).json()
            name = getHid(file).split("/")[-1]
            if name.count('cfn') > 0:
                configs.append(getProgramInformationsFromJson(file, uid))
                table = createTable(db, 'configs')
                insertInTable(table, getProgramInformationsFromJson(file, uid))
            elif name.count('CFN') > 0:
                configs.append(getProgramInformationsFromJson(file, uid))
                table = createTable(db, 'configs')
                insertInTable(table, getProgramInformationsFromJson(file, uid))
            elif name.count('conf') > 0:
                configs.append(getProgramInformationsFromJson(file, uid))
                table = createTable(db, 'configs')
                insertInTable(table, getProgramInformationsFromJson(file, uid))
            elif name.count('Config') > 0:
                configs.append(getProgramInformationsFromJson(file, uid))
                table = createTable(db, 'configs')
                insertInTable(table, getProgramInformationsFromJson(file, uid))
            elif name.count('cfg') > 0:
                configs.append(getProgramInformationsFromJson(file, uid))
                table = createTable(db, 'configs')
                insertInTable(table, getProgramInformationsFromJson(file, uid))

    json = {'configs': [element for element in configs]}
    return json
