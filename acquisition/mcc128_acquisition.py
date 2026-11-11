"""Reference reconstruction of Algorithm 1; not the authors' original software."""
import argparse
import csv
import time
from datetime import datetime, timezone
from pathlib import Path

CHANNELS = [
    # Replace channel IDs, offsets, gains, and voltage spans with measured settings.
    dict(name='PT3', ch=0, vmin=1., vmax=5., xmin=0., xmax=6., offset=0., gain=1.),
    dict(name='LE2', ch=1, vmin=1., vmax=5., xmin=0., xmax=300., offset=0., gain=1.),
    dict(name='TE2', ch=2, vmin=1., vmax=5., xmin=20., xmax=60., offset=0., gain=1.),
]

def engineering_units(raw_voltage, cfg):
    corrected = (raw_voltage + cfg['offset']) * cfg['gain']
    clipped = max(cfg['vmin'], min(cfg['vmax'], corrected))
    return cfg['xmin'] + (clipped - cfg['vmin']) / (cfg['vmax'] - cfg['vmin']) * (cfg['xmax'] - cfg['xmin'])

def acquire(out, period=15., count=0):
    try:
        from daqhats import mcc128, OptionFlags, AnalogInputMode, AnalogInputRange
    except ImportError as exc:
        raise SystemExit('Install the vendor daqhats package on the Raspberry Pi before hardware acquisition.') from exc
    from daqhats import hat_list, HatIDs
    hats = hat_list(filter_by_id=HatIDs.MCC_128)
    if not hats:
        raise SystemExit('No MCC 128 detected.')
    dev = mcc128(hats[0].address)
    dev.a_in_mode_write(AnalogInputMode.DIFF)
    dev.a_in_range_write(AnalogInputRange.BIP_10V)
    path = Path(out)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp'] + [c['name'] for c in CHANNELS])
        if path.stat().st_size == 0:
            writer.writeheader()
        n = 0
        while count == 0 or n < count:
            start = time.monotonic()
            row = {'timestamp': datetime.now(timezone.utc).isoformat()}
            for c in CHANNELS:
                row[c['name']] = engineering_units(dev.a_in_read(c['ch'], OptionFlags.DEFAULT), c)
            writer.writerow(row)
            f.flush()
            n += 1
            time.sleep(max(0., period - (time.monotonic() - start)))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='data/acquired.csv')
    p.add_argument('--period', type=float, default=15.)
    p.add_argument('--count', type=int, default=0, help='0 = run continuously')
    a = p.parse_args()
    acquire(a.out, a.period, a.count)
