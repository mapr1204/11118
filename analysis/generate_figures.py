"""Generate comparison plots from genuine paired CSV data (not included)."""
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
from calculate_metrics import load_pairs

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('paired_csv')
    p.add_argument('--outdir', default='figures')
    args = p.parse_args()
    Path(args.outdir).mkdir(parents=True, exist_ok=True)
    for name, (reference, proposed) in load_pairs(args.paired_csv).items():
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(reference, label='Multilazo reference')
        ax.plot(proposed, label='Proposed system', alpha=.8)
        ax.set(xlabel='Paired sample index', ylabel=name, title=f'{name}: system comparison')
        ax.legend()
        fig.tight_layout()
        fig.savefig(Path(args.outdir) / f'{name}_comparison.png', dpi=180)
        plt.close(fig)
