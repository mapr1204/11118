# Low-Cost Cyber-Physical Architecture for Monitoring Industrial DC Electrical Signals

**Journal:** IEEE Latin America Transactions  
**Manuscript ID:** 11118  
**Repository:** https://github.com/mapr1204/11118

## Authors and affiliations

1. **Mauricio Aarón Pérez-Romero** — Escuela Superior de Ingeniería Mecánica y Eléctrica (ESIME Zacatenco), Instituto Politécnico Nacional (IPN), Mexico City, Mexico. Institutional email: maperezro@ipn.mx.
2. **Jacobo Sandoval-Gutiérrez** — Universidad Autónoma Metropolitana, Unidad Lerma, Estado de México, Mexico. Institutional email: j.sandoval@correo.ler.uam.mx.
3. **Miguel Hernández-Bolaños** — Centro de Innovación y Desarrollo Tecnológico en Cómputo (CIDETEC), Instituto Politécnico Nacional (IPN), Mexico City, Mexico. Institutional email: mbolanos@ipn.mx.

## Overview

This repository contains a **reference reconstruction**, based on the manuscript's pseudocode and reported methods, of a low-cost cyber-physical architecture for monitoring industrial direct-current signals. It covers data acquisition with a Raspberry Pi 5 and an MCC 128 DAQ HAT, conversion of conditioned voltage signals to engineering units, local CSV recording, and HTTPS transmission to ThingSpeak. Separate scripts support statistical comparison and figure generation when paired measurements are available.

**Reproducibility status:** These scripts are reconstructed implementations, **not the original experimentally validated source code**. The original paired Multilazo measurements, calibration coefficients, and synchronization rules have not been included in this repository. Consequently, the numerical values in Table I and the plots in Figs. 7–8 cannot yet be independently reproduced exactly. Hardware execution and ThingSpeak integration have not been validated for this reconstructed package.

## System configuration described in the manuscript

- Processing unit: Raspberry Pi 5.
- Data acquisition: MCC 128 DAQ HAT, 16-bit, three differential channels, ±10 V configured input range.
- Signal conditioning: HW-685 modules, nominal 4–20 mA to 1–5 VDC conversion.
- Monitored quantities: pressure (0–6 bar), level (0–300 L), and temperature (20–60 °C, type J thermocouple with active transmitter).
- Nominal acquisition and ThingSpeak transmission periods: 15 seconds each.
- ThingSpeak field assignment: `PT3` to `field1`, `LE2` to `field2`, `TE2` to `field3`.

## Repository contents and file descriptions

| Path | Purpose | Relation to manuscript |
| --- | --- | --- |
| `README.md` | Project metadata, file descriptions, setup, usage, and limitations. | Reproducibility documentation |
| `requirements.txt` | Lists Python packages required for network communication and plotting; the MCC DAQ HAT driver must be installed separately. | Software dependencies |
| `acquisition/mcc128_acquisition.py` | Reference implementation for MCC 128 analog acquisition, configurable offset/gain correction, conversion to engineering units, and CSV logging. The channel IDs and calibration defaults must be checked before hardware use. | Algorithm 1; Section III |
| `cloud/thingspeak_upload.py` | Reads the latest locally logged CSV record and sends configured fields to ThingSpeak using HTTPS, with retry handling. | Algorithm 2; Section III |
| `analysis/calculate_metrics.py` | Calculates comparison metrics from paired proposed-system and reference-system observations, including MAE, RMSE, bias, maximum absolute difference, and Pearson correlation. | Section IV; Table I |
| `analysis/generate_figures.py` | Generates comparison plots from paired observations. | Comparative plots, Figs. 7–8 |
| `configuration/` | Location for configuration resources supplied with the reconstructed project. Review the files in this folder before setting hardware-specific parameters. | Acquisition and transmission configuration |
| `data/` | Location for acquisition CSV outputs and, when available, time-aligned paired measurements used for statistical analysis. Original experimental data are not currently supplied. | Sections III–IV |
| `tests/` | Automated checks for computational behavior of the reconstructed code; these do not replace hardware validation. | Software checks |

## Installation and software checks

Use Python 3 and install the Python dependencies:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

For physical acquisition, install the MCC DAQ HAT vendor's `daqhats` Python package and system libraries on the Raspberry Pi separately. Confirm wiring, differential channel assignments, input ranges, transmitter scaling, and calibration values before running acquisition.

## Run acquisition (hardware required)

```bash
python acquisition/mcc128_acquisition.py --out data/acquired.csv --period 15 --count 10
```

This command illustrates acquisition of ten records at the configured interval. It does not establish that the default channel assignments or correction coefficients match the original experiments. The optional GPIO lamp described in the paper is not implemented in this reference package because the required pin, electrical interface, and threshold are not specified.

## Upload the latest measurement to ThingSpeak

Set the private Write API Key in the environment (do not commit it to GitHub):

```bash
export THINGSPEAK_WRITE_API_KEY='YOUR_PRIVATE_KEY'
python cloud/thingspeak_upload.py --csv data/acquired.csv --once
```

The uploader uses the latest CSV row. It does not guarantee that every historical record will be delivered after a network interruption.

## Analyze paired measurements

The analysis requires a CSV file named, for example, `data/paired_measurements.csv`, containing these columns:

```csv
variable,reference,proposed
```

Each row must represent a correctly time-aligned pair of observations from the Multilazo reference system and the proposed monitoring system. Populate this file with **actual observations**, not invented or synthetic values, before claiming reproduction of the published results.

```bash
python analysis/calculate_metrics.py data/paired_measurements.csv
python analysis/generate_figures.py data/paired_measurements.csv --outdir figures
```

The reported metric convention is `proposed - reference`; the comparison values are not a complete measurement uncertainty assessment.

## Results reported in the manuscript (not recalculated here)

| Metric | Pressure (bar) | Level (L) | Temperature (°C) |
| --- | ---: | ---: | ---: |
| Paired samples | 116 | 116 | 106 |
| MAE | 0.002696 | 0.002684 | 0.002412 |
| RMSE | 0.003180 | 0.003026 | 0.002851 |
| Bias | -0.000328 | -0.000158 | +0.000258 |
| Maximum absolute difference | 0.008789 | 0.004917 | 0.004971 |

The paper reports Pearson correlation coefficients exceeding 0.997 for the three monitored quantities in the selected trial. It describes 21 experimental trials, while the detailed quantitative metrics above are from one selected trial.

## Limitations and responsible use

1. The original source code, original experimental measurements, calibration coefficients, and time-alignment rules are not supplied here.
2. Actual MCC 128 channel mapping and hardware wiring must be verified; illustrative defaults are not validated experimental settings.
3. The GPIO indicator lamp is not implemented in the reconstructed code.
4. The reconstructed scripts have not been validated on the original Raspberry Pi/MCC 128 installation or against the original ThingSpeak channel.
5. Exact numerical reproduction of Table I and Figs. 7–8 requires the original paired data and processing choices.
6. Do not connect the reconstructed acquisition software to industrial equipment without qualified review of electrical interfaces and safety requirements.

## Contact

For questions about the manuscript and the reference reconstruction, contact Mauricio Aarón Pérez-Romero at **maperezro@ipn.mx**.
