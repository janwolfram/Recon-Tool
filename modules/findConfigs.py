from modules.helperFunctions import getProgramInformationsDict


def findImportantConfigs(files):
    important_configs = []
    for file in files:
        name = file['name']
        if name.count('cfn') > 0:
            important_configs.append(getProgramInformationsDict(None, file['uid'], name))
        elif name.count('CFN') > 0:
            important_configs.append(getProgramInformationsDict(None, file['uid'], name))
        elif name.count('conf') > 0:
            important_configs.append(getProgramInformationsDict(None, file['uid'], name))
        elif name.count('Config') > 0:
            important_configs.append(getProgramInformationsDict(None, file['uid'], name))
        elif name.count('cfg') > 0:
            important_configs.append(getProgramInformationsDict(None, file['uid'], name))
    return important_configs
