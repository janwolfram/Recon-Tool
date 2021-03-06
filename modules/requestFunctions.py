def getCryptoMaterialSummary(tree):
    return tree['firmware']['analysis']['crypto_material']['summary']


def getSoftwareComponentsSummary(tree):
    return tree['firmware']['analysis']['software_components']['summary']


def getFileTypeSummary(tree):
    return tree['firmware']['analysis']['file_type']['summary']


def getIncludedFiles(tree):
    return tree['file_object']['meta_data']['included_files']


def hasStrings(file):
    if 'strings' in file['file_object']['analysis']['printable_strings']:
        return True


def hasPrintableStrings(tree):
    if 'printable_strings' in tree['file_object']['analysis']:
        return True


def getStrings(tree):
    return tree['file_object']['analysis']['printable_strings']['strings']


def getHid(tree):
    return tree['file_object']['meta_data']['hid']


def getExploitMitigation(tree, exploit):
    if exploit in tree['file_object']['analysis']['exploit_mitigations']:
        return {
            'Canary': tree['file_object']['analysis']['exploit_mitigations']['Canary'],
            'NX': tree['file_object']['analysis']['exploit_mitigations']['NX'],
            'PIE': tree['file_object']['analysis']['exploit_mitigations']['PIE'],
            'RELRO': tree['file_object']['analysis']['exploit_mitigations']['RELRO']
        }[exploit]


def getUnpacked(tree):
    return tree['firmware']['analysis']['unpacker']['summary']['unpacked']


def getMaterials(tree, key):
    return tree['file_object']['analysis']['crypto_material'][key]['material']


def getMetaData(tree, key):
    return tree['firmware']['meta_data'][key]


def getBinary(tree):
    return tree['binary']


def getFirmwareUids(tree):
    return tree['uids']
