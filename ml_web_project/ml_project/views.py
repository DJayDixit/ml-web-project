from django.shortcuts import render
# from apps import MlProjectConfig

import pickle
import pandas as pd

class HousePrice():

    def load_model(self, core_cpi_file, year_gni_file, price_file):
        # C:\Users\jaydi\Documents\GitHub\ml-web-project\ml_web_project\ml_project\core_cpi_predict.pickle
        core_cpi_pickle = open(core_cpi_file, "rb")
        year_gni_pickle = open(year_gni_file, "rb")
        price_pickle = open(price_file, "rb")

        core_cpi_model = pickle.load(core_cpi_pickle)
        year_gni_model = pickle.load(year_gni_pickle)
        price_model = pickle.load(price_pickle)

        return price_model, core_cpi_model, year_gni_model

    def calculate(self, date_month, flat_type_number, house_area_sqm, core_cpi_file, year_gni_file, price_file):

        date = {"date": [date_month]}
        date = pd.DataFrame(date)
        date.reset_index(drop=True, inplace=True)

        models = self.load_model(core_cpi_file, year_gni_file, price_file)
        core_cpi_predict = models[1]
        year_gni_predict = models[2]
        price_predict = models[0]

        core_cpi = core_cpi_predict.predict(date)
        year_gni = year_gni_predict.predict(date)

        flat_type = flat_type_number
        area_sqm = house_area_sqm
        size = flat_type + area_sqm
        affordability = size*(core_cpi+year_gni)

        validate = {
                "affordability": affordability, "Core CPI": core_cpi, "year_gni":year_gni, 
                "area_sqm":[area_sqm], "date":[date.iloc[0]["date"]], "flat_type": [flat_type]
                    }
        validate_df = pd.DataFrame(validate)

        pred = price_predict.predict(validate_df)

        return pred

if __name__ == "__main__":
    price = HousePrice()

    core_cpi_file = r"C:\Users\jaydi\Documents\GitHub\ml-web-project\ml_web_project\ml_project\core_cpi_predict.pickle"
    year_gni_file = r"C:\Users\jaydi\Documents\GitHub\ml-web-project\ml_web_project\ml_project\year_gni_predict.pickle"
    price_file = r"C:\Users\jaydi\Documents\GitHub\ml-web-project\ml_web_project\ml_project\price_predict.pickle" 
    calc = price.calculate(2022.06, 2, 65, core_cpi_file, year_gni_file, price_file)
    print(calc)