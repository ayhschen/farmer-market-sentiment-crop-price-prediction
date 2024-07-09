import os
import xlrd
import json


def extract_data(file_path):
    keywords = set(["wheat", "coarse grains", "oilseeds"])

    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_name("WASDE Text")

    wheat, corn, soy = "", "", ""
    curr = None

    for row_idx in range(sheet.nrows):
        row_value = sheet.cell_value(row_idx, 0)
        category = row_value.split(":  ")

        if len(category) > 1 and category[0].lower() in keywords:
            if row_value[0] == "W":
                curr = "w"
            elif row_value[0] == "C":
                curr = "c"
            elif row_value[0] == "O":
                curr = "s"

        if curr == "w":
            wheat += row_value
        elif curr == "c":
            corn += row_value
        elif curr == "s":
            soy += row_value

    return wheat, corn, soy


def extract_month_year_from_filename(filename):
    """Extract month and year from the file name."""
    return os.path.splitext(filename)[0]


# Set the path to the data directory
data_directory = "data/"

# Initialize an empty dictionary to store the extracted wheat data
wheat_data_raw = {}
corn_data_raw = {}
soybean_data_raw = {}

# Loop through all the XLS files in the data directory and extract wheat-related text
for filename in os.listdir(data_directory):
    if filename.endswith(".xls"):
        file_path = os.path.join(data_directory, filename)
        date_key = extract_month_year_from_filename(filename)

        (
            wheat_data_raw[date_key],
            corn_data_raw[date_key],
            soybean_data_raw[date_key],
        ) = extract_data(file_path)

# Create the jsons folder if it doesn't exist
jsons_directory = "jsons/"
if not os.path.exists(jsons_directory):
    os.makedirs(jsons_directory)


subdirectories = ["wheat", "corn", "soy"]
for subdir in subdirectories:
    subdir_path = os.path.join(jsons_directory, subdir)
    if not os.path.exists(subdir_path):
        os.makedirs(subdir_path)

# Export the dictionary to a JSON file
json_wheat = os.path.join(jsons_directory, "wheat", "wheat_data.json")
json_corn = os.path.join(jsons_directory, "corn", "corn_data.json")
json_soy = os.path.join(jsons_directory, "soy", "soy_data.json")

with open(json_wheat, "w") as json_file:
    json.dump(wheat_data_raw, json_file, indent=4)

with open(json_corn, "w") as json_file:
    json.dump(corn_data_raw, json_file, indent=4)

with open(json_soy, "w") as json_file:
    json.dump(soybean_data_raw, json_file, indent=4)
