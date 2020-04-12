from modules.requestFunctions import getHid, getExploitMitigation


def getProgramInformationsDict(file, uid, name):
    if file is not None:
        return {'name': getHid(file).split("/")[-1], 'uid': uid,
            'exploit_mitigations': {'Canary': getExploitMitigation(file, 'Canary'),
                                    'NX': getExploitMitigation(file, 'NX'),
                                    'PIE': getExploitMitigation(file, 'PIE'),
                                    'RELRO': getExploitMitigation(file, 'RELRO')}}
    else:
        return {'name': name, 'uid': uid,
                'exploit_mitigations': {'Canary': getExploitMitigation(file, 'Canary'),
                                        'NX': getExploitMitigation(file, 'NX'),
                                        'PIE': getExploitMitigation(file, 'PIE'),
                                        'RELRO': getExploitMitigation(file, 'RELRO')}}
