"""Calculate agreement metrics for time-aligned paired observations."""
import argparse
import csv
import math
from pathlib import Path


def metrics(reference, proposed):
    if len(reference) != len(proposed) or not reference:
        raise ValueError('Nonempty equal-length paired series required')
    n = len(reference)
    diffs = [p - r for r, p in zip(reference, proposed)]
    mae = sum(abs(d) for d in diffs) / n
    rmse = math.sqrt(sum(d*d for d in diffs) / n)
    bias = sum(diffs) / n
    max_abs = max(abs(d) for d in diffs)
    mr, mp = sum(reference)/n, sum(proposed)/n
    cov = sum((r-mr)*(p-mp) for r,p in zip(reference,proposed))
    denom = math.sqrt(sum((r-mr)**2 for r in reference)*sum((p-mp)**2 for p in proposed))
    pearson = cov/denom if denom else float('nan')
    return dict(n=n, MAE=mae, RMSE=rmse, bias=bias, maximum_absolute_difference=max_abs, pearson_r=pearson)


def load_pairs(path):
    result = {}
    with Path(path).open(newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            name = row['variable'].strip().lower()
            result.setdefault(name, ([], []))
            result[name][0].append(float(row['reference']))
            result[name][1].append(float(row['proposed']))
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('paired_csv', help='CSV columns: variable,reference,proposed')
    args = p.parse_args()
    for name, (ref, proposed) in load_pairs(args.paired_csv).items():
        print(name, metrics(ref, proposed))
