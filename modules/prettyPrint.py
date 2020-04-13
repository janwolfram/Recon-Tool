from termcolor import colored


def prettyPrint(json):
    printMetaData(json)
    printCryptoMaterial(json)
    printSoftwareComponents(json)
    printWhitelist(json)
    printImportantConfigs(json)
    printRemainingConfigs(json)


def printMetaData(json):
    print(colored('[+]', 'green'), colored('meta_data:', 'yellow'))
    seperator('yellow')
    printData('device_name', json['meta_data'][0])
    printData('vendor', json['meta_data'][1])
    printData('device_class', json['meta_data'][2])
    printData('release_date', json['meta_data'][3])
    printData('version', json['meta_data'][4])
    seperator('yellow')


def printCryptoMaterial(json):
    print(colored('\n[+]', 'green'), colored('crypto_material:\n', 'yellow'))
    seperator('yellow')
    for key in json['crypto_material']:
        seperator('red')
        print(colored('[+]', 'green'), colored('key:', 'blue'), colored(key + '\n', 'red'))
        keys = json['crypto_material'][key]
        if key == 'SSLCertificate':
            for crypto_material in keys:
                printData('name', crypto_material['name'])
                printData('uid', crypto_material['uid'])
                print(colored('[+]', 'green'), colored('[use interactive/json mode to see materials]', 'yellow'))
        else:
            for i, crypto_material in enumerate(keys):
                printData('name', crypto_material['name'])
                printData('uid', crypto_material['uid'])
                for j, material in enumerate(crypto_material['material']):
                    if j < 2:
                        print(material)
                        if j < 1 and j != len(keys) - 1:
                            seperator('white')
                    else:
                        break
                if j != len(crypto_material['material']) - 1:
                    left = (len(crypto_material['material']) - 1) - i
                    print(colored('[+]', 'green'), colored(str(left) + ' elements left', 'red'),
                          colored('[use interactive/json mode to see all]', 'yellow'))
                if i != len(keys) - 1:
                    seperator('blue')
        seperator('red')
        print('\n', end='')
    seperator('yellow')


def printSoftwareComponents(json):
    print(colored('\n[+]', 'green'), colored('software_components:\n', 'yellow'))
    seperator('yellow')
    for key in json['software_components']:
        seperator('red')
        print(colored('[+]', 'green'), colored('key:', 'blue'), colored(key + '\n', 'red'))
        keys = json['software_components'][key]
        for i, component in enumerate(keys):
            if i < 10:
                printProgram(component)
                if i != len(keys) - 1:
                    seperator('blue')
            else:
                break
        if i != len(keys) - 1:
            left = len(keys) - 10
            print(colored('[+]', 'green'), colored(str(left) + ' elements left', 'red'),
                  colored('[use interactive mode to see all]', 'yellow'))
        seperator('red')
        print('\n', end='')
    seperator('yellow')


def printWhitelist(json):
    print(colored('\n[+]', 'green'), colored('whitelist:\n', 'yellow'))
    seperator('yellow')
    for key in json['whitelist']:
        seperator('red')
        keys = json['whitelist'][key]
        if len(keys) > 0:
            print(colored('[+]', 'green'), colored('key:', 'blue'), colored(key + '\n', 'red'))
        else:
            print(colored('[-]', 'red'), colored('key:', 'blue'), colored(key, 'red'))
        for i, program in enumerate(keys):
            printProgram(program)
            if i != len(keys) - 1:
                seperator('blue')
        seperator('red')
        print('\n', end='')
    seperator('yellow')


def printImportantConfigs(json):
    print(colored('\n[+]', 'green'), colored('important_configs:\n', 'yellow'))
    seperator('yellow')
    for i, important_config in enumerate(json['important_configs']):
        printProgram(important_config)
        if i != len(json['important_configs']) - 1:
            seperator('blue')
    seperator('yellow')


def printRemainingConfigs(json):
    print(colored('\n[+]', 'green'), colored('remaining_configs:\n', 'yellow'))
    seperator('yellow')
    for i, remaining_config in enumerate(json['remaining_configs']):
        if i < 10:
            printProgram(remaining_config)
            if i != len(json['remaining_configs']) - 1:
                seperator('blue')
        else:
            break
    if i != len(json['remaining_configs']) - 1:
        left = len(json['remaining_configs']) - 10
        print(colored('[+]', 'green'), colored(str(left) + ' elements left', 'red'),
              colored('[use interactive/json mode to see all]', 'yellow'))
    seperator('yellow')


def seperator(color):
    print(colored('--------------------------------------------------------', color))


def printData(value1, value2):
    print(colored('[+]', 'green'), colored(value1, 'blue'), colored(value2, 'white'))


def printProgram(json):
    printData('name', json['name'])
    printData('uid', json['uid'])
    printExploitMitigations(json)


def printExploitMitigations(json):
    print(colored('[+]', 'green'), colored('exploit_mitigations:', 'blue'))
    print(colored('    ->', 'green'), colored('Canary:', 'blue'), json['exploit_mitigations']['Canary'])
    print(colored('    ->', 'green'), colored('NX:', 'blue'), json['exploit_mitigations']['NX'])
    print(colored('    ->', 'green'), colored('PIE:', 'blue'), json['exploit_mitigations']['PIE'])
    print(colored('    ->', 'green'), colored('RELRO:', 'blue'), json['exploit_mitigations']['RELRO'])
