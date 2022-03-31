import pickle
import pandas as pd

def load_model():
    core_cpi_pickle = open("ml_web_project\ml_project\core_cpi_predict.pickle", "rb")
    year_gni_pickle = open("ml_web_project\ml_project\year_gni_predict.pickle", "rb")
    price_pickle = open("ml_web_project\ml_project\price_predict.pickle", "rb")

    core_cpi_model = pickle.load(core_cpi_pickle)
    year_gni_model = pickle.load(year_gni_pickle)
    price_model = pickle.load(price_pickle)

    return price_model, core_cpi_model, year_gni_model

def calculate(date_month, flat_type_number, house_area_sqm):

    date = {"date": [date_month]}
    date = pd.DataFrame(date)
    date.reset_index(drop=True, inplace=True)

    models = load_model()
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


dummy = calculate(2022.05, 2, 64)
print(dummy)