import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Function to get AUM and update time for a given ETF
def get_aum_and_time(sym):
    url = f"https://www.hkex.com.hk/Market-Data/Securities-Prices/Exchange-Traded-Products/Exchange-Traded-Products-Quote?sym={sym}&sc_lang=en"
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    aum_element = soup.find('dt', {'class': 'ico_data col_aum'})
    aum_value = aum_element.text.strip() if aum_element else "N/A"

    time_element = soup.find('dt', {'class': 'ico_data col_aum_date'})
    update_time = time_element.text.strip() if time_element else "N/A"

    return aum_value, update_time

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Get AUMs and update times for the three ETFs
aum_9008, time_9008 = get_aum_and_time("9008")
aum_9042, time_9042 = get_aum_and_time("9042")
aum_9439, time_9439 = get_aum_and_time("9439")

# Close the browser
driver.quit()

# Use the first ETF's update time as the current date
current_date = time_9008.replace('as at ', '').strip()

# Define the path to the CSV file
csv_file = 'data/aum_data.csv'  # Use the correct directory

# Load or create the DataFrame
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=['Date', 'AUM_9008', 'AUM_9042', 'AUM_9439'])

# Add new data only if the current date isn't already recorded
if current_date not in df['Date'].values:
    new_data = pd.DataFrame({
        'Date': [current_date],
        'AUM_9008': [aum_9008],
        'AUM_9042': [aum_9042],
        'AUM_9439': [aum_9439]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(csv_file, index=False)
    print("AUM data updated successfully.")
else:
    print("AUM data for today is already recorded.")
