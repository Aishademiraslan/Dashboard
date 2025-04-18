import sqlite3

import requests

class CO2_api:
    def __init__(self, request):
        self.request = request


    def get_data(self):
        response = requests.get(f"{self.request}")
        return response.json()["records"]


def database_inserter(url, table):
    data = []
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    api_response = CO2_api(url).get_data()
    for i in api_response:
        for j in i.values():
            data.append(j)
        cur.execute(f"INSERT OR REPLACE INTO {table} VALUES(?, ?, ?, ?)",data)
        # print(data)
        data.clear()
    con.commit()
    con.close()

