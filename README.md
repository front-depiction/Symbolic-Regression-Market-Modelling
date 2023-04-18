# Stock Market Prediction using Symbolic Regression

This repository contains a Python-based application that uses symbolic regression machine learning to model and predict stock market performance. The application leverages a graphical user interface (GUI) to download and process data from the Federal Reserve Bank of St. Louis economic database (FRED) API seamlessly.

# Files

main.py: The main file that has to be run and holds the GUI.
processing.py: Holds all the functions for data processing and model training.
Usage

Run main.py to launch the GUI.

# GUI

The left side of the GUI holds a data unifier that automatically joins the selected market data into one .csv file.
Input start and end dates, and resampling time interval.
Manual code allows you to manually add to the list using a FRED code. On the [FRED website](https://fred.stlouisfed.org/), find an indicator and just add the code.
In the lists, you can double-click items to move them from selected to available indicators.
The right side of the GUI holds the model training parameters.
Number of processes: The number of processes simultaneously analyzing the data with different random seeds.
Other fields include:
1. Population size: Number of individuals in each generation of the genetic algorithm. Larger population size provides more diverse solutions but increases computational time.

2. Generations: Number of iterations the genetic algorithm will run to evolve the solutions. More generations can lead to better results, but also increases computation time.

3. P crossover: Probability of crossover (mating) between two individuals in the population.

4. P subtree mutation: Probability of subtree mutation, where a random subtree within an individual's program is replaced with a new randomly-generated subtree.

5. P hoist mutation: Probability of hoist mutation, where a random subtree within an individual's program is replaced by one of its own randomly-chosen subtrees.

6. P point mutation: Probability of point mutation, where a random node within an individual's program is replaced with a new randomly-generated node.

7. Max samples: Maximum number of samples to use when fitting the symbolic regression model.

8. Tournament size: Number of individuals randomly selected from the population to compete in the selection process based on their fitness scores.

 9. Parsimony coefficients: Coefficient to control the trade-off between model complexity and fit. Higher values encourage simpler models.

 10. T offset: Number of time units to offset the prediction.

 11. T offset unit: Unit of time for the offset (e.g., weeks, months, or quarters).

 12. Start and end training dates: Date range for training the symbolic regression model.

 13. Set the output parameters for the graph (timeframe): Time range for displaying the graph with the actual market data and the predictions      from the model.

# Dependencies

To run the application, you need the following packages installed:

pandas
fredapi
gplearn
sklearn
matplotlib
tkinter

You can install them using pip:

```pip install pandas fredapi gplearn scikit-learn matplotlib```
