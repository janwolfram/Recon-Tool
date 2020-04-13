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
                                programs.append(getProgramInformationsDict(file, uid))
                                table = createTable(db, element)
                                insertInTable(table, getProgramInformationsDict(file, uid))
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
