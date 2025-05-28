from time import time as take_time

from raritan import rpc
from raritan.rpc import pdumodel
from datetime import datetime

endpoints = ["192.168.27.2", "192.168.28.2", "192.168.28.3", "192.168.29.2", "192.168.30.2", "192.168.30.3", "192.168.31.2", "192.168.31.3", "192.168.32.2", "192.168.33.2"]
endpoints_to_racks = {
    "192.168.27.2" : 1,
    "192.168.28.2" : 2,
    "192.168.28.3" : 2,
    "192.168.29.2" : 3,
    "192.168.30.2" : 4,
    "192.168.30.3" : 4,
    "192.168.31.2" : 5,
    "192.168.31.3" : 5,
    "192.168.32.2" : 6,
    "192.168.33.2" : 7
}



class PX2_2493_api:
    def __init__(self, agent, pdu, endpoint, rack, point_to):
        self.agent = agent
        self.pdu = pdu
        self.endpoint = endpoint
        self.rack = rack
        self.point_to = point_to
    

    def measuring_iterator(self):
        if self.point_to == "inlet":
            data_points = self.pdu.getInlets()
        elif self.point_to == "outlets":
            data_points = self.pdu.getOutlets()
        bulk_helper = rpc.BulkRequestHelper(self.agent)
        data = []
        for i in data_points:
            bulk_helper.add_request(i.getSensors)
        responses = bulk_helper.perform_bulk(raise_subreq_failure=False)
        bulk_helper.clear()
        for response in responses:
            data.append(self.get_data(response))
        return data


    def get_data(self, response):
        try:
            starter = take_time()
            sensors = response
            voltage = round(sensors.voltage.getReading().value, 3)
            current = round(sensors.current.getReading().value, 3)
            apparent_power = round(sensors.apparentPower.getReading().value, 3)
            active_power = round(sensors.activePower.getReading().value, 3)
            active_energy = round(sensors.activeEnergy.getReading().value, 1)
            power_factor = sensors.powerFactor.getReading().value
            line_frequency = sensors.lineFrequency.getReading().value
            date_and_time = timestamp()
            date = date_and_time[:10]
            time = date_and_time[11:]
            print(f"PDU KALD OG DATA TID: {take_time() - starter}")
            return[self.endpoint, self.rack, date_and_time, date, time, current, voltage, apparent_power, active_power, active_energy, power_factor, line_frequency]       
        except Exception as e:
            print(e)



def timestamp(modifier="default"):
    now = datetime.now()
    if modifier == "default":
        return(now.strftime("%Y-%m-%d %H:%M"))
    else:
        return(now.strftime(modifier))




def get_data(endpoints, endpoints_to_racks, choice):
    data = []
    for endpoint in endpoints:
        agent = rpc.Agent("http", endpoint, "x", "x", disable_certificate_verification=True) # Username and password redacted for security reasons
        pdu = rpc.pdumodel.Pdu("/model/pdu/0", agent)
        api = PX2_2493_api(agent, pdu, endpoint, endpoints_to_racks[endpoint], choice)
        endpoint_data = api.measuring_iterator()
        data.append(endpoint_data)
    return data

