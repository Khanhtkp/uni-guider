from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin

# Setup Selenium
options = Options()
options.add_argument("--headless")  # Run browser in headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Variables
start_url = "https://ctsv.hust.edu.vn/#/danh-sach-su-kien"
image_links = set()

driver.get(start_url)
driver.implicitly_wait(10)  # Wait for JavaScript to load

# Extract image links
elements = driver.find_elements(By.CSS_SELECTOR, 'div.image-event')# for img in images:
a_values = [element.find_element(By.TAG_NAME, 'a') for element in elements]
href_values = [a_value.get_attribute('href') for a_value in a_values]

with open('file.json', 'w') as f:
    json.dump(href_values, f, indent=4)
