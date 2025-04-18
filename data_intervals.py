import time
import datetime 

import data_reader
import pandas as pd


class Power:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.rack_power_avg = self.rack_power()
    
    def rack_power(self, interval='h', all=False):
        '''
        Returns a dataframe for pr rack avg power usage pr defined interval type

        Parameters
        ----------
        interval : str
            Interval type:
                Accepts:
                    h: Hourly
                    d: Daily
                    W: Weekly
                    ME: Monthly
                    SME: Semi-monthly (15th-14th)
                    QE: Quarterly
                    YE: Yearly
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        if all == True:
            from_db = data_reader.read('Rack, Timestamp, VA', 'INLETS_DATA', WHERE=f'Timestamp <= "{self.end} 00:00"')
        else:
            from_db = data_reader.read('Rack, Timestamp, VA', 'INLETS_DATA', WHERE=f'Timestamp >= "{self.start} 00:00" and Timestamp <= "{self.end} 23:55"')

        df1 = pd.DataFrame(from_db, columns=['Rack', 'Datetime', 'VA (Wh)'])
        df1['Datetime'] = pd.to_datetime(df1['Datetime'])
        df1.set_index(['Datetime'], inplace=True)

        df1_grouped = df1.groupby(['Rack', 'Datetime']).sum()
        df1_grouped = df1_grouped.reset_index().set_index('Datetime')

        rack_power = df1_grouped.groupby('Rack').resample(interval).mean().drop('Rack', axis=1)
        rack_power = rack_power['VA (Wh)'].round(2)
        return rack_power

    def rack_power_sum(self, interval):
        '''
        Returns a dataframe for pr rack power usage pr defined interval type

        Parameters
        ----------
        interval : str
            Interval type
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        self.rack_power_avg = self.rack_power_avg.reset_index().set_index('Datetime')
        rack_power_sum = self.rack_power_avg.groupby('Rack').resample(interval).sum().drop('Rack', axis=1)
        rack_power_sum = rack_power_sum['VA (Wh)'].fillna(0).round(2)
        return rack_power_sum

    def lab_prod_power(self, interval='d', all=False):
        '''
        Returns a dataframe for pr group power usage pr defined interval type

        Parameters
        ----------
        interval : str
            Interval type
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        if all == True:
            rack_power_avg_all = self.rack_power(all=True)
            rack_power_avg_all = rack_power_avg_all.reset_index().set_index('Datetime')
            rack_power_avg_all['Rack_Group'] = rack_power_avg_all['Rack'].apply(lambda x: 'Production' if x == 1 else 'Laboratory')
            grouped_power = rack_power_avg_all.groupby('Rack_Group').resample(interval).sum().drop(['Rack_Group', 'Rack'], axis=1)
        else:
            self.rack_power_avg = self.rack_power_avg.reset_index().set_index('Datetime')
            self.rack_power_avg['Rack_Group'] = self.rack_power_avg['Rack'].apply(lambda x: 'Production' if x == 1 else 'Laboratory')
            grouped_power = self.rack_power_avg.groupby('Rack_Group').resample(interval).sum().drop(['Rack_Group', 'Rack'], axis=1)
        grouped_power = grouped_power['VA (Wh)'].round(2)
        grouped_power = grouped_power.replace(0.0, pd.NA)
        return grouped_power

    def combined_power(self, interval='d'):
        '''
        Returns a dataframe for overall power usage pr defined interval type

        Parameters
        ----------
        interval : str
            Interval type
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        self.rack_power_avg = self.rack_power_avg.reset_index().set_index('Datetime')
        combined_power = self.rack_power_avg.resample(interval).sum().drop('Rack', axis=1)
        combined_power = combined_power['VA (Wh)'].fillna(0).round(2)
        return combined_power


