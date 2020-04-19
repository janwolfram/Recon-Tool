from json import dumps
from examples import custom_style_2
from PyInquirer import prompt
from modules.promptSetup import setupQuestion


def startInteractive(json):
    mainMenue(json)


def mainMenue(json):
    question = setupQuestion(1, ['meta_data',
                                 'crypto_material',
                                 'software_components',
                                 'whitelist',
                                 'important_configs',
                                 'remaining_configs'])
    analysis = prompt(question, style=custom_style_2)
    if len(analysis) != 0:
        analysis = analysis['analysis']

        if analysis == 'meta_data':
            metaData(json)
        elif analysis == 'crypto_material':
            cryptoMaterial(json)
        elif analysis == 'software_components':
            softwareComponents(json)
        elif analysis == 'whitelist':
            whitelist(json)
        elif analysis == 'important_configs':
            config(json, 'important_configs')
        elif analysis == 'remaining_configs':
            config(json, 'remaining_configs')


def pause(method, json, level_one, index):
    print('Do you want to continue? [y/n]')
    inp = input()
    if inp == 'y':
        question = setupQuestion(7, ['Back', 'Pause prompt'])
        option = prompt(question, style=custom_style_2)
        if len(option) != 0:
            option = option['option']
            if option == 'Back':
                if method == 'metaData':
                    mainMenue(json)
                elif method == 'important_configs':
                    config(json, 'important_configs')
                elif method == 'remaining_configs':
                    config(json, 'remaining_configs')
                elif method == 'software_components':
                    softwareComponentsPrograms(json, level_one)
                elif method == 'materials':
                    programMaterials(json, level_one, index)
                elif method == 'whitelist':
                    whitelistPrograms(json, level_one)
            elif option == 'Pause prompt':
                pause(method, json, level_one, index)
    else:
        return


def metaData(json):
    print(dumps(json['meta_data'], indent=4, sort_keys=False))
    question = setupQuestion(7, ['Back', 'Pause prompt'])
    option = prompt(question, style=custom_style_2)
    if len(option) != 0:
        option = option['option']
    if option == 'Back':
        mainMenue(json)
    elif option == 'Pause prompt':
        pause('metaData', json, None, None)


def cryptoMaterial(json):
    crypto_elements = [key for key in json['crypto_material']]
    crypto_elements.insert(0, '...')

    question = setupQuestion(2, crypto_elements)
    crypto_material = prompt(question, style=custom_style_2)
    if len(crypto_material) != 0:
        crypto_material = crypto_material['crypto_material']

        if crypto_material == '...':
            mainMenue(json)
        else:
            cryptoMaterialPrograms(json, crypto_material)


def cryptoMaterialPrograms(json, crypto_material):
    programlist = [key['name'] for key in json['crypto_material'][crypto_material]]
    programlist.insert(0, '...')
    question = setupQuestion(5, programlist)
    program = prompt(question, style=custom_style_2)
    if len(program) != 0:
        program = program['program']
        if program == '...':
            cryptoMaterial(json)
        else:
            programMaterials(json, crypto_material, programlist.index(program) - 1)


def programMaterials(json, crypto_material, program_index):
    materialList = [material for material in json['crypto_material'][crypto_material][program_index]['material']]

    materialsForPrompt = []
    i = 0
    while i < len(materialList):
        materialsForPrompt.append('material' + str(i))
        i += 1
    materialsForPrompt.insert(0, '...')

    question = setupQuestion(4, materialsForPrompt)
    material = prompt(question, style=custom_style_2)

    if len(material) != 0:
        material = material['material']

        if material == '...':
            cryptoMaterialPrograms(json, crypto_material)
        else:
            print(materialList[int(material[-1])])

            question = setupQuestion(7, ['Back', 'Pause prompt'])
            option = prompt(question, style=custom_style_2)
            if len(option) != 0:
                option = option['option']
                if option == 'Back':
                    programMaterials(json, crypto_material, program_index)
                elif option == 'Pause prompt':
                    pause('materials', json, crypto_material, program_index)


def softwareComponents(json):
    components = [key for key in json['software_components']]
    components.insert(0, '...')

    question = setupQuestion(4, components)
    component = prompt(question, style=custom_style_2)
    if len(component) != 0:
        component = component['software_component']

        if component == '...':
            mainMenue(json)
        else:
            softwareComponentsPrograms(json, component)
            # programs(json, 'software_components', component)


def softwareComponentsPrograms(json, component):
    programlist = [key['name'] for key in json['software_components'][component]]
    programlist.insert(0, '...')
    question = setupQuestion(5, programlist)
    program = prompt(question, style=custom_style_2)
    if len(program) != 0:
        program = program['program']
        if program == '...':
            softwareComponents(json)
        else:
            printFile(json, 'software_components', programlist.index(program) - 1, component)


def config(json, analysis):
    elements = [key['name'] for key in json[analysis]]
    elements.insert(0, '...')

    question = setupQuestion(8, elements)
    list_element = prompt(question, style=custom_style_2)
    if len(list_element) != 0:
        list_element = list_element['choose']
        if list_element == '...':
            mainMenue(json)
        else:
            printFile(json, analysis, elements.index(list_element) - 1, None)


def whitelist(json):
    elements = [key for key in json['whitelist']]
    elements.insert(0, '...')

    question = setupQuestion(6, elements)
    list_element = prompt(question, style=custom_style_2)
    if len(list_element) != 0:
        list_element = list_element['choose']

        if list_element == '...':
            mainMenue(json)
        else:
            whitelistPrograms(json, list_element)


def whitelistPrograms(json, list_element):
    programlist = [key['name'] for key in json['whitelist'][list_element]]
    programlist.insert(0, '...')
    question = setupQuestion(5, programlist)
    program = prompt(question, style=custom_style_2)
    if len(program) != 0:
        program = program['program']
        if program == '...':
            whitelist(json)
        else:
            printFile(json, 'whitelist', programlist.index(program) - 1, list_element)


def printFile(json, analysis, index, level_one):
    if analysis == 'important_configs' or analysis == 'remaining_configs':
        print(dumps(json[analysis][index], indent=4, sort_keys=False))
    if analysis == "software_components" or analysis == 'whitelist' or analysis == 'crypto_material':
        print(dumps(json[analysis][level_one][index], indent=4, sort_keys=False))

    question = setupQuestion(7, ['Back', 'Pause prompt'])
    option = prompt(question, style=custom_style_2)
    if len(option) != 0:
        option = option['option']
        if option == 'Back':
            if analysis == 'whitelist':
                whitelistPrograms(json, level_one)
            elif analysis == 'software_components':
                softwareComponentsPrograms(json, level_one)
            elif analysis == 'crypto_material':
                cryptoMaterialPrograms(json, level_one)
            elif analysis == 'important_configs' or analysis == 'remaining_configs':
                config(json, analysis)
        elif option == 'Pause prompt':
            pause(analysis, json, level_one, index)
