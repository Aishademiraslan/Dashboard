from datetime import datetime
from time import sleep, time_ns

import data_inserter
import CO2_emissions
from div_funcs import api_modular_time
import co2_usage_pr_rack
import power_price

print("PROGRAM STARTED...\n")

stopper = False

def timer():
    global stopper
    end = api_modular_time(9, 5, "future")
    filter = '{"PriceArea":"DK2"}'
    # print(stopper)
    timestamp = datetime.now()
    stopwatch = time_ns()
    minute = int(timestamp.strftime("%M"))
    try:
        if stopper == False and (minute % 5 == 0 or minute == 0):
            # print("yup")
            co2_usage_inserter = co2_usage_pr_rack.Insert()
            stopwatch = time_ns()
            print("INSERTING PDU DATA")
            data_inserter.insert_into_database()
            print("PDU DATA INSERTED")
            print(f"IT TOOK {(time_ns()-stopwatch)/1000000000} SECONDS TO GET AND INSERT PDU DATA INTO THE DATABASE")
            print("INSERTING EMISSIONS DATA")
            CO2_emissions.database_inserter(f'https://api.energidataservice.dk/dataset/CO2Emis?filter={filter}&sort=Minutes5UTC%20DESC&limit=1', "POWER_GRID_CO2_EMISSIONS")
            print("EMISSIONS DATA INSERTED")
            print("INSERTING PROGNOSIS DATA")
            # data_inserter.table_data_delete("POWER_GRID_CO2_EMISSIONS_PROGNOSIS")
            CO2_emissions.database_inserter(f'https://api.energidataservice.dk/dataset/CO2EmisProg?end={end}&filter={filter}&sort=Minutes5UTC%20ASC', "POWER_GRID_CO2_EMISSIONS_PROGNOSIS")
            print("PROGNOSIS DATA INSERTED")
            print("INSERTING CO2 USAGE PR RACK DATA")
            co2_usage_inserter.co2_usage()
            print("CO2 USAGE PR RACK DATA INSERTED")
            print("INSERTING CO2 USAGE PR RACK PROGNOSIS DATA")
            co2_usage_inserter.co2_usage_prognosis()
            print("CO2 USAGE PR RACK DATA INSERTED")
            print("INSERTING POWER PRICE DATA")
            power_price.db_insert()
            print("POWER PRICES DATE INSERTED")
            stopper = True
            print("DONE\n")
            print("WAITING UNTIL NEXT DATA FETCH...\n")
        if minute % 5 != 0:
            sleep(1)
            # print(f"reloading {minute % 2 = }")
            stopper = False
    except Exception as e:
        print(e)

while True:
    timer()
