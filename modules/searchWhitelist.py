from modules.helperFunctions import getProgramInformationsFromJson
from modules.loadData import loadData
from modules.requestFunctions import hasStrings, hasPrintableStrings, getStrings
from requests import get
from modules.db import createTable, checkDB, insertInTable


def searchWithWhitelist(included_files, db):
    json = {}
    whitelist = loadData('whitelist')

    if checkDB(db, whitelist):
        for element in whitelist:
            json[element] = [key for key in db.table(element)]
    else:
        for uid in included_files:
            file = get('http://localhost:5000/rest/file_object/' + uid).json()
            if hasPrintableStrings(file):
                if hasStrings(file):
                    for element in whitelist:
                        for string in getStrings(file):
                            if string.count(element) > 0:
                                table = createTable(db, element)
                                insertInTable(table, getProgramInformationsFromJson(file, uid))
                                break
        if checkDB(db, whitelist):
            for element in whitelist:
                json[element] = [key for key in db.table(element)]
    return json
