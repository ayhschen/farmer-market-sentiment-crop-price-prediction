import matplotlib.pyplot as plt
import numpy as np
import json
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import datetime
import re
from volatility import VolatilityExtractor

# Load .env file
load_dotenv()

# Retrieve the API key from the environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def sort_json_by_date(json_data):
    # Helper function to convert month-year string to a datetime object
    def get_date_from_string(date_str):
        return datetime.datetime.strptime(date_str, '%B_%Y')

    # Sort the json data by keys converted to dates
    sorted_keys = sorted(json_data, key=get_date_from_string)
    return {key: json_data[key] for key in sorted_keys}


def analyze_usda_report(api_key, commodity):
    os.environ["OPENAI_API_KEY"] = api_key
    data_path = f"./jsons/{commodity}/{commodity}_data.json"

    template = """
        Using the provided USDA report, categorize the information into four lists: Supply Qualitative, Supply Quantitative, Demand Qualitative, and Demand Quantitative. Each sentence should be classified based on its content.
        Always have the four lists in the same order. Always have the 4 lists for Supply Qualitative, Supply Quantitative, Demand Qualitative, and Demand Quantitative. Do not drop a list even if there is no data. 
        If no information exists, the list should have the sentence \"Metric Score is 0\". For example, if Demand Qualitative has no information, the list should have the sentence \"Metric score is 0\".

        For qualitative sentences, label them as positive, negative, or neutral, corresponding to a score of 0.5, -0.5, and 0, respectively.

        For quantitative sentences, label them (bad, slightly bad, neutral, slightly good, good) according to the examples below on the score (-1, -0.5, 0, 0.5, 1).

        For example the following sentences should have these Metric Scores:

        "Quantitative: Wheat: Feed and residual use in Russia is 21.0 million tons, increased 1.0 million tons.” (1)

        "Quantitative: Wheat: Global consumption is 791.0 million tons, increased 2.4 million tons.” (0.5)

        "Qualitative: Wheat: Supply outlook is stable, due to unchanged U.S. wheat outlook.” (0)

        "Quantitative: Wheat: Ending stocks are 862 million bushels, decreased 15 million bushels.” (-0.5)

        “Quantitative: Wheat: Global exports are 41 million tons, decreased 2.5 million tons” (-1)

        Give me only the lists and the sentences in the following format: 
        Qualitative: [Commodity]: [Qualitative Aspect] is [Trend/Outlook], due to [Cause/Factor], Metric score is [Numeric value of metric score].
        Quantitative: [Commodity]: [Metric] is [Value] [Unit], [Change Direction] [Change Amount] [Unit], Metric score is [Numeric value of metric score].
        Please provide the lists and sentences in the above formats based on the report content. The report is {value}.
    """

    # Corrected PromptTemplate initialization
    prompt = PromptTemplate(
        template=template, input_variables=["value"])

    # Load the wheat data
    with open(data_path, "r") as f:
        wheat_data = json.load(f)

    # Usage in your existing code
    sorted_data = sort_json_by_date(wheat_data)
    monthly_score = {}

    for curr_month in sorted_data:
        # Recreate the LLM chain for each iteration
        llm = OpenAI(openai_api_key=api_key)
        llm_chain = LLMChain(prompt=prompt, llm=llm)

        report_sentences = llm_chain.run(value=wheat_data[curr_month])
        print(report_sentences)
        print("--------------")
        # Assume report_sentences is a list of sentences with their respective labels
        score = extract_metric_scores(report_sentences)
        if score:
            monthly_score[curr_month] = score

    wheat_vol_extraction = VolatilityExtractor(commodity)
    wheat_vol = wheat_vol_extraction.get_volatility()

    for key, value in monthly_score.items():
        monthly_score[key] = [wheat_vol[key][0], value[0], value[1], wheat_vol[key][1]]

    # Write to a json file organized by month
    with open(f"./jsons/{commodity}/{commodity}_data_analysis.json", "w") as f:
        json.dump(monthly_score, f)

def extract_metric_scores(text):
    """
    Extracts and categorizes metric scores for supply and demand from the given text.
    Adjusted to handle case variations of 'metric score'.

    Args:
    text (str): A string containing supply and demand information with metric scores.

    Returns:
    dict: A dictionary with two keys 'supply' and 'demand', each containing a list of corresponding scores.
    """
   
    delims = {"Supply Qualitative", "Supply Quantitative", "Demand Qualitative", "Demand Quantitative"}
    split = '|'.join(map(re.escape, delims))
    split_text = [s.replace("\n", "").strip() for s in re.split(split, text)]
    split_text = [s for s in split_text if s]

    if len(split_text) != 4:
        return None

     # Adjusted regex pattern to match "metric score" in case-insensitive manner
    pattern = r'metric score is ([\-0-9.]+)\.'

    # Extracting all the metric scores with adjusted pattern
    score_matrix = []
    for curr_text in split_text:
        score_matrix.append([float(value) for value in re.findall(pattern, curr_text, re.IGNORECASE)])
    
    average = lambda lst: sum(lst) / len(lst) if lst else 0
    for i in range(4):
        score_matrix[i] = average(score_matrix[i])
    
    supply = average(score_matrix[:2])
    demand = average(score_matrix[2:])

    # Output list
    return [supply, demand]

def main(commodity):
    analyze_usda_report(OPENAI_API_KEY, commodity)

    with open(f"./jsons/{commodity}/{commodity}_data_analysis.json", "r") as f:
        data = json.load(f)

    # Extracting months and corresponding values
    months = list(data.keys())
    supply = [value[0] for value in data.values()]
    demand = [value[1] for value in data.values()]

    # Plotting the data
    plt.figure(figsize=(15, 6))
    plt.plot(months, supply, label='Supply')
    plt.plot(months, demand, label='Demand')

    # Formatting the plot
    plt.xticks(rotation=90)  # Rotate x-axis labels for readability
    plt.xlabel('Months')
    plt.ylabel('Values')
    plt.title('Monthly Values Comparison')
    plt.legend()
    plt.tight_layout()  # Adjusts the plot to ensure everything fits without overlapping

    # Show the plot
    plt.show()


# Running the main function
# text = "Supply Qualitative: \
# Wheat: Supply outlook is stable, due to unchanged U.S. wheat outlook, Metric Score is 0. \n\
# Supply Quantitative: \
# Wheat: Beginning stocks are 1.85 million tons, increased 0.07 million tons, Metric Score is 0.5. \n\
# Demand Qualitative: \
# Wheat: Global consumption is projected down 24.6 million tons year to year, Metric Score is -0.5. \n\
# Demand Quantitative: \
# Wheat: Feed and residual use in Russia is 21.0 million tons, increased 1.0 million tons, Metric Score is 1. \
# Wheat: Global exports are 41 million tons, decreased 2.5 million tons, Metric Score is -1. \
# Wheat: Ending stocks are 862 million bushels, decreased 15 million bushels, Metric Score is -0.5."

# To Run:
# Call main(commodity) function on a commodity (wheat, corn, soy) and it should create a pandas dataframe of [month num, supply, demand, volatility] - all monthly
commodity = "wheat"
main(commodity)