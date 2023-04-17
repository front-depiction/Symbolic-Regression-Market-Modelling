#processing.py

import pandas as pd
from fredapi import Fred
import os
from gplearn.genetic import SymbolicRegressor
from sklearn.metrics import mean_absolute_error
import pandas as pd
import matplotlib.pyplot as plt
import concurrent.futures
from multiprocessing import cpu_count
from sklearn.metrics import mean_absolute_error
from gplearn.genetic import SymbolicRegressor
import random

def resample_fred_data(api_key, series_ids, start_date, end_date, time_interval, output_path):
    fred = Fred(api_key=api_key)
    t_frame = time_interval.upper()

    # Validate the time interval
    if t_frame not in ['W', 'M', 'Q']:
        raise ValueError("Invalid time interval. Allowed values are 'W', 'M', or 'Q'.")

    # Create an empty DataFrame to store the resampled data
    df_resampled = pd.DataFrame()

    # Loop through each FRED series ID and resample the data to the specified time unit
    for series_id in series_ids:
        try:
            df = pd.DataFrame(fred.get_series(series_id, start_date, end_date))
        except ValueError as e:
            print(f"Error for {series_id}: {e}")
            continue

        df.index.name = "DATE"
        df.columns = [series_id]
        # Convert any non-numeric values to NaN, and then forward-fill the NaN values
        df = pd.to_numeric(df.iloc[:, 0], errors='coerce').ffill()
        df_resampled[series_id] = df.resample(t_frame).mean()

    # Write the resampled data to a CSV file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_resampled = df_resampled.fillna(method='ffill')
    df_resampled.to_csv(output_path)

    print("All files were included in the final resampled data.")



def train_model(population_size, generations, p_crossover, p_subtree_mutation, p_hoist_mutation, p_point_mutation, max_samples, tournament_size, parsimony_coefficient, t_offset, t_frame, start_training, end_training, start_graphing, end_graphing, market_data_path, resampled_data_path, output_path, n_processes=cpu_count()):

    # Read the stock market data
    market_df = pd.read_csv(market_data_path, parse_dates=['DATE'])
    market_df = market_df[['DATE', 'NASDAQCOM']]
    market_df = market_df.set_index('DATE')

    market_df['NASDAQCOM'] = pd.to_numeric(market_df['NASDAQCOM'], errors='coerce')
    market_df = market_df.fillna(method='ffill')

    market_df = market_df.resample(t_frame).last()

    df_resampled = pd.read_csv(resampled_data_path, parse_dates=['DATE'])
    df_resampled = df_resampled.set_index('DATE')
    df_resampled = df_resampled.resample(t_frame).last()

    df_resampled = df_resampled.fillna(method='ffill')
    df_resampled = df_resampled.shift(t_offset, freq=t_frame)

    data = pd.concat([market_df, df_resampled], axis=1).dropna()

    end_graphing_timestamp = pd.to_datetime(end_graphing)
    if t_frame == 'W':
        offset = pd.DateOffset(weeks=t_offset)
    elif t_frame == 'M':
        offset = pd.DateOffset(months=t_offset)
    elif t_frame == 'Q':
        offset = pd.DateOffset(months=t_offset * 3)
    end_graphing_timestamp = end_graphing_timestamp + offset
    end_graphing_shifted = end_graphing_timestamp.strftime('%Y-%m-%d')

    X = data[df_resampled.columns]
    y = data['NASDAQCOM']

    X_train = X.loc[start_training:end_training]
    y_train = y.loc[start_training:end_training]

    X_test = X.loc[start_graphing:end_graphing_shifted]
    y_test = y.loc[start_graphing:end_graphing_shifted]

    with concurrent.futures.ProcessPoolExecutor(max_workers=n_processes) as executor:
        seeds_list = [random.randint(1, 2**32-1) for _ in range(n_processes)]
        args = args = [(seed, X_train, y_train, X_test, y_test, X, population_size, generations, p_crossover, p_subtree_mutation, p_hoist_mutation, p_point_mutation, max_samples, tournament_size, parsimony_coefficient, t_offset, t_frame, start_graphing, end_graphing) for seed in seeds_list]
        results = list(executor.map(actual_training, args))
        
    best_result = max(results, key=lambda x: x[1])
    best_formula, score, mae, predictions_filtered, best_seed = best_result

    print(f"Best formula: {best_formula}")
    print(f"Score: {score}")
    print(f"Mean absolute error: {mae}")
    print(f"Best random seed: {best_seed}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as file:
        file.write(f"Best formula: {best_formula}\n")
        file.write(f"Score: {score}\n")
        file.write(f"Mean absolute error: {mae}\n")

    
    plt.figure(figsize=(10, 6))
    plt.plot(market_df[start_graphing:end_graphing], label='NASDAQCOM', color='blue')
    plt.plot(predictions_filtered[start_graphing:end_graphing_shifted], label='SymbolicRegressor Predictions', color='red')
    plt.title('Market Data vs SymbolicRegressor Predictions')
    plt.xlabel('Year')
    plt.ylabel('Price')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()

def actual_training(args):
    random_seed, X_train, y_train, X_test, y_test, X, population_size, generations, p_crossover, p_subtree_mutation, p_hoist_mutation, p_point_mutation, max_samples, tournament_size, parsimony_coefficient, t_offset, t_frame, start_graphing, end_graphing = args
    
    est_gp = SymbolicRegressor(
        population_size=population_size,
        function_set=('add', 'sub', 'mul', 'div', 'log', 'sqrt', 'sin', 'cos', 'tan', 'abs', 'neg', 'inv'),
        generations=generations,
        stopping_criteria=0.01,
        p_crossover=p_crossover,
        p_subtree_mutation=p_subtree_mutation,
        p_hoist_mutation=p_hoist_mutation,
        p_point_mutation=p_point_mutation,
        max_samples=max_samples,
        tournament_size=tournament_size,
        parsimony_coefficient=parsimony_coefficient,
        verbose=1,
        n_jobs=1,
        random_state=random_seed
    )
    
    est_gp.fit(X_train, y_train)

    y_pred = est_gp.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean absolute error: {mae}")

    score = est_gp.score(X_test, y_test)
    print(f"Score: {score}")

    y_pred_all = est_gp.predict(X)
    predictions_all = pd.DataFrame({'Predicted': y_pred_all}, index=X.index)
    
    predictions_filtered = predictions_all.loc[start_graphing:]

    best_formula = est_gp._program
    
    return best_formula, score, mae, predictions_filtered, random_seed