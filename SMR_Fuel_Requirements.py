# =============================================================================
# SMR Fuel Requirements
# =============================================================================
#
# Reactor Neutronic and Computational Analysis Laboratory (LANCER)
# Nuclear Engineering Program
# COPPE - Federal University of Rio de Janeiro (UFRJ)
#
# Description:
# Python implementation for estimating fuel-cycle metrics and natural uranium
# requirements for Small Modular Reactor (SMR) deployment scenarios.
#
# The code evaluates the ACP100, BANDI, and RITM-200N reactor designs and
# calculates reactor deployment requirements, initial heavy metal inventory,
# specific natural uranium requirements, and annual fleet-level uranium demand.
#
# Associated manuscript:
# "Small Modular Reactors for Data Centers: Deployment and Nuclear Fuel
# Requirements"
#
# Authors:
# Willian Vieira de Abreu et al.
#
# Repository:
# https://github.com/wacoppe/SMR
#
# =============================================================================


import math

# =========================
# Reactor data
# =========================

reactors = {
    "ACP100": {
        "ihmm_tHM": 16.44,
        "burnup_mwd_per_kgHM": 13.9,
        "enrichment": 2.99,
        "efficiency": 32,
        "electric_power_MWe": 125,
    },
    "BANDI": {
        "ihmm_tHM": 11.89,
        "burnup_mwd_per_kgHM": 29.4,
        "enrichment": 4.95,
        "efficiency": 30,
        "electric_power_MWe": 60,
    },
    "RITM-200N": {
        "ihmm_tHM": 2.88,
        "burnup_mwd_per_kgHM": 96.4,
        "enrichment": 19.75,
        "efficiency": 31,
        "electric_power_MWe": 55,
    },
}

# Common fuel-cycle parameters
tails_assay = 0.25
feed_assay = 0.711
conv_losses = 0.5

# Reference data-center demand
demand_MWe = 2525


# =========================
# Functions
# =========================

def vx(x_percent):
    x = x_percent / 100.0
    return (1.0 - 2.0 * x) * math.log((1.0 - x) / x)


def get_feed_factor(enrich, tails, feed):
    return (enrich - tails) / (feed - tails)


def get_swu_factor(enrich, tails, feed, feed_factor):
    v_tails = vx(tails)
    return vx(enrich) - v_tails - feed_factor * (vx(feed) - v_tails)


def compute_feed_from_product(feed_factor, product_mass_kgHM, conv_losses):
    conv_factor = (100.0 - conv_losses) / 100.0
    uf6_feed_kgU = feed_factor * product_mass_kgHM
    natural_feed_kgU = uf6_feed_kgU / conv_factor
    return uf6_feed_kgU, natural_feed_kgU


def compute_swu(swu_factor, product_mass_kgHM):
    return swu_factor * product_mass_kgHM


def compute_energy_from_burnup(product_mass_kgHM, burnup_mwd_per_kgHM):
    energy_mwd_th = product_mass_kgHM * burnup_mwd_per_kgHM
    energy_mwh_th = energy_mwd_th * 24
    return energy_mwd_th, energy_mwh_th


# =========================
# Calculations
# =========================

for reactor_name, data in reactors.items():

    ihmm_tHM = data["ihmm_tHM"]
    burnup_mwd_per_kgHM = data["burnup_mwd_per_kgHM"]
    enrichment = data["enrichment"]
    efficiency = data["efficiency"]
    electric_power_MWe = data["electric_power_MWe"]

    product_mass_kgHM = ihmm_tHM * 1000

    feed_factor = get_feed_factor(
        enrichment,
        tails_assay,
        feed_assay
    )

    swu_factor = get_swu_factor(
        enrichment,
        tails_assay,
        feed_assay,
        feed_factor
    )

    uf6_feed_kgU, natural_feed_kgU = compute_feed_from_product(
        feed_factor,
        product_mass_kgHM,
        conv_losses
    )

    swu_total = compute_swu(
        swu_factor,
        product_mass_kgHM
    )

    energy_mwd_th, energy_mwh_th = compute_energy_from_burnup(
        product_mass_kgHM,
        burnup_mwd_per_kgHM
    )

    energy_mwh_e = energy_mwh_th * efficiency / 100

    specific_natural_uranium_gU_per_MWh = (
        natural_feed_kgU * 1000 / energy_mwh_e
    )

    spent_fuel_gHM_per_MWh = (
        product_mass_kgHM * 1000 / energy_mwh_e
    )

    # Number of reactor units required
    units = math.ceil(demand_MWe / electric_power_MWe)

    # Installed fleet capacity
    fleet_capacity_MWe = units * electric_power_MWe

    # Total initial heavy-metal inventory
    fleet_IHMM_tHM = units * ihmm_tHM

    # Annual natural uranium demand
    fleet_annual_natural_uranium_tU = (
        specific_natural_uranium_gU_per_MWh
        * fleet_capacity_MWe
        * 8760
        / 1_000_000
    )

    # =========================
    # Results
    # =========================

    print("=" * 55)
    print(f"{reactor_name} Fuel Cycle Estimate")
    print("=" * 55)

    print(f"IHMM: {ihmm_tHM:.2f} tHM")
    print(f"Burnup: {burnup_mwd_per_kgHM:.2f} MWd/kgHM")
    print(f"Enrichment: {enrichment:.2f} %")
    print(f"Thermal efficiency: {efficiency:.1f} %")
    print(f"Electric power: {electric_power_MWe:.0f} MWe")
    print()

    print(f"Feed factor F/P: {feed_factor:.4f}")
    print(f"SWU factor: {swu_factor:.4f} SWU/kgHM")
    print()

    print(f"Product mass: {product_mass_kgHM:,.2f} kgHM")
    print(f"UF6 feed required: {uf6_feed_kgU:,.2f} kgU")
    print(f"Natural uranium required: {natural_feed_kgU:,.2f} kgU")
    print(f"Total SWU required: {swu_total:,.2f} SWU")
    print()

    print(f"Thermal energy: {energy_mwd_th:,.2f} MWd_th")
    print(f"Thermal energy: {energy_mwh_th:,.2f} MWh_th")
    print(f"Electric energy: {energy_mwh_e:,.2f} MWh_e")
    print()

    print(
        f"Specific natural uranium requirement: "
        f"{specific_natural_uranium_gU_per_MWh:.3f} gU/MWh_e"
    )

    print(
        f"Spent fuel: "
        f"{spent_fuel_gHM_per_MWh:.3f} gHM/MWh_e"
    )

    print()
    print(f"Reference demand: {demand_MWe:.0f} MWe")
    print(f"Required reactor units: {units}")
    print(f"Fleet capacity: {fleet_capacity_MWe:.0f} MWe")
    print(f"Fleet IHMM: {fleet_IHMM_tHM:.2f} tHM")

    print(
        f"Fleet annual natural uranium demand: "
        f"{fleet_annual_natural_uranium_tU:.2f} tU/year"
    )

    print()
