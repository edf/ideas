import json

with open('pattern.json') as f:
    data = json.load(f)
    # print(data)
    for things in data['content']:
        item: object
        for item in things['items']:
            print('item: ' + item.replace("-suffix", ''))