class Emissions:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.rack_emissions_avg = self.rack_emissions()
    
    def rack_emissions(self, interval='h', all=False):
        '''
        Returns a dataframe for pr rack avg CO2 emissions pr defined interval

        Parameters
        ----------
        interval : str
            Interval type:
                Accepts:
                    h: Hourly
                    d: Daily
                    W: Weekly
                    ME: Monthly
                    SME: Semi-monthly (15th-14th)
                    QE: Quarterly
                    YE: Yearly
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        if all == True:
            from_db = data_reader.read('Rack, Timestamp, CO2_emissions', 'PR_RACK_CO2_EMISSIONS_PROGNOSIS', WHERE=f'Timestamp >= "{self.start} 00:00" and Timestamp <= "{self.end} 23:55"')
        else:
            from_db = data_reader.read('Rack, Timestamp, CO2_emissions', 'PR_RACK_CO2_EMISSIONS', WHERE=f'Timestamp >= "{self.start} 00:00" and Timestamp <= "{self.end} 23:55"')
        reformattet_db_data = []
        for i in from_db:
            i = list(i)
            i[0] = int(i[0][5:])
            reformattet_db_data.append(i)

        df1 = pd.DataFrame(reformattet_db_data, columns=['Rack', 'Datetime', 'CO2 Grams'])
        df1['Datetime'] = pd.to_datetime(df1['Datetime'])
        df1.set_index(['Datetime'], inplace=True)

        df1_grouped = df1.groupby(['Rack', 'Datetime']).sum()
        df1_grouped = df1_grouped.reset_index().set_index('Datetime')
        
        racks_emissions = df1_grouped.groupby('Rack').resample(interval).mean().drop('Rack', axis=1)
        racks_emissions = racks_emissions['CO2 Grams'].round(2)
        return racks_emissions

    def rack_emissions_sum(self, interval='d'):
        '''
        Returns a dataframe for pr rack CO2 emissions pr defined interval type

        Parameters
        ----------
        interval : str
            Interval type
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        self.rack_emissions_avg = self.rack_emissions_avg.reset_index().set_index('Datetime')
        rack_emissions_sum = self.rack_emissions_avg.groupby('Rack').resample(interval).sum().drop('Rack', axis=1)
        rack_emissions_sum = rack_emissions_sum['CO2 Grams'].fillna(0).round(2)
        return rack_emissions_sum

    def lab_prod_emissions(self, interval='d', all=False):
        '''
        Returns a dataframe for pr group CO2 emissions pr defined interval type

        Parameters
        ----------
        interval : str
            Interval type
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        if all == True:
            rack_emissions_avg_all = self.rack_emissions(all=True)
            rack_emissions_avg_all = rack_emissions_avg_all.reset_index().set_index('Datetime')
            rack_emissions_avg_all['Rack_Group'] = rack_emissions_avg_all['Rack'].apply(lambda x: 'Production' if x == 1 else 'Laboratory')
            grouped_emissions = rack_emissions_avg_all.groupby('Rack_Group').resample(interval).sum().drop(['Rack_Group', 'Rack'], axis=1)
        else:
            self.rack_emissions_avg = self.rack_emissions_avg.reset_index().set_index('Datetime')
            self.rack_emissions_avg['Rack_Group'] = self.rack_emissions_avg['Rack'].apply(lambda x: 'Production' if x == 1 else 'Laboratory')
            grouped_emissions = self.rack_emissions_avg.groupby('Rack_Group').resample(interval).sum().drop(['Rack_Group', 'Rack'], axis=1)
        grouped_emissions = grouped_emissions['CO2 Grams'].round(2)
        grouped_emissions = grouped_emissions.replace(0.0, pd.NA)
        return grouped_emissions

    def combined_emissions(self, interval='d'):
        '''
        Returns a dataframe for overall CO2 emissions pr defined interval type

        Parameters
        ----------
        interval : str
            Interval type
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        self.rack_emissions_avg = self.rack_emissions_avg.reset_index().set_index('Datetime')
        combined_emissions = self.rack_emissions_avg.resample(interval).sum().drop('Rack', axis=1)
        combined_emissions = combined_emissions['CO2 Grams'].fillna(0).round(2)
        return combined_emissions


