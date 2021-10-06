import json
import os

import requests

data_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'ARScanner.json')


def get(protocol: str, address: str) -> list:
    try:
        print('peer', '{}://{}/'.format(protocol, address))
        resp = requests.get(
            '{}://{}/peers'.format(protocol, address), timeout=2.0).json()  # a timeout is set to speed up the process
        assert isinstance(resp, list)
        return [('http', address) for address in resp]
    except requests.exceptions.Timeout:
        # this is a quite common exception, as some of the peers are unreachable due to firewall or proxy
        print('error', 'peer unreachable')
        return []
    except Exception as err:
        print('error', err)
        return []


if __name__ == '__main__':
    if os.path.isfile(data_path):
        with open(data_path, 'r', encoding='utf-8') as fin:
            data = json.load(fin)
        gateways = set(map(tuple, data['all']))
    else:
        gateways = {('https', 'arweave.net'), ('https', 'arweave.live')}
    reachable = set()

    try:
        while True:
            copied = gateways.copy()
            for obj in copied:
                protocol, address = obj
                peers = get(protocol, address)
                if len(peers) > 0:
                    reachable.add(obj)
                    gateways.update(peers)
                print('{} peers found, {} peers reachable (Press Ctrl + C and open ARScanner.json for details)'
                      .format(len(gateways), len(reachable)))
    except KeyboardInterrupt:
        gateways = sorted(list(map(list, gateways)))
        reachable = sorted(list(map(list, reachable)))
        data = {'all': gateways, 'reachable': reachable}
        with open(data_path, 'w', encoding='utf-8') as fout:
            json.dump(data, fout,
                      ensure_ascii=False, indent=2)
