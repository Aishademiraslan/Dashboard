import sqlite3
import datetime

import data_inserter
import data_reader
import div_funcs

racks = {
    "27" : 1,
    "28" : 2,
    "29" : 3,
    "30" : 4,
    "31" : 5,
    "32" : 6,
    "33" : 7
}

def power_draw_pr_rack(racks):
    pdu_data = data_reader.read('*', 'INLETS_DATA')
    pr_rack_power_data = {}
    for i in pdu_data:
        timestamp = i[2][:16]
        rack = f"Rack {racks[i[0][8:10]]}"
        if rack not in pr_rack_power_data:
            pr_rack_power_data.update({rack: {}})
        if timestamp not in pr_rack_power_data[rack]:
            pr_rack_power_data[rack].update({timestamp: 0})
        pr_rack_power_data[rack][timestamp] += int(i[7])
    return pr_rack_power_data

class CO2_usage:
    def __init__(self):
        self.racks_power_draw = power_draw_pr_rack(racks)
        self.co2_data = data_reader.read('*', 'POWER_GRID_CO2_EMISSIONS')
        self.co2_prognosis_data = data_reader.read('*', 'POWER_GRID_CO2_EMISSIONS_PROGNOSIS')

    def co2_usage_pr_rack(self):
        pr_rack_co2_emissions_data = []
        for i in self.co2_data[1:]:
            co2 = i[3]
            time = div_funcs.time_reformat(i[1])
            for rack,data in self.racks_power_draw.items():
                for timestamp,power in data.items():
                    if timestamp == time:
                        pdu_co2 = round(power/1000 * co2, 2)
                        pr_rack_co2_emissions_data.append([rack, timestamp, pdu_co2])
        return pr_rack_co2_emissions_data


    def co2_usage_pr_rack_prognosis(self):
        pr_rack_co2_emissions_data_prediction = []
        avgs = []
        for rack, data in self.racks_power_draw.items():
            cumulative = []
            for timestamp, power in data.items():
                cumulative.append(power)
            avg = sum(cumulative)/len(cumulative)
            avgs.append([rack, avg])
        for i in self.co2_prognosis_data:
            rack_predictions = []
            for rack in avgs:
                co2 = i[3]
                co2_consumption = round(rack[1]/1000*co2, 2)
                time = div_funcs.time_reformat(i[1])
                rack_predictions.append([rack[0], time, co2_consumption])
            pr_rack_co2_emissions_data_prediction.append(rack_predictions)
        return pr_rack_co2_emissions_data_prediction
            

class Insert:
    def __init__(self):
        pass

    def co2_usage(self):
        try:
            data_inserter.table_data_delete("PR_RACK_CO2_EMISSIONS")
            CO2 = CO2_usage()
            data = []
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            co2_data = CO2.co2_usage_pr_rack()
            for i in co2_data:
                for j in i:
                    data.append(j)
                # print(data)
                cur.execute(f"INSERT OR REPLACE INTO PR_RACK_CO2_EMISSIONS VALUES(?, ?, ?)",data)
                # print(data)
                data.clear()
            con.commit()
            con.close()
        except Exception as e:
            print(f"\n#####################\n{e}\n#####################\n")
        
    def co2_usage_prognosis(self):
        try:
            data_inserter.table_data_delete("PR_RACK_CO2_EMISSIONS_PROGNOSIS")
            CO2 = CO2_usage()
            data = []
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            co2_data = CO2.co2_usage_pr_rack_prognosis()
            for i in co2_data:
                for j in i:
                    for k in j:
                        data.append(k)
                    # print(data)
                    cur.execute(f"INSERT OR REPLACE INTO PR_RACK_CO2_EMISSIONS_PROGNOSIS VALUES(?, ?, ?)",data)
                    # print(data)
                    data.clear()
            con.commit()
            con.close()
        except Exception as e:
            print(f"\n#####################\n{e}\n#####################\n")

# co2_usage_inserter = Insert()

# co2_usage_inserter.co2_usage()
# co2_usage_inserter.co2_usage_prognosis()
# x = CO2_usage()
# print(x.co2_usage_pr_rack_prognosis())
