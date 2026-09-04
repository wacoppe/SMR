# SMR Fuel Requirement Model

Python code associated with the manuscript:

**Small Modular Reactors for Data Centers: Deployment and Nuclear Fuel Requirements**

## Description

This repository contains the Python implementation used to estimate the
fuel-cycle metrics and natural uranium requirements reported in the manuscript.

The calculations include:

- natural uranium feed requirements;
- specific natural uranium requirement (gU/MWh_e);
- initial heavy metal inventory;
- fleet-level annual natural uranium demand (tU/year).

The reactor parameters correspond to the ACP100, BANDI, and RITM-200N
designs evaluated in the study.

## Requirements

Python 3.x

No external Python packages are required.

## Usage

Run:

python FuelandMinedMaterial.py

The reactor input parameters can be modified directly in the script to
evaluate alternative reactor designs or scenarios.

## Authors

Willian Vieira de Abreu et al.

## Citation

If you use this code, please cite the associated manuscript.
