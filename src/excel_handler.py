import pandas as pd
from datetime import datetime

class ExcelHandler:
    def __init__(self):
        self.all_data_file = 'data/all_data_commodities.xlsx'
        self.hourly_data_pattern = 'data/commodities_{}.xlsx'

    def save_all_data(self, data):
        try:
            # Read existing data or create new DataFrame
            try:
                df = pd.read_excel(self.all_data_file)
            except FileNotFoundError:
                df = pd.DataFrame()

            # Append new data
            new_df = pd.DataFrame([data])
            df = pd.concat([df, new_df], ignore_index=True)

            df.to_excel(self.all_data_file, index=False)
        except Exception as e:
            print(f"Error saving all data: {str(e)}")

    def save_hourly_data(self, data):
        try:
            current_time = datetime.now()
            filename = self.hourly_data_pattern.format(
                current_time.strftime('%Y%m%d%H')
            )

            df = pd.DataFrame([data])
            df.to_excel(filename, index=False)
        except Exception as e:
            print(f"Error saving hourly data: {str(e)}")