import requests
import sqlite3

import div_funcs

additional_charges= {
    "Grøn El" : 0.08,
    "Omk. til myndighedsbehandling" : 0.0004,
    "Systemtarif" : 0.051,
    "Transmissions nettarif" : 0.074,
    "Elafgift" : 0.761,
    "Nettarrif C" : 0.3417
}

def additional_charge(additional_charges):
    cumulative = []
    for i in additional_charges.values():
        cumulative.append(i)
    additional_charge = sum(cumulative)
    return additional_charge

def api_data():
    filter = '{"PriceArea":"DK2"}'
    response = requests.get(f"https://api.energidataservice.dk/dataset/Elspotprices?start=now&filter={filter}&sort=HourUTC").json()["records"]
    return response

def power_price():
    data_to_db = []
    for data in api_data():
        kWh_spot_price = 0
        kWh_price = 0
        reformattet_data = []
        for key, value in data.items():
            if key == 'HourUTC' or key == 'HourDK':
                timestamp = div_funcs.time_reformat(value)
                # print(timestamp)
                reformattet_data.append(timestamp)
            elif key == "SpotPriceDKK":
                kWh_spot_price = value/1000
                # print(f"Uden: {kWh_spot_price}")
                kWh_price = kWh_spot_price+additional_charge(additional_charges)
                # print(f"Med: {kWh_price}\n")
                reformattet_data.append(kWh_price)
        data_to_db.append(reformattet_data)
    return data_to_db

def db_insert():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    power_price_data = power_price()

    for data in power_price_data:
        # print(data)
        cur.execute("INSERT OR REPLACE INTO POWER_PRICES_KWH VALUES(?,?,?)",data)
    con.commit()
    con.close()
