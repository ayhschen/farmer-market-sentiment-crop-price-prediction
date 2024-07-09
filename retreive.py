import os
import requests
from datetime import datetime, timedelta

# Function to get the last day of the month
def last_day_of_month(date):
    next_month = date.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

# Endpoint base URL
base_url = "https://usda.library.cornell.edu/api/v1/release/findAll?acronym=waob"

# Authentication token
auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE0NzcxfQ.7EjisQmD3qtTfHpS53G3vbdlDwGEPD2r2DvIvdTBylA"
headers = {
    "Authorization": f"Bearer {auth_token}"  # Assuming Bearer token authentication
}

# Start and end dates
start_date = datetime(2013, 1, 1)
end_date = datetime(2023, 1, 1)

# Loop through the time frame month by month
current_date = start_date
while current_date < end_date:
    # Get the first and last day of the month
    month_start = current_date.strftime('%Y-%m-%d')
    month_end = last_day_of_month(current_date).strftime('%Y-%m-%d')
    
    # Make the request for the current month
    response = requests.get(f"{base_url}&start_date={month_start}&end_date={month_end}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        for item in data:
            if "World Agricultural Supply and Demand Estimates" in item['title']:
                xml_link = next((link for link in item['files'] if link.endswith('.xls')), None)
                if xml_link:
                    xml_content = requests.get(xml_link).content
                    file_name = f"{current_date.strftime('%B_%Y')}.xls"
                    with open(os.path.join('data', file_name), 'wb') as file:
                        file.write(xml_content)
                    break
    
    # Increment to the next month
    current_date = current_date + timedelta(days=last_day_of_month(current_date).day)

