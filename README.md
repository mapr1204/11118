# Low-Cost Cyber-Physical Architecture for Monitoring Industrial DC Electrical Signals

**Status: reference reconstruction from the published manuscript, not the original experimental source code.**

This repository reconstructs the procedures in Algorithm 1 (MCC 128 acquisition and engineering-unit conversion) and Algorithm 2 (ThingSpeak HTTPS upload), and supplies independent scripts for agreement metrics and comparison plots. It does **not** contain original Multilazo observations or original offset/gain calibration coefficients. Exact reproduction of the manuscript's Table I and Figs. 7–8 is therefore **not currently possible**. Do not describe these scripts as the original validated implementation.

## Manuscript parameters
- Raspberry Pi 5 + MCC 128 DAQ-HAT, differential mode, ±10 V range, 16-bit ADC.
- HW-685 modules condition 4–20 mA signals to nominal 1–5 VDC.
- Nominal monitored ranges: pressure 0–6 bar, level 0–300 L, temperature 20–60 °C (type J thermocouple with active transmitter).
- Acquisition interval 15 s; ThingSpeak transmission interval 15 s; fields PT3→field1, LE2→field2, TE2→field3.
- The manuscript does not establish actual MCC 128 channel mapping or measured offset/gain. Defaults in `acquisition/mcc128_acquisition.py` are **assumptions for demonstration**, not recovered settings. Note: channel selection and wiring must be verified before connecting any industrial signals.

## Setup
```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```
Hardware acquisition requires a Raspberry Pi with an MCC 128 and the manufacturer's DAQ HAT Python package/system drivers installed separately. Check the vendor documentation and hardware wiring before use.

## Hardware acquisition (requires Raspberry Pi and DAQ)
```bash
python acquisition/mcc128_acquisition.py --out data/acquired.csv --period 15 --count 10
```
Configure the true channel IDs, calibration offsets/gains, and transmitter scaling before running. This example has no GPIO lamp-control implementation because the paper does not specify GPIO pin, electrical interface, or threshold.

## ThingSpeak upload
```bash
export THINGSPEAK_WRITE_API_KEY='YOUR_PRIVATE_KEY'
python cloud/thingspeak_upload.py --csv data/acquired.csv --once
```
Never publish API keys. The uploader sends the most recent CSV row and retries failed uploads; it does not guarantee every acquired sample is transmitted, especially after a network outage.

## Reproduce analyses (original paired CSV required)
Prepare `data/paired_measurements.csv` with columns `variable,reference,proposed` and one row per time-aligned pair. The source paper says Multilazo readings were rounded to two decimal places. Reproduce the authors' actual synchronization and comparison procedures before claiming numeric equivalence.
```bash
python analysis/calculate_metrics.py data/paired_measurements.csv
python analysis/generate_figures.py data/paired_measurements.csv --outdir figures
```
Metrics use differences `proposed - reference`; RMSE is population root-mean-square; Pearson's r is computed on paired observations.

## Published results (reported values, not recalculated here)
| Metric | Pressure (bar) | Level (L) | Temperature (°C) |
|---|---:|---:|---:|
| Paired samples | 116 | 116 | 106 |
| MAE | 0.002696 | 0.002684 | 0.002412 |
| RMSE | 0.003180 | 0.003026 | 0.002851 |
| Bias | -0.000328 | -0.000158 | +0.000258 |
| Max absolute difference | 0.008789 | 0.004917 | 0.004971 |

The article reports Pearson r > 0.997 for all three variables in the selected trial. It also describes 21 trials, but provides detailed quantitative statistics only for the selected trial. These figures cannot be independently verified from summary values alone.

## Reproducibility limitations
1. Original software, CSV data, calibration coefficients, and time-alignment rules are unavailable.
2. GPIO indicator-lamp pin and threshold are unspecified; not implemented.
3. Real hardware execution, cloud integration, and exact quantitative reproduction have **not** been validated for this reconstructed package.
4. Signal wiring and safety must be checked by a qualified person before field use.

This repository is intended as a transparent starting point for subsequent verification and publication of the original artifacts when available.
