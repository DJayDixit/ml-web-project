# House Future Price Predict


## To run this project

1. You have Python 3.7 or above. Preffered Python 3.9
2. You have atleast Django version 4.0.3
3. You have Pandas and XG_Boost installed.
4. Contact the creator if you want the models to run this project.

## Some Details about the project

This projects deploys ML model on a website.

This project has a future house price prediction model running at the server side to calculate the prices of house.

I am using 3 different models and putting them togther to calculate the prices.This is in order to make the predicitions robust.

Unfortunately models are large and cannot be uploaded to github. Althoug I have uploaded the code I used to train the models in ml_project/ create_models.py.

I cannot upload the data I am using to trian the model due to the copyright issues and their size. You can get the data from https://www.kaggle.com/datasets/denzilg/hdb-flat-prices-19902021-march. I am using ALL Prices 1990-2021 mar.csv dataset to train the models.

I am using Django to handle back-end routing. Bootstrap and css for styling the html pages.

XGBoost and Linear_reg algorithm to create the model.
Optuna for hyperparameter optimization. I have used SuccesiveHalving to prune the optimization for a quicker optimization. 

I am using mysql to store the user information and calculations from the model.
It usually takes about 40 seconds to get the model to calculate and return a value. I am storing the information calculted in a database so we can fetch the same calculation next time a user requests it.