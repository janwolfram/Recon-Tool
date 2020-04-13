from termcolor import colored


def prettyPrint(json):
    print(colored('[+]', 'green'), colored('device_name:', 'blue'), json['meta_data'][0])
    print(colored('[+]', 'green'), colored('vendor:', 'blue'), json['meta_data'][1])
    print(colored('[+]', 'green'), colored('device_class:', 'blue'), json['meta_data'][2])
    print(colored('[+]', 'green'), colored('release_date:', 'blue'), json['meta_data'][3])
    print(colored('[+]', 'green'), colored('version:', 'blue'), json['meta_data'][4])
    print('--------------------------------------------------------')
    print(colored('[+]', 'green'), colored('crypto_material:', 'yellow'))
    for key in json['crypto_material']:
        print(colored('\n[+]', 'green'), colored('key:', 'blue'), colored(key, 'red'))
        print(colored('--------------------------------------------------------', 'red'))
        liste = json['crypto_material'][key]
        if key == 'SSLCertificate':
            for e in liste:
                print(colored('\n[+]', 'green'), colored('name:', 'blue'), e['name'])
                print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
        else:
            for i, e in enumerate(liste):
                print(colored('\n[+]', 'green'), colored('name:', 'blue'), e['name'])
                print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
                for i, material in enumerate(e['material']):
                    if i < 2:
                        print(material)
                        if i < 1 and i != len(liste) - 1:
                            print(colored('--------------------------------------------------------', 'white'))
                    else:
                        break
                if i != len(e['material']) - 1:
                    left = (len(e['material']) - 1) - i
                    print(colored('[+]', 'green'), colored(str(left) + ' elements left', 'red'),
                          colored('[use interactive mode to see all]', 'yellow'))
                if i != len(liste) - 1:
                    print(colored('--------------------------------------------------------', 'blue'))
        print(colored('--------------------------------------------------------', 'red'))

    # print(json['crypto_material']['SSLCertificate'][0]['material'][0])

    print(colored('\n[+]', 'green'), colored('software_components:\n', 'yellow'))
    for key in json['software_components']:
        print(colored('--------------------------------------------------------', 'red'))
        print(colored('[+]', 'green'), colored('key:', 'blue'), colored(key + '\n', 'red'))
        liste = json['software_components'][key]
        for i, e in enumerate(liste):
            if i < 10:
                print(colored('[+]', 'green'), colored('name:', 'blue'), e['name'])
                print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
                print(colored('[+]', 'green'), colored('exploit_mitigations:', 'blue'))
                print(colored('    ->', 'green'), colored('Canary:', 'blue'), e['exploit_mitigations']['Canary'])
                print(colored('    ->', 'green'), colored('NX:', 'blue'), e['exploit_mitigations']['NX'])
                print(colored('    ->', 'green'), colored('PIE:', 'blue'), e['exploit_mitigations']['PIE'])
                print(colored('    ->', 'green'), colored('RELRO:', 'blue'), e['exploit_mitigations']['RELRO'])
                if i != len(liste) - 1:
                    print(colored('--------------------------------------------------------', 'blue'))
            else:
                break
        if i != len(liste) - 1:
            left = len(liste) - 10
            print(colored('[+]', 'green'), colored(str(left) + ' elements left', 'red'),
                  colored('[use interactive mode to see all]', 'yellow'))
        print(colored('--------------------------------------------------------\n', 'red'))

    print(colored('\n[+]', 'green'), colored('whitelist:\n', 'yellow'))
    for key in json['whitelist']:
        print(colored('--------------------------------------------------------', 'red'))
        liste = json['whitelist'][key]
        if len(liste) > 0:
            print(colored('[+]', 'green'), colored('key:', 'blue'), colored(key + '\n', 'red'))
        else:
            print(colored('[-]', 'red'), colored('key:', 'blue'), colored(key, 'red'))
        for i, e in enumerate(liste):
            print(colored('[+]', 'green'), colored('name:', 'blue'), e['name'])
            print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
            print(colored('[+]', 'green'), colored('exploit_mitigations:', 'blue'))
            print(colored('    ->', 'green'), colored('Canary:', 'blue'), e['exploit_mitigations']['Canary'])
            print(colored('    ->', 'green'), colored('NX:', 'blue'), e['exploit_mitigations']['NX'])
            print(colored('    ->', 'green'), colored('PIE:', 'blue'), e['exploit_mitigations']['PIE'])
            print(colored('    ->', 'green'), colored('RELRO:', 'blue'), e['exploit_mitigations']['RELRO'])
            if i != len(liste) - 1:
                print(colored('--------------------------------------------------------', 'blue'))
        print(colored('--------------------------------------------------------\n', 'red'))

    print(colored('\n[+]', 'green'), colored('important_configs:\n', 'yellow'))
    for i, e in enumerate(json['important_configs']):
        print(colored('[+]', 'green'), colored('name:', 'blue'), e['name'])
        print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
        print(colored('[+]', 'green'), colored('exploit_mitigations:', 'blue'))
        print(colored('    ->', 'green'), colored('Canary:', 'blue'), e['exploit_mitigations']['Canary'])
        print(colored('    ->', 'green'), colored('NX:', 'blue'), e['exploit_mitigations']['NX'])
        print(colored('    ->', 'green'), colored('PIE:', 'blue'), e['exploit_mitigations']['PIE'])
        print(colored('    ->', 'green'), colored('RELRO:', 'blue'), e['exploit_mitigations']['RELRO'])
        if i != len(json['important_configs']) - 1:
            print(colored('--------------------------------------------------------', 'blue'))

    print(colored('\n[+]', 'green'), colored('remaining_configs:\n', 'yellow'))
    for i, e in enumerate(json['configs']):
        if i < 10:
            print(colored('[+]', 'green'), colored('name:', 'blue'), e['name'])
            print(colored('[+]', 'green'), colored('uid:', 'blue'), e['uid'])
            print(colored('[+]', 'green'), colored('exploit_mitigations:', 'blue'))
            print(colored('    ->', 'green'), colored('Canary:', 'blue'), e['exploit_mitigations']['Canary'])
            print(colored('    ->', 'green'), colored('NX:', 'blue'), e['exploit_mitigations']['NX'])
            print(colored('    ->', 'green'), colored('PIE:', 'blue'), e['exploit_mitigations']['PIE'])
            print(colored('    ->', 'green'), colored('RELRO:', 'blue'), e['exploit_mitigations']['RELRO'])
            if i != len(json['configs']) - 1:
                print(colored('--------------------------------------------------------', 'blue'))
        else:
            break
    if i != len(json['configs']) - 1:
        left = len(json['configs']) - 10
        print(colored('[+]', 'green'), colored(str(left) + ' elements left', 'red'),
              colored('[use interactive mode to see all]', 'yellow'))