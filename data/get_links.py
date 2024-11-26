from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
options = Options()
options.add_argument("--headless")  # Run browser in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")  # Example user-agent
service = Service(executable_path="chromedriver-mac-arm64/chromedriver")  # Replace with your chromedriver path
driver = webdriver.Chrome(service=service, options=options)
def scrape(links: list):
    dict_data = []
    hrefs = set()
    # Iterate through links
    for link in links:
        hrefs.add(link)
        driver = webdriver.Chrome(service=service, options=options)  # New browser instance for each link
        driver.get(link)
        try:
            # Wait for element and extract text
            content = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.a-desc"))
            ).text
            metadata = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.content-card")))
            title, info = metadata[0].text.split("\n", 1)
            uncared, criteria = metadata[1].text.split("\n", 1)
            info = info.split("\n")     
            info_dict = {info[i]: info[i + 1] for i in range(0, len(info), 2)}
            
        except Exception as e:
            print(f"Error fetching content from {link}: {e}")
        finally:
            driver.quit()  # Close the browser instance
        print(f"Finished fetching content from: {link}")
        dict = {
            'title': title,
            'page_content': content,
            'criteria': criteria,
        }
        dict.update(info_dict)
        dict_data.append(dict)

    file_path = "data/full_data.csv"
    with open(file_path, "w", encoding='utf-8', newline="") as f:
        fieldnames = dict_data[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
    
        # Write the header (column names)
        writer.writeheader()
        
        # Write the data rows
        writer.writerows(dict_data)
            
    print(f"List of dictionaries has been written to {file_path}")

    with open("data/file.json", 'w') as f:
        json.dump(list(hrefs), f, indent=4)
