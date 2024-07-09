# Proposal: Using Farmers’ Outlooks On Commodity Market To Predict Crop Prices

## Authors
Arnav Patidar, Rohit Prasanna, Ronak Agarwal, Shyam Sai Bethina, Alex Yu-Hsin Chen, Sidharth Subbarao, Harold Huang

## Introduction
The agriculture sector is crucial for global food production, impacting everyone significantly. Factors like supply and demand affect commodity prices such as corn, soy, wheat, and rice, leading to price volatility. This project aims to predict crop supply and prices using Natural Language Processing (NLP) and Machine Learning (ML) on qualitative data from USDA WASDE monthly reports.

## Objectives
- **Predict Price of Crop Commodity Futures:** Evaluate and select appropriate NLP and ML models for predicting crop supply and prices using techniques like regression, time series analysis, and sentiment analysis.
- **Dataset Creation:** Label the dataset of official commodity reports from USDA.
- **Text Mining and Sentiment Analysis:** Implement NLP techniques to extract valuable insights from online sources.
- **Model Training and Validation:** Train and validate selected ML models using historical data to ensure accurate predictions of crop supply and prices.
- **Forecasting:** Develop models that can forecast crop supply for different time horizons and predict future crop prices based on supply predictions.

## Data
There are numerous data sources that can be used to collect the outlooks that the farming community across the United States have related to their own yields and the commodity market as a whole. In addition, we will use USDA’s WASDE monthly reports, which provides annual forecasts of supply, demand, and prices of wheat, rice, coarse grains, oilseeds, and cotton. 

- **USDA WASDE Reports:** [USDA WASDE Reports](https://www.usda.gov/oce/commodity/wasde)
- **Planting Reports:** [NASS Reports by Date](https://www.nass.usda.gov/Publications/Calendar/reports_by_date.php), [NASS Publications](https://www.nass.usda.gov/Publications/)

### Potential Future Datasets
- **Reddit API:** Focus on subreddits such as [r/farming](https://www.reddit.com/r/farming/), [Reddit API](https://www.reddit.com/dev/api/)
- **FarmChat:** [FarmChat](https://www.farmchat.com/)
- **CommodityAPI:** [CommodityAPI](https://commodities-api.com/)
- **Drought Monitor:** [Drought Monitor](https://droughtmonitor.unl.edu/)
- **NOAA Climate Prediction Center:** [NOAA Climate Prediction Center](https://www.cpc.ncep.noaa.gov/)
- **Agriville:** [Agriville](https://www.agriville.com/)
- **AgWeb’s Crop Comments:** [AgWeb’s Crop Comments](https://www.agweb.com/crop-comments)
- **Other Agricultural Online Discussion Forums:** [Talk New AgTalk](https://talk.newagtalk.com/category-view.asp), [The Combine Forum](https://www.thecombineforum.com/)

## Methodology
### Natural Language Preprocessing 
- **Data Collection:** Aggregate data from USDA reports over a set timeframe and consider implementing external features including current climate, weather patterns/intensity, etc.
- **Descriptive Analytics:** Use unsupervised learning techniques for sentiment analysis on USDA reports to detect tone and overall outlook.
- **Data Cleaning:** Remove noise, standardize text format, and ensure data consistency.
- **Tokenization and Grouping (Lemmatization):** Break down and standardize textual data for efficient processing, excluding common words to focus on relevant terms.
- **Post NLP Goal:** Have an overall summary of outlook based on sentiment derived from model for each crop and its prices.

### Machine Learning
- **Feature Extraction:** Implement TF-IDF (Term Frequency - Inverse Document Frequency) to convert textual data into a numerical format for ML models.
- **Data Preparation:** Using the features derived from the NLP analysis, prepare datasets for model training.
- **Model Selection:** Choose appropriate models for sentiment analysis and time series forecasting, such as Random Forest and LSTM.
- **Training and Validation/Evaluation:** Train the model on the dataset and evaluate performance using metrics like MAE (Mean Absolute Error) or RMSE (Root Mean Squared Error).

## Final Output/Outcomes
- Creation of an NLP-centered tool/feature to gain analytical insights into the trends between the commodity market, price changes, and other factors from sources such as agricultural reports.
- Identification of potential limitations and biases in data from farmer forums and social media.

## Limitations
- **Overview:** Potential limitations in predicting prices of corn, soy, wheat, etc., using sentiment in forums. Commodity prices are determined by both supply and demand. Factors like politics, war, and other geopolitical events cause volatility, which our model currently does not account for.
- **Sentiment Ambiguity:** Challenges in accurately capturing sentiment, especially when dealing with nuances.
- **Data Bias:** Collected outlooks may not holistically represent the current state of the agriculture sector since it is provided by a single source, the USDA.
- **Model Limitations:** Price predictions are as accurate as the data and the robustness of the model.

## Literature Review
- [A machine learning-based price state prediction model for agricultural commodities using external factors](https://link.springer.com/article/10.1007/s10203-018-0223-8)
- [Machine learning approach for forecasting crop yield based on climatic parameters](https://ieeexplore.ieee.org/document/8475672)
- [Semantics Analysis of Agricultural Experts’ Opinions for Crop Productivity through Machine Learning](https://www.tandfonline.com/doi/full/10.1080/10485252.2020.1851928)
- [Predicting State-Level Agricultural Sentiment with Tweets from Farming Communities](https://www.researchgate.net/publication/332820090_Predicting_State-Level_Agricultural_Sentiment_with_Tweets_from_Farming_Communities)
- [Using USDA Forecasts to Estimate the Price Flexibility of Demand for Agricultural Commodities](https://onlinelibrary.wiley.com/doi/epdf/10.1093/ajae/aas122)

## Timeline
### Phase 1: Initiation and Data Collection
- Define team roles, finalize research methodology, and set up tools.
- Collect appropriate data from USDA reports and other relevant sources.
- Conduct data cleaning and organize all the collected data.

### Phase 2: Data Preprocessing and Initial Analysis
- Conduct natural language preprocessing, sentiment analysis, and data tokenization.
- Label dataset of messages, posts, and reports.
- Extract features using TF-IDF and prepare datasets for model training.
- Begin model selection, training, and validation.
- Compile initial insights and results from the analysis.

### Phase 3: Final Analysis, Report, and Presentation
- Finalize machine learning models and conduct additional testing and fine-tuning.
- Develop a basic NLP-centered analytical tool based on the findings.
- Consider further improvements and potential next steps.
```
