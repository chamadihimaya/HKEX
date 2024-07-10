#!/usr/bin/env python
# coding: utf-8

# In[2]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time


# In[3]:


# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for automation
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


# In[4]:


# Function to get AUM and update time for a given ETF
def get_aum_and_time(sym):
    url = f"https://www.hkex.com.hk/Market-Data/Securities-Prices/Exchange-Traded-Products/Exchange-Traded-Products-Quote?sym={sym}&sc_lang=en"
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract AUM
    aum_element = soup.find('dt', {'class': 'ico_data col_aum'})
    aum_value = aum_element.text.strip() if aum_element else "N/A"
    
    # Extract update time
    time_element = soup.find('dt', {'class': 'ico_data col_aum_date'})
    update_time = time_element.text.strip() if time_element else "N/A"
    
    return aum_value, update_time


# In[5]:


# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)


# In[6]:


# Get AUMs and update times for the three ETFs
aum_9008, time_9008 = get_aum_and_time("9008")  # BOS HSK BTC
aum_9042, time_9042 = get_aum_and_time("9042")  # CAM BTC
aum_9439, time_9439 = get_aum_and_time("9439")  # HGI BTC


# In[7]:


# Close the browser
driver.quit()


# In[8]:


# Use the update time from the first ETF as the current date
time_9008_date = time_9008.replace('as at ', '').strip()
current_date = time_9008_date


# In[9]:


# Load or create a CSV file to store the AUM data
csv_file = 'aum_data.csv'
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Date', 'AUM_9008', 'AUM_9042', 'AUM_9439'])


# In[10]:


# Check if the current date is already in the DataFrame
if current_date not in df['Date'].values:
    # Create a new DataFrame for the current entry
    new_data = pd.DataFrame({
        'Date': [current_date], 
        'AUM_9008': [aum_9008], 
        'AUM_9042': [aum_9042], 
        'AUM_9439': [aum_9439]
    })
    
    # Append the new data using pd.concat()
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Save the updated DataFrame to the CSV file
    df.to_csv(csv_file, index=False)
    print("AUM data updated successfully.")
else:
    print("AUM data for today has already been recorded.")


# In[12]:


# Print the DataFrame
df


# In[ ]:





# In[ ]:





# In[ ]:




