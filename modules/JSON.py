from modules.requestFunctions import (getMetaData, getCryptoMaterialSummary, getMaterials, getHid,
                                      getSoftwareComponentsSummary, getExploitMitigation, getFileTypeSummary,
                                      getIncludedFiles, getUnpacked)
from modules.db import setupDB
from modules.searchWhitelist import searchWithWhitelist
from modules.findConfigs import findImportantConfigs
from requests import get


def createReconJSON(tree, uid):
    json = {}
    json['meta_data'] = createMetaData(tree)
    json['crypto_material'] = createCryptoMaterial(tree)
    json['software_components'] = createSoftwareComponents(tree)

    included_files = findIncludedFiles(tree)
    db = setupDB(uid)

    json['whitelist'] = searchWithWhitelist(included_files, db)
    json['important_configs'] = createImportantConfigs(json['whitelist'])


def createMetaData(tree):
    return [getMetaData(tree, "device_name"),
            getMetaData(tree, "vendor"),
            getMetaData(tree, "device_class"),
            getMetaData(tree, "release_date"),
            getMetaData(tree, "version")]


def createCryptoMaterial(tree):
    json = {}
    for key in getCryptoMaterialSummary(tree):
        uids = [uid for uid in tree['firmware']['analysis']['crypto_material']['summary'][key]]
        programs = []
        for uid in uids:
            uid_tree = get('http://localhost:5000/rest/file_object/' + uid).json()
            materials = getMaterials(uid_tree, key)
            programs.append({'name': getHid(uid_tree).split("/")[-1], 'uid': uid,
                             'material': materials})
        json[key] = programs
    return json


def createSoftwareComponents(tree):
    json = {}
    for key in getSoftwareComponentsSummary(tree):
        uids = [uid for uid in tree['firmware']['analysis']['software_components']['summary'][key]]
        programs = []
        for uid in uids:
            uid_tree = get('http://localhost:5000/rest/file_object/' + uid).json()
            programs.append(
                {'name': getHid(uid_tree).split("/")[-1],
                 'uid': uid,
                 'exploit_mitigations': {'Canary': getExploitMitigation(uid_tree, 'Canary'),
                                         'NX': getExploitMitigation(uid_tree, 'NX'),
                                         'PIE': getExploitMitigation(uid_tree, 'PIE'),
                                         'RELRO': getExploitMitigation(uid_tree, 'RELRO')}}
            )
        json[key] = programs
    return json


def findIncludedFiles(tree):
    index_filesystems = findFileSystems(tree)
    included_files = []
    for index in index_filesystems:
        file_system = list(getFileTypeSummary(tree).values())[index][0]
        file_system = get('http://localhost:5000/rest/file_object/' + file_system + '?summary=true').json()
        for file in getIncludedFiles(file_system):
            included_files.append(file)

    if len(included_files) == 0:
        for file in getUnpacked(tree):
            included_files.append(file)
    return included_files


def findFileSystems(tree):
    index_filesystems = []
    for i, key in enumerate(list(getFileTypeSummary(tree).keys())):
        if key.count('filesystem/') > 0:
            index_filesystems.append(i)
    return index_filesystems


def createImportantConfigs(whitelist_tree):
    important_configs = []
    for key in whitelist_tree:
        for config in findImportantConfigs(whitelist_tree[key]):
            important_configs.append(config)
    return important_configs
