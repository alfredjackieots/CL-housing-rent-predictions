'''
Helper function to evaluate ridge/lasso models at different random states 
'''

# Necessary imports
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso, LassoCV, Ridge, RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error


def model_eval_with_alphavec(rando_state_list, alphavec, X, y, model_type):
    '''
    Function to evalaute models at different random states for lasso or ridge
    Best alpha is unknown - uses list of alphas (alphavec) to help with cross validation
    
    Inputs:  * list of random states
             * vector of possible alphas to evaluate
             * X - independent variables
             * y - target variable
             * model type: 'ridge' or 'lasso'
             
    Process: * split data into train / test
             * use cross validation to find best alpha
             * train & fit model using best alpha
             * evalaute r^2 values for train/test
             * evaluate root mean squared error (RMSE)

    Output:  * For each random state
                * Best alpha
                * train r^2 
                * test r^2
                * train/test r^2 ratio
                * RMSE
             * Summary
                * list of alphas used
                * mean alpha and standard deviation (std)
                * mean train r^2 and std
                * mean test r^2 and std
                * avg train/test r^ ratio
                * mean RMSE and std   
    '''
    
    train_scores = []
    test_scores = []
    alphas = []
    rmse_list = []
    
    print("Model Type: ", model_type)
    print("Alpha evaluation in progress...\n")    
    
    for r_state in rando_state_list:
        
        # Split data
        X, X_test, y, y_test = train_test_split(X, y, test_size=.3, random_state=r_state)
        
        # Scalilng features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X.values)
        X_test_scaled = scaler.transform(X_test.values)   
            
        
        if model_type == 'lasso':
        
            # Lasso Model Evaluation
            model = LassoCV(alphas = alphavec, cv=3)
            model.fit(X_train_scaled, y)
            
            # Find best alpha 
            best_alpha = model.alpha_
        
            # Fit & train model
            model = Lasso(alpha=best_alpha)
            model.fit(X_train_scaled, y)
            
            # Score model
            train_score = model.score(X_train_scaled, y)
            test_score = model.score(X_test_scaled, y_test)
            
            
        elif model_type == 'ridge':
            
            # Ridge Model evaluation
            model = RidgeCV(alphas = alphavec, cv=3)
            model.fit(X_train_scaled, y)
            
            # Find best alpha 
            best_alpha = model.alpha_
        
            # Fit and train model
            model = Ridge(alpha=best_alpha)
            model.fit(X_train_scaled, y)
            
            # Score model
            train_score = model.score(X_train_scaled, y)
            test_score = model.score(X_test_scaled, y_test)
            
        else:
            print("~~~ No Other Models Supported ~~~")
            break
        
        
        # Add scores & alphas to list
        train_scores.append(train_score)
        test_scores.append(test_score)
        alphas.append(best_alpha)
        
        rmse = mean_squared_error(y_test, model.predict(X_test_scaled), squared=False)
        rmse_list.append(rmse)
        
        # Print out for each random state
        print("Random State: ", r_state)
        print("~~~~~~~~~~~~~~~~~~")
        print("Best Alpha: ", best_alpha)
        print(f'Lasso Regression train R^2: {train_score:.5f}')
        print(f'Lasso Regression test R^2: {test_score:.5f}')
        print("")
        print(f'Train/Val R^2 Ratio: {train_score/test_score: .5f}')
        print("")
        print("RMSE : ", rmse)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
    
    # Summary print out
    print("Evaluation complete.\n")
    print("Summary\n")
    
    # Alphas: 
    print('Alphas: ', alphas)
    print(f'Avg alpha: {np.mean(alphas):.5f} +- {np.std(alphas):.5f}')
    print("")
    
    # Scores: 
    print(f'Mean training r^2: {np.mean(train_scores):.5f} +- {np.std(train_scores):.5f}')
    print(f'Mean test r^2: {np.mean(test_scores):.5f} +- {np.std(test_scores):.5f}')
    print(f'Avg train/test r^2 ratio: {(np.mean(train_scores)/np.mean(test_scores)):.5f}')
    print("")
    print(f'Avg RMSE: {np.mean(rmse_list):.5f} +- {np.std(rmse_list):.5f}')


def model_eval_with_alpha(random_state_list, X, y, model_type, alpha=1):
    '''
    Function to evalaute models at different random states for lasso or ridge with a provided alpha
    
    Inputs:  * list of random states
             * alpha
             * X - independent variables
             * y - target variable
             * model type: 'ridge' or 'lasso'
             
    Process: * split data into train / test
             * train & fit model using given alpha
             * evalaute r^2 values for train/test
             * evaluate root mean squared error (RMSE)

    Output:  * For each random state
                * train r^2 
                * test r^2
                * train/test r^2 ratio
                * RMSE
             * Summary
                * mean train r^2 and std
                * mean test r^2 and std
                * avg train/test r^ ratio
                * mean RMSE and std   
    '''
    
    train_scores = []
    test_scores = []
    alphas = []
    rmse_list = []
    
    print("Model Type: ", model_type)
    print("Alpha evaluation in progress...\n")    
    
    for r_state in random_state_list:
        
        # Data split into train/test
        X, X_test, y, y_test = train_test_split(X, y, test_size=.3, random_state=r_state)
        
        # Scalilng features
        scaler = StandardScaler()

        X_train_scaled = scaler.fit_transform(X.values)
        X_test_scaled = scaler.transform(X_test.values)   
            
        
        if model_type == 'lasso':
            
            # Create & fit model
            model = Lasso(alpha=alpha)
            model.fit(X_train_scaled, y)
            
            # score model
            train_score = model.score(X_train_scaled, y)
            test_score = model.score(X_test_scaled, y_test)
            
            
        elif model_type == 'ridge':
            
            # Create and fit model
            model = Ridge(alpha=alpha)
            model.fit(X_train_scaled, y)
            
            # Score model
            train_score = model.score(X_train_scaled, y)
            test_score = model.score(X_test_scaled, y_test)
            
        else:
            print("~~~ No Other Models Supported ~~~")
            break
        
        
        # Add scores
        train_scores.append(train_score)
        test_scores.append(test_score)
        
        rmse = mean_squared_error(y_test, model.predict(X_test_scaled), squared=False)
        rmse_list.append(rmse)
        
        # Print out for each random state
        print("Random State: ", r_state)
        print("~~~~~~~~~~~~~~~~~~")
        print(f'Lasso Regression train R^2: {train_score:.5f}')
        print(f'Lasso Regression test R^2: {test_score:.5f}')
        print("")
        print(f'Train/Val R^2 Ratio: {train_score/test_score: .5f}')
        print("")
        print("RMSE : ", rmse)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        
    print("Evaluation complete.\n")
    print("Summary\n")
    
    # Summary printout 
    print(f'Mean training r^2: {np.mean(train_scores):.5f} +- {np.std(train_scores):.5f}')
    print(f'Mean test r^2: {np.mean(test_scores):.5f} +- {np.std(test_scores):.5f}')
    print(f'Avg train/test r^2 ratio: {(np.mean(train_scores)/np.mean(test_scores)):.5f}')
    print("")
    print(f'Avg RMSE: {np.mean(rmse_list):.5f} +- {np.std(rmse_list):.5f}')
    