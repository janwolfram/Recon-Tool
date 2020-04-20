from modules.requestFunctions import getHid, getExploitMitigation


def getProgramInformationsFromJson(file, uid):
    return {'name': getHid(file).split("/")[-1], 'uid': uid,
            'exploit_mitigations': {'Canary': getExploitMitigation(file, 'Canary'),
                                    'NX': getExploitMitigation(file, 'NX'),
                                    'PIE': getExploitMitigation(file, 'PIE'),
                                    'RELRO': getExploitMitigation(file, 'RELRO')}}


def getProgramInformationsFromDict(name, uid, file):
    return {'name': name, 'uid': uid,
            'exploit_mitigations': {'Canary': file['exploit_mitigations']['Canary'],
                                    'NX': file['exploit_mitigations']['NX'],
                                    'PIE': file['exploit_mitigations']['PIE'],
                                    'RELRO': file['exploit_mitigations']['RELRO']}}
