from json import loads


def getDeviceName(tree):
    return tree['firmware']['meta_data']['device_name']


def getCryptoMaterial(tree):
    return tree['firmware']['analysis']['crypto_material']['summary']


def getSoftwareComponents(tree):
    return tree['firmware']['analysis']['software_components']['summary']


def getFileType(tree):
    return tree['firmware']['analysis']['file_type']['summary']


def getIncludedFiles(tree):
    return tree['file_object']['meta_data']['included_files']


def hasStrings(file):
    if 'strings' in file['file_object']['analysis']['printable_strings']:
        return True
    else:
        return False


def hasPrintableStrings(file):
    if 'printable_strings' in file['file_object']['analysis']:
        return True
    else:
        return False


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
    else:
        return None


def getUnpacked(tree):
    return tree['firmware']['analysis']['unpacker']['summary']['unpacked']


def getMaterials(tree, key):
    return tree['file_object']['analysis']['crypto_material'][key]['material']


def getDeviceClass(tree):
    return tree['firmware']['meta_data']['device_class']


def getVendor(tree):
    return tree['firmware']['meta_data']['vendor']


def getVerison(tree):
    return tree['firmware']['meta_data']['version']


def getReleaseDate(tree):
    return tree['firmware']['meta_data']['release_date']
