from data_inserter import table_data_delete

list = [
    "INLETS_DATA",
    "POWER_GRID_CO2_EMISSIONS",
    "POWER_GRID_CO2_EMISSIONS_PROGNOSIS",
    "PR_RACK_CO2_EMISSIONS",
    "PR_RACK_CO2_EMISSIONS_PROGNOSIS",
    "POWER_PRICES_KWH"
]

for i in list:
    try:
        print(f"DELETING DATA FROM TABLE: {i}")
        table_data_delete(i)
        print(f"DATA DELETED FROM TABLE : {i}\n")
    except Exception as e:
        print(f"\n#####################\n{e}\n#####################\n")
