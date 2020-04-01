from json import (dumps, loads)
from copy import deepcopy


def findComponentInJson(t, c):
    out = []

    def findComponent(tree, component):
        for key, value in tree.items():
            if isinstance(value, dict):
                if key == component:
                    out.append(dumps({component: deepcopy(value)}))
                else:
                    findComponent(value, component)
            else:
                if key == component:
                    out.append(dumps({component: deepcopy(value)}))

    findComponent(t, c)
    return out


def printComponent(components):
    for component in components:
        print(dumps(loads(component), indent=4, sort_keys=True))
