# ml-web-project
 This projects deploys ML model on a website.

This project has a future house price prediction model running at the server to calculate the prices of house.

I am using 3 different models and putting them togther to calculate the prices.This is in order to make the predicitions robust.
Trained models are large and cannot be uploaded to github. 

I have the code I used to train the models uploaded in the system.

Using Django to handle back-end routing. Bootstrap for giving styling to html pages.
XGBoost and Linear_reg algorithm to create the model.

Optuna for hyperparameter optimization. Used SuccesiveHalving to prune the optimization for a quicker optimization.