from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load links
with open("file.json", 'r') as f:
    links = json.load(f)

# Setup Selenium
options = Options()
options.add_argument("--headless")  # Run browser in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")  # Example user-agent
service = Service(executable_path="chromedriver-mac-arm64/chromedriver")  # Replace with your chromedriver path

contents = []

# Iterate through links
for link in links:
    driver = webdriver.Chrome(service=service, options=options)  # New browser instance for each link
    driver.get(link)
    try:
        # Wait for element and extract text
        content = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.a-desc"))
        ).text
        contents.append(content)
    except Exception as e:
        print(f"Error fetching content from {link}: {e}")
        contents.append("")  # Append empty content in case of failure
    finally:
        driver.quit()  # Close the browser instance
    print(f"Finished fetching content from: {link}")

# Save contents to a file
with open("contents.json", "w") as f:
    json.dump(contents, f, indent=4)
