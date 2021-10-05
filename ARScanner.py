import json
import os

import requests

current = os.path.dirname(os.path.abspath(__file__))


def get(protocol: str, address: str) -> list:
    try:
        print(protocol, address)
        resp = requests.get(
            '{}://{}/peers'.format(protocol, address), timeout=2.0).json()
        assert isinstance(resp, list)
        return [('http', address) for address in resp]
    except Exception as err:
        print('error', err)
        return []


if __name__ == '__main__':
    with open(os.path.join(current, 'ARScanner.json'), 'r', encoding='utf-8') as fin:
        gateways = json.load(fin)
    gateways = set(map(tuple, gateways))

    try:
        while True:
            copied = gateways.copy()
            for obj in copied:
                protocol, address = obj
                gateways.update(get(protocol, address))
                print(len(gateways))
    except KeyboardInterrupt:
        gateways = sorted(list(map(list, gateways)))
        with open(os.path.join(current, 'ARScanner.json'), 'w', encoding='utf-8') as fout:
            json.dump(gateways, fout,
                      ensure_ascii=False, indent=2)
