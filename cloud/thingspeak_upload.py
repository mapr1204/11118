"""Reference reconstruction of Algorithm 2; reads latest CSV record."""
import argparse
import csv
import os
import time
from pathlib import Path
import requests

FIELDS = {'PT3': 'field1', 'LE2': 'field2', 'TE2': 'field3'}
URL = 'https://api.thingspeak.com/update'

def latest_row(path):
    with Path(path).open(newline='', encoding='utf-8') as f:
        rows = csv.DictReader(f)
        return next(reversed(list(rows)), None)

def send_once(path, key):
    row = latest_row(path)
    if row is None:
        raise ValueError('CSV has no records')
    payload = {'api_key': key}
    payload.update({field: row[name] for name, field in FIELDS.items() if row.get(name)})
    for retry in range(3):
        try:
            response = requests.post(URL, data=payload, timeout=10)
            response.raise_for_status()
            entry_id = int(response.text.strip())
            if entry_id > 0:
                print('TS_OK', entry_id)
                return True
        except (requests.RequestException, ValueError) as exc:
            print('TS_ERR', retry + 1, exc)
        time.sleep(2 * (retry + 1))
    return False

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--csv', default='data/acquired.csv')
    p.add_argument('--once', action='store_true')
    a = p.parse_args()
    key = os.getenv('THINGSPEAK_WRITE_API_KEY')
    if not key:
        raise SystemExit('Set THINGSPEAK_WRITE_API_KEY in the environment; never commit it.')
    while True:
        start = time.monotonic()
        send_once(a.csv, key)
        if a.once:
            break
        time.sleep(max(0, 15 - (time.monotonic() - start)))
