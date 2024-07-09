import pandas as pd
from arch import arch_model

import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.api import VAR


def analyze_volatility(volatility_data, sentiment_data):
    # Load the dataset

    # print(volatility_data.head())

    # VAR model requires the time series to be stationary. Depending on your data, you might need to transform it (e.g., taking first differences)
    # data_diff = data.diff().dropna()

    # Prepare the exogenous variables (sentiment scores)
    exog_data = sentiment_data[['Sentiment_Supply', 'Sentiment_Demand']]

    # Prepare the endogenous variable (volatility)
    endog_data = volatility_data[['Volatility']]

    # Create the VARX model
    model = VAR(endog=endog_data, exog=exog_data)

    # Fit the model
    # You can adjust maxlags and information criteria (ic) as per your data
    results = model.fit(maxlags=5, ic='aic')

    # Print summary of the model
    print(results.summary())

    # Predictions (Optional)
    # predictions = results.forecast(y=endog_data.values[-results.k_ar:], steps=5, exog_future=exog_future_data)
    # print(predictions)
