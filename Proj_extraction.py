from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
print("Please Enter a Company Tag used in Yahoo Finance(e.g TSLA): ")
compname = input()

url = f"https://finance.yahoo.com/quote/{compname}/history?period1=1542844800&period2=1700611200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
driver_path = r'C:\codes\cd\chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.get(url) 

driver.implicitly_wait(10)
for _ in range(15):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(1)
table_xpath = '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table'
table_element = driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table')

table_html = table_element.get_attribute('outerHTML')

driver.quit()

soup = BeautifulSoup(table_html, 'html.parser')

table_data = []
for row in soup.find_all('tr'):
    row_data = [col.get_text(strip=True) for col in row.find_all(['th', 'td'])]
    table_data.append(row_data)

columns = table_data[0]  
df = pd.DataFrame(table_data[1:], columns=columns)
df = df.iloc[:-1]
excel_filename = 'stock_data.csv'
df.to_csv(excel_filename, index=False)

print(f"Data has been extracted and stored in {excel_filename}")
