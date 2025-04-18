import sqlite3

import pdu_api_classes


def insert_into_database():
    data = []
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    api_data = pdu_api_classes.get_data(pdu_api_classes.endpoints, pdu_api_classes.endpoints_to_racks, "inlet")

    for i in api_data:
        for j in i:
            for h in j:
                data.append(h)
            cur.execute("INSERT OR REPLACE INTO INLETS_DATA VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",data)
            data.clear()
    con.commit()
    con.close()


##### COMMAND TO SELECT ALL ROWS FROM THE TABLE AND SHOW THE DATA WITHIN
# con = sqlite3.connect("database.db")
# cur = con.cursor()
# response = cur.execute("SELECT * FROM INLETS_DATA")
# print(response.fetchall())

##### COMMAND TO CREATE THE TABLE IN CASE IT WAS DELETED
# con = sqlite3.connect("database.db")
# cur = con.cursor()
# table = '''CREATE TABLE IF NOT EXISTS POWER_PRICES_KWH(
#             "Timestamp_UTC" TEXT PRIMARY KEY NOT NULL,
#             "Timestamp_DK" TEXT NOT NULL,
#             "Price_DKK" REAL NOT NULL
#         );'''
# cur.execute(table)
# con.commit()

##### COMMAND TO DELETE ALL FROM THE TABLE
def table_data_delete(table):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute(f"DELETE FROM {table}")
    con.commit()

##### COMMAND TO DELETE A TABLE
# con = sqlite3.connect("database.db")
# cur = con.cursor()
# cur.execute("DROP TABLE IF EXISTS POWER_PRICES_KWH")
# con.commit()

# table_data_delete("POWER_GRID_CO2_EMISSIONS_PROGNOSIS")