class Power_Costs:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.rack_power_avg = Power(start, end).rack_power()
        self.rack_avg_costs = self.rack_power_cost_avg()
        

    def rack_power_cost_avg(self, interval='h', all=False):
        '''
        Returns a dataframe for pr rack avg cost to run pr defined interval type

        Parameters
        ----------
        interval : str
            Interval type:
                Accepts:
                    h: Hourly
                    d: Daily
                    W: Weekly
                    ME: Monthly
                    SME: Semi-monthly (15th-14th)
                    QE: Quarterly
                    YE: Yearly
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        if all == True:
            rack_power_avg_all = Power(self.start, self.end).rack_power(all=True)
            rack_power_avg_all = rack_power_avg_all.reset_index().set_index('Datetime')
            db_power_prices = data_reader.read('Timestamp_DK, Price_DKK', 'POWER_PRICES_KWH')
        else:
            self.rack_power_avg = self.rack_power_avg.reset_index().set_index('Datetime')
            db_power_prices = data_reader.read('Timestamp_DK, Price_DKK', 'POWER_PRICES_KWH', WHERE=f'Timestamp_DK >= "{self.start} 00:00" and timestamp_DK <= "{self.end} 23:55"')
        
        power_prices = pd.DataFrame(db_power_prices, columns=['Datetime', 'Price'])
        power_prices['Datetime'] = pd.to_datetime(power_prices['Datetime'])
        power_prices.set_index('Datetime', inplace=True)

        if all == True:
            merged_frames = pd.merge(rack_power_avg_all,power_prices, how='inner', left_index=True, right_index=True)
        else:
            merged_frames = pd.merge(self.rack_power_avg,power_prices, how='inner', left_index=True, right_index=True)
        racks_power_costs = merged_frames
        racks_power_costs['Power Costs DKK'] = racks_power_costs.apply(lambda row: (row['VA (Wh)']/1000) * row.Price, axis=1)
        racks_power_costs = racks_power_costs.groupby('Rack').resample(interval).mean().drop(['VA (Wh)', 'Price', 'Rack'], axis=1)
        racks_power_costs = racks_power_costs['Power Costs DKK'].round(2)
        return racks_power_costs

    def rack_power_costs_sum(self, interval='d'):
        '''
        Returns a dataframe for pr rack cost to run pr defined interval type

        Parameters
        ----------
        interval : str
            Interval type
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        self.rack_avg_costs = self.rack_avg_costs.reset_index().set_index('Datetime')
        rack_power_costs_sum = self.rack_avg_costs.groupby('Rack').resample(interval).sum().drop('Rack', axis=1)
        rack_power_costs_sum = rack_power_costs_sum['Power Costs DKK'].fillna(0).round(2)
        return rack_power_costs_sum

    def lab_prod_power_costs(self, interval='d', all=False):
        '''
        Returns a dataframe for pr rack group cost to run pr defined interval type

        Parameters
        ----------
        interval : str
            Interval type
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        if all == True:
            rack_avg_costs_all = self.rack_power_cost_avg(all=True)
            rack_avg_costs_all = rack_avg_costs_all.reset_index().set_index('Datetime')
            rack_avg_costs_all['Rack_Group'] = rack_avg_costs_all['Rack'].apply(lambda x: 'Production' if x == 1 else 'Laboratory')
            # print(rack_avg_costs_all)
            grouped_costs = rack_avg_costs_all.groupby('Rack_Group').resample(interval).sum().drop(['Rack_Group', 'Rack'], axis=1)
        else:
            self.rack_avg_costs = self.rack_avg_costs.reset_index().set_index('Datetime')
            self.rack_avg_costs['Rack_Group'] = self.rack_avg_costs['Rack'].apply(lambda x: 'Production' if x == 1 else 'Laboratory')
            # print(f"{self.rack_avg_costs = }")
            grouped_costs = self.rack_avg_costs.groupby('Rack_Group').resample(interval).sum().drop(['Rack_Group', 'Rack'], axis=1)
        grouped_costs = grouped_costs['Power Costs DKK'].round(2)
        grouped_costs = grouped_costs.replace(0.0, pd.NA)
        # print(f"{grouped_costs = }")
        return grouped_costs

    def combined_power_costs(self, interval='d'):
        '''
        Returns a dataframe for overall cost to run pr defined interval type

        Parameters
        ----------
        interval : str
            Interval type
        
        Returns
        -------
        rack_power : DataFrame
            Pandas dataframe
        '''
        self.rack_avg_costs = self.rack_avg_costs.reset_index().set_index('Datetime')
        combined_costs = self.rack_avg_costs.resample(interval).sum().drop('Rack', axis=1)
        combined_costs = combined_costs['Power Costs DKK'].fillna(0).round(2)
        return combined_costs



##### Use the below code if you want to see the dataframes' data in the shell before using for whatever you want to use it for.
##### It should cover all the data.
##### If you want to see ALL the data in the dataframe just use .to_string() after the method you're visualising

# while True:
#     try:
#         print("\n(1) POWER USAGE\n(2) CO2 EMISSIONS\n(3) POWER COSTS")
#         data_type_choice = int(input("CHOOSE WHICH DATA TYPE TO SHOW\n> "))
#         print("\n(1) PR RACK AVG\n(2) PR RACK SUM\n(3) PR GROUP SUM\n(4) OVERALL SUM")
#         collection_choice = int(input("CHOOSE DATA STRUCTURE\n> "))
#         if collection_choice != 1:
#             print("\n(h) HOURLY\n(d) DAILY\n(W) WEEKLY\n(ME) MONTHLY\n(SME) SEMI-MONTHLY\n(QE) QUARTERLY\n(YE) YEARLY")
#             interval_choice = input("CHOOSE TIME INTERVAL\n> ")
#         start = time.time()
#         if data_type_choice == 1:
#             pw = Power()
#             if collection_choice == 1:
#                 print(pw.rack_power())
#             elif collection_choice == 2:
#                 print(pw.rack_power_sum(interval_choice))
#             elif collection_choice == 3:
#                 print(pw.lab_prod_power(interval_choice))
#             elif collection_choice == 4:
#                 print(pw.combined_power(interval_choice))
#         elif data_type_choice == 2:
#             em = Emissions('2024-11-01 00:00', '2025-01-31 23:55')
#             if collection_choice == 1:
#                 print(em.rack_emissions())
#             elif collection_choice == 2:
#                 print(em.rack_emissions_sum(interval_choice))
#             elif collection_choice == 3:
#                 print(em.lab_prod_emissions(interval_choice))
#             elif collection_choice == 4:
#                 print(em.combined_emissions(interval_choice))
#         elif data_type_choice == 3:
#             pc = Power_Costs()
#             if collection_choice == 1:
#                 print(pc.rack_power_cost_avg())
#             elif collection_choice == 2:
#                 print(pc.rack_power_costs_sum(interval_choice))
#             elif collection_choice == 3:
#                 print(pc.lab_prod_power_costs(interval_choice))
#             elif collection_choice == 4:
#                 print(pc.combined_power_costs(interval_choice))
#         print(f"DET TOG {time.time() - start} SEKUNDER AT GENNEMFØRE")
#     except Exception as e:
#         print(f"\n####################\n{e}\n####################\n")
