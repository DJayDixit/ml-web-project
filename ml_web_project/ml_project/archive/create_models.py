#imports

# imports important scientific libraries
import numpy as np
import pandas as pd 

# imports preProcessing library
from sklearn.preprocessing import OneHotEncoder

# imports libraries to divide data set into equal and random split
from sklearn.model_selection import KFold

# imports machine learning model and bayesian-hyperparameter optimizer
from xgboost import XGBRegressor
# import optuna

# import mse to evaluate the ml model
from sklearn.metrics import mean_squared_error

# imports libraries for saving the model
import joblib
import pickle

print("Section: 1")
df = pd.read_csv("ml_web_project\ml_project\\archive\ALL Prices 1990-2021 mar.csv")

df["month"] = [int(month.replace(str(year)+"-", ""))*0.01 for year, month in zip(df["year"], df["month"])]
df["date"] = df["year"]+df["month"]
df.drop(["year", "month"], axis=1, inplace=True)

useless = list({col for col in df.columns if "resale_price" not in col and ("lease" in col or "price" in col)})
useless.append("block")
useless.append("address")
useless.append("storey_range")
useless.append("street_name")
useless.append("town")
df.drop(useless, axis=1, inplace=True)

cleanup_nums = {"flat_type": {"1 ROOM":0, "2 ROOM":1, "3 ROOM":2, "4 ROOM":3, "5 ROOM": 4, 
                              "MULTI GENERATION": 5, "EXECUTIVE": 7 
                             }
               }
df = df.replace(cleanup_nums)
df["flat_type"].head(5)

size = df["flat_type"]+df["area_sqm"]
df["affordability"] = (size*(df["Core CPI"]+df["year_gni"]))

df_final = df

print("Section: 2")
row = 0
for i in df_final["affordability"]==np.inf:
    if i:
        df_final.drop(row, inplace=True)

    row += 1

print("Section: 3")
splits = 5  
df_final["kfold"]=-1
folds = KFold(n_splits=splits, shuffle=True, random_state=42)

for kfolds, (train_index, test_index) in enumerate(folds.split(df_final)):
    df_final.loc[test_index, "kfold"] = kfolds

useful_features = ["affordability", "Core CPI", "year_gni", "area_sqm", "date", "flat_type"]

core_cpi_df = df_final[["Core CPI", "date", "kfold"]]

print("Section: 4")
from sklearn.linear_model import LinearRegression

core_cpi_predict = LinearRegression()

i = 7

x_train = core_cpi_df[core_cpi_df["kfold"] != i][["date"]]
y_train = core_cpi_df[core_cpi_df["kfold"] != i]["Core CPI"]

core_cpi_predict.fit(x_train, y_train)

year_gni_df = df_final[["year_gni", "date", "kfold"]]

# we are using optuna for hyperparameter optimization
# study = optuna.create_study(study_name="optimization",
#     sampler=optuna.samplers.TPESampler(seed=42),
#     pruner=optuna.pruners.SuccessiveHalvingPruner()
# )

# I am training my machine learning model on kaggle 
# After 9 hours of continous usage kaggle tends to turn off the kernel 
# instead of losing our progress I am saving our hyperparameter optimizer in every run 
# so that we continue from where we left off

# study = joblib.load("study.pkl")

# function for hyperparameter optimization
# def objective(trial, folds=5):

#     final_scores=0
    
#     params = {
#         "eta": trial.suggest_float("eta", 1e-5, 1e-1, log=True),
#         "n_estimators": trial.suggest_int("n_estimators", 1000, 10000, step=300),
#         "max_depth": trial.suggest_int("max_depth", 3, 10),
#         "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-1, log=True),
#         "gamma": trial.suggest_float("gamma", 0, 7, step=0.1),
#         "min_child_weight": trial.suggest_int("min_child_weight", 0, 10),
#         "subsample": trial.suggest_float("subsample", 0.2, 1.0),
#         "colsample_bytree": trial.suggest_float("colsample_bytree", 0.1, 1.0),
#         "colsample_bylevel": trial.suggest_float("colsample_bylevel", 0.1, 1.0,),
#         "colsample_bynode": trial.suggest_float("colsample_bynode", 0.1, 1.0),
#         "alpha": trial.suggest_float("alpha", 1e-6, 100.),
#         "lambda": trial.suggest_float("lambda", 1e-6, 100.),
#     }
    
#     model = XGBRegressor(**params, n_jobs=-1, random_state=42, tree_method="gpu_hist", 
#                          gpu_id=0, predictor="gpu_predictor")
    
#     for i in range(folds):
#         x_train = df_final[df_final["kfold"] != i][useful_features]
#         y_train = df_final[df_final["kfold"] != i]["resale_price"]

#         x_valid = df_final[df_final["kfold"] == i][useful_features]
#         y_valid = df_final[df_final["kfold"] == i]["resale_price"]

#         model.fit(x_train, y_train)
#         pred = model.predict(x_valid)
#         score = mean_squared_error(y_valid, pred)

#         final_scores += np.sqrt(score)
#         trial.report(score, i)
        
#         joblib.dump(study, "study.pkl")
#         # Handle pruning based on the intermediate value.
#         if trial.should_prune():
#             raise optuna.exceptions.TrialPruned()
    
#     return final_scores/folds

# study.optimize(objective, n_trials=5, show_progress_bar=True)

best_params = {'eta': 0.00032735038807241054, 'n_estimators': 8500, 'max_depth': 10, 'learning_rate': 0.02141464809595559, 'gamma': 0.7000000000000001, 'min_child_weight': 1, 'subsample': 0.42767550815007427, 'colsample_bytree': 0.9565024010441561, 'colsample_bylevel': 0.8388279926154787, 'colsample_bynode': 0.9682364524289278, 'alpha': 71.15978635340159, 'lambda': 14.623745762860942}

print("Section: 5")
year_gni_predict = XGBRegressor(**best_params, n_jobs=-1, random_state=42, tree_method="hist", 
                         gpu_id=0, predictor="cpu_predictor")


x_train = year_gni_df[year_gni_df["kfold"] != i][["date"]]
y_train = year_gni_df[year_gni_df["kfold"] != i]["year_gni"]

year_gni_predict.fit(x_train, y_train)

best_params = {'eta': 0.00032735038807241054, 'n_estimators': 8500, 'max_depth': 10, 'learning_rate': 0.02141464809595559, 'gamma': 0.7000000000000001, 'min_child_weight': 1, 'subsample': 0.42767550815007427, 'colsample_bytree': 0.9565024010441561, 'colsample_bylevel': 0.8388279926154787, 'colsample_bynode': 0.9682364524289278, 'alpha': 71.15978635340159, 'lambda': 14.623745762860942}

print("Section: 6")
price_predict = XGBRegressor(**best_params, n_jobs=-1, random_state=42, tree_method="hist", 
                         gpu_id=0, predictor="cpu_predictor")

price_predict.fit(df_final[useful_features], df_final["resale_price"])

print("Section: 7")
filename1 = "price_predict.pickle"
filename2 = "core_cpi_predict.pickle"
filename3 = "year_gni_predict.pickle"

pickle.dump(price_predict, open(filename1, 'wb'))
pickle.dump(core_cpi_predict, open(filename2, 'wb'))
pickle.dump(year_gni_predict, open(filename3, 'wb'))