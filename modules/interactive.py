from json import dumps
from examples import custom_style_2
from PyInquirer import prompt

from modules.promptSetup import setupQuestion


def startInteractive(json):
    mainMenue(json)


def mainMenue(json):
    question = setupQuestion(2, ['meta_data',
                                 'crypto_material',
                                 'software_components',
                                 'whitelist',
                                 'important_configs',
                                 'remaining_configs'])
    analysis = prompt(question, style=custom_style_2)
    if len(analysis) != 0:
        analysis = analysis['choose']

        if analysis == 'meta_data':
            metaData(json)
        elif analysis == 'crypto_material':
            cryptoMaterial(json)
        elif analysis == 'software_components':
            softwareComponents(json)
        elif analysis == 'whitelist':
            whitelist(json)
        elif analysis == 'important_configs':
            programs(json, 'important_configs', None)
        elif analysis == 'remaining_configs':
            programs(json, 'remaining_configs', None)


def pause(method, json, level_one, level_two):
    print('Do you want to continue? [y/n]')
    inp = input()
    if inp == 'y':
        question = setupQuestion(9, ['Back', 'Pause prompt'])
        option = prompt(question, style=custom_style_2)['options']
        if option == 'Back':
            print(method)
            if method == 'metaData':
                mainMenue(json)
            elif method == 'important_configs':
                programs(json, 'important_configs', level_one)
            elif method == 'remaining_configs':
                programs(json, 'remaining_configs', level_one)
            elif method == 'software_components':
                programs(json, 'software_components', level_one)
            elif method == 'materials':
                materials(json, level_one, level_two)
            elif method == 'whitelist':
                programs(json, 'whitelist', level_one)

        else:
            pause(method, json, level_one, level_two)
    else:
        return


def metaData(json):
    print(dumps(json['meta_data'], indent=4, sort_keys=False))
    question = setupQuestion(9, ['Back', 'Pause prompt'])
    option = prompt(question, style=custom_style_2)
    if len(option) != 0:
        option = option['options']
    if option == 'Back':
        mainMenue(json)
    elif option == 'Pause prompt':
        pause('metaData', json, None, None)


def cryptoMaterial(json):
    crypto_elements = [key for key in json['crypto_material']]
    crypto_elements.insert(0, '...')

    question = setupQuestion(10, crypto_elements)
    crypto_material = prompt(question, style=custom_style_2)
    if len(crypto_material) != 0:
        crypto_material = crypto_material['choose']

        if crypto_material == '...':
            mainMenue(json)
        else:
            programs(json, 'crypto_material', crypto_material)


def softwareComponents(json):
    components = [key for key in json['software_components']]
    components.insert(0, '...')

    question = setupQuestion(10, components)
    component = prompt(question, style=custom_style_2)
    if len(component) != 0:
        component = component['choose']

        if component == '...':
            mainMenue(json)
        else:
            programs(json, 'software_components', component)


def whitelist(json):
    elements = [key for key in json['whitelist']]
    elements.insert(0, '...')

    question = setupQuestion(10, elements)
    list_element = prompt(question, style=custom_style_2)
    if len(list_element) != 0:
        list_element = list_element['choose']

        if list_element == '...':
            mainMenue(json)
        else:
            programs(json, 'whitelist', list_element)


def programs(json, analysis, level_one):
    if level_one is None:
        programlist = [key['name'] for key in json[analysis]]
        programlist.insert(0, '...')
        question = setupQuestion(10, programlist)
        program = prompt(question, style=custom_style_2)
        if len(program) != 0:
            program = program['choose']
            if program == '...':
                mainMenue(json)
            else:
                index = None
                for i, prog in enumerate(programlist):
                    if prog == program:
                        index = i - 1
                print(dumps(json[analysis][index], indent=4, sort_keys=False))
                question = setupQuestion(9, ['Back', 'Pause prompt'])
                option = prompt(question, style=custom_style_2)['options']
                if option == 'Back':
                    programs(json, analysis, None)
                elif option == 'Pause prompt':
                    pause(analysis, json, None, None)
    else:
        programlist = [key['name'] for key in json[analysis][level_one]]
        programlist.insert(0, '...')
        question = setupQuestion(10, programlist)
        program = prompt(question, style=custom_style_2)
        if len(program) != 0:
            program = program['choose']
            if program == '...':
                if analysis == 'crypto_material':
                    cryptoMaterial(json)
                elif analysis == 'software_components':
                    softwareComponents(json)
                elif analysis == 'whitelist':
                    whitelist(json)
            else:
                if analysis == 'crypto_material':
                    materials(json, level_one, program)
                elif analysis == 'software_components':
                    index = None
                    for i, prog in enumerate(programlist):
                        if prog == program:
                            index = i - 1
                    print(dumps(json[analysis][level_one][index], indent=4, sort_keys=False))
                    question = setupQuestion(9, ['Back', 'Pause prompt'])
                    option = prompt(question, style=custom_style_2)['options']
                    if option == 'Back':
                        programs(json, 'software_components', level_one)
                    elif option == 'Pause prompt':
                        pause('software_components', json, level_one, None)
                elif analysis == 'whitelist':
                    index = None
                    for i, prog in enumerate(programlist):
                        if prog == program:
                            index = i - 1
                    print(dumps(json[analysis][level_one][index], indent=4, sort_keys=False))
                    question = setupQuestion(9, ['Back', 'Pause prompt'])
                    option = prompt(question, style=custom_style_2)['options']
                    if option == 'Back':
                        programs(json, 'whitelist', level_one)
                    elif option == 'Pause prompt':
                        pause('whitelist', json, level_one, None)


def materials(json, level_one, level_two):
    materialList = None
    for element in json['crypto_material'][level_one]:
        if element['name'] == level_two:
            materialList = [key for key in element['material']]

    materialsForPrompt = []
    i = 0
    while i < len(materialList):
        materialsForPrompt.append('material' + str(i))
    materialsForPrompt.insert(0, '...')

    question = setupQuestion(10, materialsForPrompt)
    ch = prompt(question, style=custom_style_2)
    if len(ch) != 0:
        ch = ch['choose']

        if ch == '...':
            programs(json, 'crypto_material', level_one)
        else:
            print(materialList[int(ch[-1])])
            question = setupQuestion(9, ['Back', 'Pause prompt'])
            option = prompt(question, style=custom_style_2)['options']
            if option == 'Back':
                materials(json, level_one, level_two)
            elif option == 'Pause prompt':
                pause('materials', json, level_one, level_two)
