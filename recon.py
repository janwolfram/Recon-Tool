# sudo pip3 install requests PyInquirer
# sudo pip install prompt_toolkit==1.0.14
# python3 recon.py -h


from requests import get
from json import dumps
from json import loads
import argparse
from PyInquirer import prompt
from examples import custom_style_2
from searchJSON import(findComponentInJson, printComponent)


def setupArgparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--uid", help="uid of firmware", required=False)
    parser.add_argument("-c", "--component", help="component you are looking for", required=False)
    return parser.parse_args()


def getDeviceNames(uids):
    device_names = []
    for uid in uids:
        device_name = getDeviceName(uid)
        device_names.append(device_name["device_name"])
    return device_names


def getDeviceName(uid):
    return loads(
        findComponentInJson(get('http://localhost:5000/rest/firmware/' + uid).json(), "device_name")[0])


def getActiveAnalysis(analysis):
    arr = []
    analysis_body = list(analysis.values())[0]
    for key, value in analysis_body.items():
        arr.append(key)
    return arr


def main():
    args = setupArgparse()
    if args.uid and args.component:
        res = get('http://localhost:5000/rest/firmware/' + args.uid + "?summary=true").json()
        printComponent(findComponentInJson(res, args.component))
    else:
        res = get('http://localhost:5000/rest/firmware').json()
        uids = loads(findComponentInJson(res, "uids")[0])["uids"]
        device_names = getDeviceNames(uids)

        analysis = []
        for uid in uids:
            analysis.append(getActiveAnalysis(
                loads(findComponentInJson(get('http://localhost:5000/rest/firmware/' + uid).json(), "analysis")[0])))

        def getAnalysis(a):
            activeTool = 0
            for d in device_names:
                for i, uid in enumerate(uids):
                    if getDeviceName(uid)["device_name"] == d:
                        activeTool = i
            return analysis[activeTool]

        questions = [
            {
                'type': 'list',
                'name': 'firmware',
                'message': 'What firmware you want to examine?',
                'choices': device_names
            },
            {
                'type': 'list',
                'name': 'component',
                'message': 'What analysis do you want to see?',
                'choices': getAnalysis,
                'filter': lambda val: val.lower()
            }
        ]

        answers = prompt(questions, style=custom_style_2)
        # print(answers)

        activeUid = None
        for i, uid in enumerate(uids):
            if getDeviceName(uid)["device_name"] == answers["firmware"]:
                activeUid = uids[i]

        printComponent(findComponentInJson(get('http://localhost:5000/rest/firmware/' + activeUid + "?summary=true"
                                               ).json(), answers["component"]))


if __name__ == '__main__':
    main()
