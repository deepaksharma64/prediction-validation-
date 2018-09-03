I have used Python 3 for this work.
Libraries I have used are: pandas, numpy and sys.



Problem Statement - (https://github.com/InsightDataScience/prediction-validation/)

Introduction -
You are a data engineer working at a financial institution that analyzes real-time stock market data. To determine the best trading strategy, the company's data scientists created a machine learning model to predict the future price of a stock every hour, and they want to test it on real-time stock data.
Before deploying the model, they want you to help test how accurate their predictions are over time by comparing their predictions with newly arriving real-time stock prices.

Challenge summary -
You will read two different files, one provides the actual value of each stock every hour and the second lists the predicted value of various stocks at a certain hour during the same time period.
You will obtain the average error by calculating the average difference between the actual stock prices and predicted values over a specified sliding time window.

