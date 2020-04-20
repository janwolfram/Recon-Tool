from modules.helperFunctions import getProgramInformationsDict
from modules.loadData import loadData
from modules.requestFunctions import hasStrings, hasPrintableStrings, getStrings
from requests import get
from modules.db import createTable, getProgramInformations, checkDB, insertInTable


def searchWithWhitelist(included_files, db):
    founded_programs_whitelist = None
    whitelist = loadData('whitelist')
    db_created = checkDB(db, whitelist)

    if db_created:
        founded_programs_whitelist = printWhitelist(whitelist, db)

    else:
        for uid in included_files:
            file = get('http://localhost:5000/rest/file_object/' + uid).json()
            if hasPrintableStrings(file):
                if hasStrings(file):
                    for element in whitelist:
                        for string in getStrings(file):
                            if string.count(element) > 0:
                                table = createTable(db, element)
                                insertInTable(table, getProgramInformationsDict(file, uid))
                                break
        if checkDB(db, whitelist):
            founded_programs_whitelist = printWhitelist(whitelist, db)
    json = {}
    for element in enumerate(founded_programs_whitelist):
        element_list = element[1].copy()
        name = element_list[0]
        element_list.pop(0)
        json[name] = [element for element in element_list]
    return json


def printWhitelist(whitelist, db):
    founded_programs = []
    for element in whitelist:
        programs = [element]
        table = db.table(element)
        for row in table:
            programs.append(getProgramInformations(row))
        founded_programs.append(programs)
    return founded_programs
