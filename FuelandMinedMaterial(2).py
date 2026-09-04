import math

# =========================
# Dados do Reator
# =========================

ihmm_tHM = 16.44
burnup_mwd_per_kgHM = 13.9
enrichment = 2.99

tails_assay = 0.25
feed_assay = 0.711
efficiency = 32
conv_losses = 0.5

# Custos unitários
unit_costs = {
    "swu": 145,     # $/SWU Fonte: não foi preciso, está tudo na minha cabeça. Brinks. Mean - Meta-Analysis of Advanced Nuclear Reactor Cost Estimations Idaho (2024, p.91)
    "feed": 65,    # $/lb U3O8
    "conv": 60,    # $/kgU
    "fab": 1310,    # $/kgHM
}


# =========================
# Funções
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


def compute_fuel_reload_cost(unit_costs, swu, natural_feed_kgU, uf6_feed_kgU, product_mass_kgHM):
    costs = {}

    costs["SWU cost"] = swu * unit_costs["swu"]

    # feed em $/lb U3O8 convertido para $/kgU
    costs["U3O8 feed cost"] = natural_feed_kgU * (
        unit_costs["feed"] * 2.2046 / 0.847981
    )

    costs["Conversion cost"] = uf6_feed_kgU * unit_costs["conv"]
    costs["Fabrication cost"] = product_mass_kgHM * unit_costs["fab"]

    costs["Total reload cost"] = sum(costs.values())

    return costs


# =========================
# Cálculos
# =========================

product_mass_kgHM = ihmm_tHM * 1000

feed_factor = get_feed_factor(enrichment, tails_assay, feed_assay)
swu_factor = get_swu_factor(enrichment, tails_assay, feed_assay, feed_factor)

uf6_feed_kgU, natural_feed_kgU = compute_feed_from_product(
    feed_factor,
    product_mass_kgHM,
    conv_losses
)

swu_total = compute_swu(swu_factor, product_mass_kgHM)

energy_mwd_th, energy_mwh_th = compute_energy_from_burnup(
    product_mass_kgHM,
    burnup_mwd_per_kgHM
)

energy_mwh_e = energy_mwh_th * efficiency / 100

required_natural_uranium_gU_per_MWh = natural_feed_kgU * 1000 / energy_mwh_e
spent_fuel_gHM_per_MWh = product_mass_kgHM * 1000 / energy_mwh_e

fuel_reload_costs = compute_fuel_reload_cost(
    unit_costs,
    swu_total,
    natural_feed_kgU,
    uf6_feed_kgU,
    product_mass_kgHM
)

fuel_reload_cost_per_MWh = fuel_reload_costs["Total reload cost"] / energy_mwh_e


# =========================
# Resultados
# =========================

print("===== BANDI Fuel Cycle Estimate =====")
print(f"IHMM: {ihmm_tHM:.2f} tHM")
print(f"Burnup: {burnup_mwd_per_kgHM:.2f} MWd/kgHM")
print(f"Enrichment: {enrichment:.2f} %")
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

print(f"Required natural uranium: {required_natural_uranium_gU_per_MWh:.3f} gU/MWh_e")
print(f"Spent fuel: {spent_fuel_gHM_per_MWh:.3f} gHM/MWh_e")
print()

print("===== Fuel Reload Cost =====")
for item, value in fuel_reload_costs.items():
    print(f"{item}: US$ {value:,.2f}")

print()
print(f"Fuel reload cost: US$ {fuel_reload_cost_per_MWh:.2f}/MWh_e")
print(f"Fuel reload cost: US$ {fuel_reload_cost_per_MWh / 10:.4f} cents/kWh_e")