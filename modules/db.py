from tinydb import TinyDB


def setupDB(uid):
    return TinyDB('db/' + uid + '.json')


def checkDB(db, whitelist):
    for element in whitelist:
        if len(db.table(element)) > 0:
            return True
    return False


def getProgramInformations(row):
    return {'name': row['name'], 'uid': row['uid'],
            'exploit_mitigations': {'Canary': row['exploit_mitigations']['Canary'],
                                    'NX': row['exploit_mitigations']['NX'],
                                    'PIE': row['exploit_mitigations']['PIE'],
                                    'RELRO': row['exploit_mitigations']['RELRO']}}


def createTable(db, element):
    return db.table(element)


def insertInTinydbTable(table, dict):
    table.insert(dict)
